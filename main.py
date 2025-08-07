# main.py
import os
import sys
# import resources_rc
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlDebuggingEnabler
QQmlDebuggingEnabler.enableDebugging(True)
from PySide6.QtCharts import QChartView, QChart, QLineSeries
import ui.resources_rc
from common.logger import logger
from PySide6.QtCore import QObject, Property
from core.channel import Channel

class App(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._channels = [Channel(0), Channel(1), Channel(2)]

    @Property(list, constant=True)
    def channels(self):
        return self._channels

if __name__ == "__main__":
    app = QApplication(sys.argv)

    logger.info("main")

    backend = App()

    engine = QQmlApplicationEngine()
    # engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui", "styles"))
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui/"))

    engine.rootContext().setContextProperty("backend", backend)


    engine.load(os.path.join(os.path.dirname(__file__), "ui/HILContent/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
