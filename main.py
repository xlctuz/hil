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
import logging
from core.app import App


logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(levelname)s] [%(thread)d] [%(filename)s:%(lineno)d] %(message)s") # 确保basicConfig的级别也足够低，或者移除basicConfig并手动添加handler

logger = logging.getLogger("hil") # 获取logger
logger.setLevel(logging.DEBUG) # 设置logger级别为DEBUG，可以显示DEBUG及以上级别的日志

if __name__ == "__main__":
    app = QApplication(sys.argv)

    logger.info("main")

    backend = App()

    # 关键步骤：设置 QML 引擎的路径，使其能找到 styles 目录
    # 假设你的 styles 目录在项目根目录
    engine = QQmlApplicationEngine()
    # engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui", "styles"))
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui/"))

    engine.rootContext().setContextProperty("backend", backend)


    # # 应用你的自定义样式
    # QQuickStyle.setStyle("HilAppStyle")

    engine.load(os.path.join(os.path.dirname(__file__), "ui/HILContent/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
