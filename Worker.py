from Microphone import Microphone
from PySide6.QtCore import QObject, QThread, Slot, Signal
import math

NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "H"
]


class Worker(QObject):

    textChanged = Signal(str, float, float)

    def __init__(self):
        super().__init__()

        self.thread = QThread()
        self.microphone = Microphone()

        self.microphone.moveToThread(self.thread)

        self.microphone.freqChanged.connect(self.onFreq)

        self.thread.started.connect(self.microphone.run)

    @Slot(float)
    def onFreq(self, value):
        note, target_frequency = self.freq_to_note(value)
        cents = self.cents_off(value, target_frequency)
        self.textChanged.emit(note, value, cents)

    @Slot()
    def start(self):
        self.microphone.stopRequested = False
        self.thread.start()

    @Slot()
    def stop(self):
        self.microphone.stopRequested = True
        self.thread.quit()
        self.thread.wait()

    def freq_to_note(self, freq):
        import math

        if freq is None or freq <= 0:
            return "--", 0

        if freq < 20:
            return "--", 0

        n = 12 * math.log2(freq / 440.0)
        n = round(n)
        note_index = (n + 9) % 12
        octave = 4 + ((n + 9) // 12)

        target_freq = 440.0 * (2 ** (n / 12))
        return NOTE_NAMES[note_index] + str(octave), target_freq

    def cents_off(self, freq, target_freq):
        return 1200 * math.log2(freq / target_freq)
