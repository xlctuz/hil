import sys
import os
from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer
from common.logger import logger
import traceback

# Add core to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from core.channel import Base, Channel
from core.project import Project
from core.power_supply_it6302 import Power_supply_it6302, Power_supply_it6302_channel, IO, Channel as PSChannel
from core.visa_resource_manager import rm


class PowerSupplyPoller(QObject):
    polledData = Signal(dict)
    finished = Signal()
    error = Signal(str)

    def __init__(self, resource_name, baud_rate, project, parent=None):
        super().__init__(parent)
        self._resource_name = resource_name
        self._baud_rate = baud_rate
        self._project = project
        self._ps_controller = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.poll)
        self._running = False

    def start(self):
        try:
            self._ps_controller = Power_supply_it6302(resource_name = self._resource_name, baud_rate = self._baud_rate)
            self._ps_controller.open()

            # Set initial configuration from the project
            ps_config = self._project.power_supply
            for i, ch_config in enumerate(ps_config.channels):
                channel_enum = PSChannel[f"CH{i+1}"]
                if ch_config.voltage is not None and ch_config.current is not None:
                    self._ps_controller.set_voltage_current(channel_enum, ch_config.voltage, ch_config.current)
                    self._ps_controller.set_on_off(IO.ON, channel_enum)

            self._running = True
            self._timer.start(100) # 100 ms interval
            print("Poller started and power supply configured.")
        except Exception as e:
            traceback.print_exc()
            self.error.emit(f"Failed to start poller: {e}")
            self.stop()

    def stop(self):
        self._running = False
        self._timer.stop()
        if self._ps_controller:
            try:
                # Turn off all channels when polling stops
                self._ps_controller.set_on_off(IO.OFF, PSChannel.ALL)
                if self._ps_controller.instrument and self._ps_controller.instrument.session is not None:
                    self._ps_controller.close()
            except Exception as e:
                print(f"Error while closing power supply in poller: {e}")
        self._ps_controller = None
        self.finished.emit()
        print("Poller stopped.")

    def poll(self):
        if not self._running or not self._ps_controller:
            return

        try:
            data = {
                'voltage': [],
                'current': [],
                'power': []
            }
            channels = [PSChannel.CH1, PSChannel.CH2, PSChannel.CH3]
            for ch in channels:
                v_str = self._ps_controller.measure_voltage(ch).strip()
                c_str = self._ps_controller.measure_current(ch).strip()
                p_str = self._ps_controller.measure_power(ch).strip()
                
                data['voltage'].append(float(v_str) if v_str else 0.0)
                data['current'].append(float(c_str) if c_str else 0.0)
                data['power'].append(float(p_str) if p_str else 0.0)
            
            self.polledData.emit(data)
        except Exception as e:
            self.error.emit(f"Polling failed: {e}")
            self.stop()


class ProjectModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    CheckedRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._projects = []

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._projects)):
            return None
        project = self._projects[index.row()]
        if role == self.NameRole:
            return project.name
        if role == self.CheckedRole:
            return getattr(project, 'checked', False)
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._projects)

    def roleNames(self):
        return {
            self.NameRole: b'name',
            self.CheckedRole: b'checked'
        }

    def set_projects(self, projects):
        self.beginResetModel()
        self._projects = projects
        # Add checked attribute for UI state
        for p in self._projects:
            p.checked = False
        self.endResetModel()

    def get_project(self, row):
        if 0 <= row < len(self._projects):
            return self._projects[row]
        return None

    def set_checked(self, row, checked=True):
        if 0 <= row < len(self._projects):
            # Uncheck others
            for i, p in enumerate(self._projects):
                if i != row and getattr(p, 'checked', False):
                    p.checked = False
                    self.dataChanged.emit(self.index(i, 0), self.index(i, 0), [self.CheckedRole])

            # Check selected
            project = self._projects[row]
            project.checked = checked
            self.dataChanged.emit(self.index(row, 0), self.index(row, 0), [self.CheckedRole])


class PowerSupplyChannelProxy(QObject):
    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data

    @Property('QVariant', constant=True)
    def voltage(self):
        return self._channel_data.voltage if self._channel_data and self._channel_data.voltage is not None else None

    @Property('QVariant', constant=True)
    def current(self):
        return self._channel_data.current if self._channel_data and self._channel_data.current is not None else None

class PowerSupplyProxy(QObject):
    resourceNameChanged = Signal()
    baudRateChanged = Signal()

    def __init__(self, power_supply_data, parent=None):
        super().__init__(parent)
        self._power_supply_data = power_supply_data
        self._channels = []
        if self._power_supply_data:
            # sort channels by index
            sorted_channels = sorted(self._power_supply_data.channels, key=lambda c: c.index)
            for ch_data in sorted_channels:
                self._channels.append(PowerSupplyChannelProxy(ch_data, self))
        # ensure 3 channels exist for QML binding
        while len(self._channels) < 3:
            self._channels.append(PowerSupplyChannelProxy(None, self))

    @Property(str, notify=resourceNameChanged)
    def resource_name(self):
        return self._power_supply_data.resource_name if self._power_supply_data else ""

    @Property(int, notify=baudRateChanged)
    def baud_rate(self):
        return self._power_supply_data.baud_rate if self._power_supply_data else 9600

    @Property(QObject, constant=True)
    def ch1(self):
        return self._channels[0]


    @Property(QObject, constant=True)
    def ch2(self):
        return self._channels[1]

    @Property(QObject, constant=True)
    def ch3(self):
        return self._channels[2]


class ProjectProxy(QObject):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self._project_data = project_data
        self._power_supply = PowerSupplyProxy(project_data.power_supply if project_data else None, self)

    @Property('QVariant', constant=True)
    def name(self):
        return self._project_data.name if self._project_data else None

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply


class ConfigViewModel(QObject):
    currentProjectChanged = Signal()
    powerSupplyTestFailed = Signal(str)
    powerSupplyDataUpdated = Signal(list, list, list) # voltage, current, power

    def __init__(self, parent=None):
        super().__init__(parent)
        self._poller_thread = None
        self._poller = None


        db_path = 'project.db'
        self._engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)

        self._project_model = ProjectModel()
        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
        self._current_channel_index = 0

    @Property(QObject, constant=True)
    def projectsModel(self):
        return self._project_model

    @Property(QObject, notify=currentProjectChanged)
    def currentProject(self):
        return self._current_project_proxy

    @Property('QVariant', constant=True)
    def availableVisaResources(self):
        try:
            return list(rm.list_resources())
        except Exception as e:
            print(f"Could not list VISA resources: {e}")
            return []

    @Slot(str, int)
    def setPowerSupplyConfig(self, resource_name, baud_rate):
        if not self._current_project or not self._current_project.power_supply:
            return

        session = self._Session()
        try:
            power_supply = session.merge(self._current_project.power_supply)
            power_supply.resource_name = resource_name
            power_supply.baud_rate = baud_rate
            session.commit()
            print(f"Updated config for project {self._current_project.id}: Resource={resource_name}, Baudrate={baud_rate}")

            self._current_project.power_supply.resource_name = resource_name
            self._current_project.power_supply.baud_rate = baud_rate

            self._current_project_proxy.powerSupply.resourceNameChanged.emit()
            self._current_project_proxy.powerSupply.baudRateChanged.emit()
        except Exception as e:
            print(f"Error updating power supply config: {e}")
            session.rollback()
        finally:
            session.close()

    @Slot(int)
    def selectChannel(self, index):
        self._current_channel_index = index
        print(f"Channel {index + 1} selected")
        session = self._Session()
        try:
            # Assuming channel IDs are 1, 2, 3...
            channel_id = index + 1
            projects = session.query(Project).filter(Project.channel_id == channel_id).options(joinedload(Project.power_supply).joinedload(Power_supply_it6302.channels)).all()
            self._project_model.set_projects(projects)
        finally:
            session.close()

        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(str)
    def addProject(self, name):
        if not name:
            return
        print(f"Adding project {name} to channel {self._current_channel_index + 1}")
        session = self._Session()
        try:
            channel_id = self._current_channel_index + 1
            # Create a new project
            new_project = Project(name=name)
            new_project.channel_id = channel_id

            # Create default power supply config
            power_supply = Power_supply_it6302(resource_name="ASRL3::INSTR", baud_rate=9600)
            new_project.power_supply = power_supply

            session.add(new_project)
            session.commit()
            print(f"Project {name} added with id {new_project.id}")
        finally:
            session.close()

        # Refresh the project list
        self.selectChannel(self._current_channel_index)

    @Slot(int, float)
    def setPowerSupplyVoltage(self, channel_index, voltage):
        if not self._current_project or not self._current_project.power_supply:
            return

        session = self._Session()
        try:
            power_supply = session.merge(self._current_project.power_supply)
            channel = next((ch for ch in power_supply.channels if ch.index == channel_index), None)
            if channel:
                channel.voltage = voltage
                session.commit()
                print(f"Updated voltage for project {self._current_project.id}, channel {channel_index} to {voltage}")
                # Refresh current project data to update UI
                self._current_project.power_supply.channels[channel_index].voltage = voltage
                self.currentProjectChanged.emit()
        except Exception as e:
            print(f"Error updating voltage: {e}")
            session.rollback()
        finally:
            session.close()

    @Slot(int, float)
    def setPowerSupplyCurrent(self, channel_index, current):
        if not self._current_project or not self._current_project.power_supply:
            return

        session = self._Session()
        try:
            power_supply = session.merge(self._current_project.power_supply)
            channel = next((ch for ch in power_supply.channels if ch.index == channel_index), None)
            if channel:
                channel.current = current
                session.commit()
                print(f"Updated current for project {self._current_project.id}, channel {channel_index} to {current}")
                # Refresh current project data to update UI
                self._current_project.power_supply.channels[channel_index].current = current
                self.currentProjectChanged.emit()
        except Exception as e:
            print(f"Error updating current: {e}")
            session.rollback()
        finally:
            session.close()

    @Slot(bool)
    def togglePowerSupplyTest(self, testing):
        if not self._current_project or not self._current_project.power_supply:
            msg = "没有为测试选择项目."
            print(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        ps_config = self._current_project.power_supply
        if not ps_config.resource_name:
            msg = "电源资源名称未配置."
            print(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        if testing:
            # Stop any existing poller first
            if self._poller_thread and self._poller_thread.isRunning():
                self._poller.stop()
                self._poller_thread.quit()
                self._poller_thread.wait()

            # Setup and start the poller thread
            self._poller_thread = QThread()
            self._poller = PowerSupplyPoller(ps_config.resource_name, ps_config.baud_rate, self._current_project)
            self._poller.moveToThread(self._poller_thread)

            self._poller.polledData.connect(self._on_power_supply_data_updated)
            self._poller.error.connect(self.powerSupplyTestFailed)
            self._poller_thread.started.connect(self._poller.start)
            self._poller.finished.connect(self._poller_thread.quit)
            
            self._poller_thread.start()
        else:
            if self._poller:
                self._poller.stop() # This will turn off channels and close connection
            if self._poller_thread:
                self._poller_thread.quit()
                self._poller_thread.wait()
            self._poller_thread = None
            self._poller = None
            print("Test stopped and poller cleaned up.")

    @Slot(dict)
    def _on_power_supply_data_updated(self, data):
        logger.info(f"on power supply data updated {data['voltage']}, {data['current']}, {data['power']}")
        self.powerSupplyDataUpdated.emit(data['voltage'], data['current'], data['power'])

    @Slot()
    def resetPowerSupplySettings(self):
        if not self._current_project or not self._current_project.power_supply:
            print("No project or power supply selected.")
            return

        print(f"Resetting power supply settings for project {self._current_project.name}")
        session = self._Session()
        try:
            power_supply = session.merge(self._current_project.power_supply)
            for channel in power_supply.channels:
                channel.voltage = None
                channel.current = None
            session.commit()
            print("Power supply settings reset.")

            # Refresh current project data to update UI
            for channel_data in self._current_project.power_supply.channels:
                channel_data.voltage = None
                channel_data.current = None
            self.currentProjectChanged.emit()
        except Exception as e:
            print(f"Error resetting power supply settings: {e}")
            session.rollback()
        finally:
            session.close()

    @Slot()
    def deleteCurrentProject(self):
        if not self._current_project:
            print("No project selected to delete.")
            return

        print(f"Deleting project {self._current_project.name} (ID: {self._current_project.id})")
        session = self._Session()
        try:
            # Re-attach the object to the session before deleting
            project_to_delete = session.merge(self._current_project)
            session.delete(project_to_delete)
            session.commit()
            print("Project deleted.")
        except Exception as e:
            print(f"Error deleting project: {e}")
            session.rollback()
        finally:
            session.close()

        # Refresh the project list for the current channel
        self.selectChannel(self._current_channel_index)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            print(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectProxy(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()
