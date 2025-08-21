from enum import StrEnum
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .channel import Base
import pyvisa
from contextlib import contextmanager
from base.devices.visa_resource_manager import rm
import time


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


def _next(self):
    self._root.command += ";"
    return self


def _root(self):
    self._root.command += ":"
    return self._root


def _result(self):
    return self._root.command


def _constructor(self, root):
    self._root = root


def _add_common_method(cls):
    cls.next = _next
    cls.root = _root
    cls.result = _result
    cls.__init__ = _constructor


class PowerSupplyCommand:
    def __init__(self):
        self.command = ""
        _add_common_method(self._Syst)
        _add_common_method(self._Inst)
        _add_common_method(self._Sour)
        _add_common_method(self._Meas)
        self._syst = self._Syst(self)
        self._inst = self._Inst(self)
        self._sour = self._Sour(self)
        self._meas = self._Meas(self)

    def syst(self):
        self.command += "SYST"
        return self._syst

    def inst(self):
        self.command += "INST"
        return self._inst

    def sour(self):
        self.command += "SOUR"
        return self._sour

    def meas(self):
        self.command += "MEAS"
        return self._meas

    def outp(self, io: IO):
        self.command += f"OUTP {io}"
        return self

    def result(self):
        return self.command

    class _Syst:
        def rem(self):
            self._root.command += ":REM"
            return self

    class _Inst:
        def nsel(self, channel: int):
            if channel <= 0 or channel > 3:
                raise ParameterError("channel should be in range (0, 3]")

            self._root.command += f":NSEL {channel}"
            return self

        def sel(self, channel: Channel):
            if channel == Channel.ALL:
                raise ParameterError("channel can not be ALL")

            self._root.command += f":SEL {channel}"
            return self

    class _Sour:
        def volt(self, voltage: float | None = None):
            if voltage:
                self._root.command += f":VOLT {voltage}"
            else:
                self._root.command += f":VOLT?"
            return self

        def curr(self, current: float | None = None):
            if current:
                self._root.command += f":CURR {current}"
            else:
                self._root.command += f":CURR?"
            return self

        def appl(self, channel: Channel, voltage: float, current: float):
            if channel == Channel.ALL:
                raise ParameterError(f"channel can not be ALL")

            self._root.command += f":APPL {channel},{voltage},{current}"
            return self

        def outp(self, io: IO):
            self._root.command += f":CHAN:OUTP {io}"
            return self

    class _Meas:
        def curr(self, channel):
            self._root.command += f":CURR? {channel}"
            return self

        def volt(self, channel):
            self._root.command += f":VOLT? {channel}"
            return self

        def pow(self, channel):
            self._root.command += f":POW? {channel}"
            return self


class PowerSupplyChannel:
    def __init__(self, index):
        self.index = index
        self.voltage = None
        self.current = None


class PowerSupplyChannelORM(Base):
    __tablename__ = 'power_supply_channels'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    voltage = Column(Float)
    current = Column(Float)

    power_supply_id = Column(Integer, ForeignKey('power_supplies.id'))
    power_supply = relationship("PowerSupplyORM", back_populates="channels")


class PowerSupplyORM(Base):
    __tablename__ = 'power_supplies'

    id = Column(Integer, primary_key=True)
    resource_name = Column(String)
    baud_rate = Column(Integer)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("ProjectORM", back_populates="power_supply", uselist=False)

    channels = relationship("PowerSupplyChannelORM", back_populates="power_supply", cascade="all, delete-orphan")

    def __init__(self, resource_name="", baud_rate=9600, **kwargs):
        # Initialize domain model attributes
        self.resource_name = resource_name
        self.baud_rate = baud_rate
        self.instrument = None
        
        # Initialize channels if not already done
        if not self.channels:
            self.channels = [PowerSupplyChannelORM(index=0),
                             PowerSupplyChannelORM(index=1),
                             PowerSupplyChannelORM(index=2)]
        
        super().__init__(**kwargs)

    # Domain model methods
    def open(self):
        self.instrument = rm.open_resource(self.resource_name)
        self.instrument.baud_rate = self.baud_rate
        self.instrument.data_bits = 8
        self.instrument.parity = pyvisa.constants.Parity.none
        self.instrument.stop_bits = pyvisa.constants.StopBits.one
        self.instrument.read_termination = '\n'
        self.instrument.write_termination = '\n'
        self.instrument.timeout = 5000
        self.instrument.flush(pyvisa.constants.VI_READ_BUF | pyvisa.constants.VI_WRITE_BUF)

    def close(self):
        print(f"close power supply")
        if self.instrument:
            self.instrument.close()

    def _write(self, cmd):
        if not self.instrument:
            raise PowerSupplyError("Power supply not opened")
        self.instrument.write(cmd)

    def _read(self):
        if not self.instrument:
            raise PowerSupplyError("Power supply not opened")
        return self.instrument.read()

    def get_idn(self):
        self._write("*IDN?")
        response = self._read()
        return response

    def set_voltage(self, channel: int, voltage: float):
        self._write(PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt(voltage)
                    .result())

    def get_voltage(self, channel: int) -> float:
        self._write(PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt()
                    .result())
        return float(self._read())

    def set_current(self, channel: int, current: float):
        self._write(PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr(current)
                    .result())

    def get_current(self, channel: int) -> float:
        self._write(PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr()
                    .result())
        return float(self._read())

    def set_voltage_current(self, channel: Channel, voltage: float, current: float):
        self._write(PowerSupplyCommand().syst().rem()
                    .next().root().sour().appl(channel, voltage, current)
                    .result())

    def measure_current(self, channel: Channel = Channel.ALL) -> str:
        self._write(PowerSupplyCommand().meas().curr(channel).result())
        return self._read()

    def measure_voltage(self, channel: Channel = Channel.ALL) -> str:
        self._write(PowerSupplyCommand().meas().volt(channel).result())
        return self._read()

    def measure_power(self, channel: Channel = Channel.ALL) -> str:
        self._write(PowerSupplyCommand().meas().pow(channel).result())
        return self._read()

    def set_on_off(self, io: IO, channel: Channel = Channel.ALL):
        if channel == Channel.ALL:
            self._write(PowerSupplyCommand().syst().rem().next().root().outp(io).result())
        else:
            self._write(PowerSupplyCommand().syst().rem()
                        .next().root().inst().sel(channel)
                        .next().root().sour().outp(io)
                        .result())


# For backward compatibility, we can create an alias
PowerSupply = PowerSupplyORM
PowerSupplyChannel = PowerSupplyChannelORM


@contextmanager
def open_power_supply(power_supply: PowerSupplyORM):
    try:
        power_supply.open()
        yield power_supply
    except Exception as e:
        # If there was an error, we still want to try to close the instrument if it was opened
        try:
            power_supply.close()
        except:
            # If closing also fails, we don't want to mask the original error
            pass
        raise
    else:
        # Only close if there was no exception
        power_supply.close()