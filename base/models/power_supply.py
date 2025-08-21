from enum import StrEnum
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from base.database import Base

import pyvisa
from contextlib import contextmanager


class PowerSupplyError(Exception):
    pass


class ParameterError(PowerSupplyError):
    def __init__(self, message):
        super().__init__(message)


class IO(StrEnum):
    ON = "ON"
    OFF = "OFF"


class Channel(StrEnum):
    CH1 = "CH1"
    CH2 = "CH2"
    CH3 = "CH3"
    ALL = "ALL"


class PowerSupplyChannel(Base):
    __tablename__ = 'power_supply_channels'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    voltage = Column(Float)
    current = Column(Float)

    power_supply_id = Column(Integer, ForeignKey('power_supplies.id'))
    power_supply = relationship("PowerSupply", back_populates="channels")


class PowerSupply(Base):
    __tablename__ = 'power_supplies'

    id = Column(Integer, primary_key=True)
    resource_name = Column(String)
    baud_rate = Column(Integer)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="power_supply", uselist=False)

    channels = relationship("PowerSupplyChannel", back_populates="power_supply", cascade="all, delete-orphan")

    def __init__(self, resource_name="", baud_rate=9600, **kwargs):
        # Initialize domain model attributes
        self.resource_name = resource_name
        self.baud_rate = baud_rate
        self.instrument = None

        # Initialize channels if not already done
        if not self.channels:
            self.channels = [PowerSupplyChannel(index=0),
                             PowerSupplyChannel(index=1),
                             PowerSupplyChannel(index=2)]

        super().__init__(**kwargs)
