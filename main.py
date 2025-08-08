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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.channel import Base, Channel
from core.project import Project
from core.power_supply_it6302 import Power_supply_it6302
from core.pcie_1762h_controller import Pcie_1762h
from view.config_view import ConfigViewModel
from core.db import engine

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

    # Base.metadata.drop_all(engine) # For clean test runs
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create channels if they don't exist
    if session.query(Channel).count() == 0:
        logger.info("Creating channels...")
        channels = [
            Channel(index=0, name="通道1"),
            Channel(index=1, name="通道2"),
            Channel(index=2, name="通道3")
        ]
        session.add_all(channels)
        session.commit()
    else:
        channels = session.query(Channel).order_by(Channel.id).all()


    # Create a sample project for each channel
    # TODO Add Pcie_1762h data
    if session.query(Project).count() == 0:
        logger.info("Creating and saving new projects...")

        # Project 1 for Channel 1
        project1 = Project(name="项目A")
        ps1 = Power_supply_it6302(resource_name="ASRL3::INSTR", baud_rate=9600)
        ps1.channels[0].voltage = 5.0
        ps1.channels[0].current = 1.0
        ps1.channels[1].voltage = 15.0
        ps1.channels[1].current = 1.1
        ps1.channels[2].voltage = 3.3
        ps1.channels[2].current = 1.2
        project1.power_supply = ps1
        
        # Add PCIe-1762H controller (通道初始化已在类内部实现)
        pcie1 = Pcie_1762h()
        project1.pcie_1762h = pcie1
        
        project1.channel = channels[0]

        session.add(project1)

        # Project 2 for Channel 1
        project2 = Project(name="项目B")
        project2.channel = channels[0]
        ps2 = Power_supply_it6302(resource_name="ASRL3::INSTR", baud_rate=9600)
        ps2.channels[0].voltage = 3.0
        ps2.channels[0].current = 2.0
        ps2.channels[1].voltage = 13.0
        ps2.channels[1].current = 2.1
        ps2.channels[2].voltage = 4.3
        ps2.channels[2].current = 2.2
        project2.power_supply = ps2
        
        # Add PCIe-1762H controller (通道初始化已在类内部实现)
        pcie2 = Pcie_1762h()
        project2.pcie_1762h = pcie2
        session.add(project2)

        # Project 3 for Channel 2
        project3 = Project(name="项目C")
        ps3 = Power_supply_it6302(resource_name="ASRL3::INSTR", baud_rate=9600)
        ps3.channels[0].voltage = 2.0
        ps3.channels[0].current = 2.0
        ps3.channels[1].voltage = 12.0
        ps3.channels[1].current = 2.0
        ps3.channels[2].voltage = 4.3
        ps3.channels[2].current = 2.2
        project3.power_supply = ps3
        
        # Add PCIe-1762H controller (通道初始化已在类内部实现)
        pcie3 = Pcie_1762h()
        project3.pcie_1762h = pcie3
        
        project3.channel = channels[1]
        session.add(project3)

        session.commit()
        logger.info("Sample projects created.")

    session.close()
    # --- Database End ---

    backend = App()
    config_view_model = ConfigViewModel()

    engine = QQmlApplicationEngine()
    # engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui", "styles"))
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui/"))

    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("configViewModel", config_view_model)


    engine.load(os.path.join(os.path.dirname(__file__), "ui/HILContent/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
