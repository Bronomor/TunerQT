import pyaudio
import numpy as np
import logging
from collections import deque

from PySide6.QtCore import QObject, Signal, Slot


class Microphone(QObject):

    freqChanged = Signal(float)

    def __init__(self):
        super().__init__()

        self.CHUNK = 4096
        self.RATE = 44100

        self.audio = None
        self.stream = None

        self.last_freqs = deque(maxlen=5)
        self.stopRequested = False

    def push_frequency(self, freq):

        if freq == 0:
            self.last_freqs.clear()
            self.freqChanged.emit(0.0)
            return

        if not (50 < freq < 2000):
            return

        self.last_freqs.append(freq)

        if len(self.last_freqs) < 3:
            return

        avg = sum(self.last_freqs) / len(self.last_freqs)

        self.freqChanged.emit(round(avg, 2))

    def autocorr_pitch(self, signal, rate):
        signal = signal - np.mean(signal)

        corr = np.correlate(signal, signal, mode='full')
        corr = corr[len(corr)//2:]

        start = int(rate / 1000)
        corr[:start] = 0

        if np.max(corr) < 1e-6:
            return 0

        peak = np.argmax(corr)
        if peak == 0:
            return 0

        if np.max(corr) < 0.2 * np.sum(corr):
            return 0

        return rate / peak

    def is_silent(self, samples):
        energy = np.mean(np.abs(samples))
        return energy < 500  # eksperymentalnie

    @Slot()
    def run(self):

        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        logging.debug("Audio loop started")

        while not self.stopRequested:

            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)

            freq = self.autocorr_pitch(samples, self.RATE)
            self.push_frequency(freq)

        self.cleanup()

    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()