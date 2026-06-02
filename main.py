# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from Microphone import Microphone
from Worker import Worker
import logging

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(Path(__file__).parent)
    engine.loadFromModule("GuitarTuner", "Main")

    worker = Worker()
    engine.rootContext().setContextProperty("worker", worker)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
    