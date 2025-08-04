# main.py
import os
import sys
import resources_rc
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # 关键步骤：设置 QML 引擎的路径，使其能找到 styles 目录
    # 假设你的 styles 目录在项目根目录
    engine = QQmlApplicationEngine()
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui", "styles"))
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui/HIL"))

    # # 应用你的自定义样式
    # QQuickStyle.setStyle("HilAppStyle")

    engine.load(os.path.join(os.path.dirname(__file__), "ui/HIL/HILContent/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
