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

    # --- Database Example Start ---
    # Setup database
    engine = create_engine('sqlite:///project.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new project and power supply configuration
    logger.info("Creating and saving a new project with power supply configuration...")
    new_project = Project()
    power_supply = Power_supply_it6302(resource_name="ASRL4::INSTR", baud_rate=9600)
    power_supply.channels[0].voltage = 5.0
    power_supply.channels[0].current = 1.0
    power_supply.channels[1].voltage = 12.0
    power_supply.channels[1].current = 0.5
    power_supply.channels[2].voltage = 3.3
    power_supply.channels[2].current = 0.2

    # Associate power supply with the project
    new_project.power_supply = power_supply

    session.add(new_project)
    session.commit()
    project_id = new_project.id
    logger.info(f"Project with ID {project_id} saved.")

    # Query the project and its power supply configuration
    logger.info(f"Querying for project ID {project_id} from database...")
    queried_project = session.query(Project).filter_by(id=project_id).one_or_none()

    if queried_project:
        logger.info(f"Found project ID: {queried_project.id}")
        if queried_project.power_supply:
            ps = queried_project.power_supply
            logger.info(f"  Power Supply: {ps.resource_name} @ {ps.baud_rate}bps")
            for ch in ps.channels:
                logger.info(f"    Channel {ch.index}: Voltage={ch.voltage}V, Current={ch.current}A")
    else:
        logger.warning("Could not find the project in the database.")

    session.close()
    # --- Database Example End ---

    backend = App()

    engine = QQmlApplicationEngine()
    # engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui", "styles"))
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui/"))

    engine.rootContext().setContextProperty("backend", backend)


    engine.load(os.path.join(os.path.dirname(__file__), "ui/HILContent/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
