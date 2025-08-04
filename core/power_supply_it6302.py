from visa_resource_manager import rm
import pyvisa
from contextlib import contextmanager
from enum import StrEnum, auto
import time

class Power_supply_error(Exception):
    pass

class Parameter_error(Power_supply_error):
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

class Power_supply_command():
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

    def outp(self, io : IO):
        self.command += f"OUTP {io}"
        return self

    def result(self):
        return self.command

    class _Syst:
        def rem(self):
            self._root.command += ":REM"
            return self


    class _Inst:
        def nsel(self, channel : int):
            if channel <= 0 or channel > 3:
                raise Parameter_error(f"channel should be in range (0, 3]")

            self._root.command += f":NSEL {channel}"
            return self

        def sel(self, channel : Channel):
            if channel == Channel.ALL:
                raise Parameter_error(f"channel can not be ALL")

            self._root.command += f":SEL {channel}"
            return self

    class _Sour:
        def volt(self, voltage : float | None = None):
            if voltage:
                self._root.command += f":VOLT {voltage}"
            else:
                self._root.command += f":VOLT?"
            return self

        def curr(self, current : float | None = None):
            if current:
                self._root.command += f":CURR {current}"
            else:
                self._root.command += f":CURR?"
            return self

        def appl(self, channel: Channel, voltage : float, current: float):
            if channel == Channel.ALL:
                raise Parameter_error(f"channel can not be ALL")

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


class Power_supply_it6302:
    def __init__(self, resource_name : str, baud_rate: int):
        self.resource_name = resource_name
        self.baud_rate = baud_rate
        self.instrument = None


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
        self.instrument.close();

    def _write(self, cmd):
        self.instrument.write(cmd)

    def _read(self):
        return self.instrument.read()


    def get_idn(self):
        self.instrument.write("*IDN?")
        response = self.instrument.read()
        return response

    def set_voltage(self, channel : int, voltage: float):
        self._write(Power_supply_command().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt(voltage)
                    .result())


    def get_voltage(self, channel : int):
        self._write(Power_supply_command().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt()
                    .result())
        return self._read()


    def set_current(self, channel : int, current: float):
        self._write(Power_supply_command().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr(current)
                    .result())


    def get_current(self, channel : int):
        self._write(Power_supply_command().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr()
                    .result())
        return self._read()


    def set_voltage_current(self, channel, voltage, current):
        self._write(Power_supply_command().syst().rem()
                    .next().root().sour().appl(channel, voltage, current)
                    .result())

    def measure_current(self, channel : Channel = Channel.ALL):
        self._write(Power_supply_command().meas().curr(channel).result())
        return self._read()


    def measure_voltage(self, channel : Channel = Channel.ALL):
        self._write(Power_supply_command().meas().volt(channel).result())
        return self._read()


    def measure_power(self, channel : Channel = Channel.ALL):
        self._write(Power_supply_command().meas().pow(channel).result())
        return self._read()


    def set_on_off(self, io : IO, channel : Channel = Channel.ALL):
        if channel == Channel.ALL:
            self._write(Power_supply_command().syst().rem().next().root().outp(io).result())
        else:
            self._write(Power_supply_command().syst().rem()
                        .next().root().inst().sel(channel)
                        .next().root().sour().outp(io)
                        .result())


@contextmanager
def open_power_supply(resource_name, baud_rate):
    ps = None
    try:
        ps = Power_supply_it6302(resource_name, baud_rate)
        ps.open()
        yield ps
    finally:
        if ps:
            ps.close()


if __name__ == "__main__":

    print(f"{Channel.CH1}")
    with open_power_supply("ASRL3::INSTR", 9600) as ps:
        print(f"设备ID: {ps.get_idn().strip()}")
        ps.set_voltage_current(Channel.CH1, 10, 2)
        print(f"通道1 电压: {ps.get_voltage(1)}")
        print(f"通道1 电流: {ps.get_current(1)}")

        print(f"关闭电源")
        ps.set_on_off(IO.OFF, Channel.CH1)
        time.sleep(2)

        print(f"通道1 测量电压: {ps.measure_voltage(Channel.CH1)}")
        print(f"通道1 测量电流: {ps.measure_current(Channel.CH1)}")
        print(f"通道1 测量功率: {ps.measure_power(Channel.CH1)}")
        print(f"通道2 测量电压: {ps.measure_voltage(Channel.CH2)}")
        print(f"通道2 测量电流: {ps.measure_current(Channel.CH2)}")
        print(f"通道2 测量功率: {ps.measure_power(Channel.CH2)}")

        print(f"开启电源")
        ps.set_on_off(IO.ON, Channel.CH1)
        time.sleep(1)

        print(f"通道1 测量电压: {ps.measure_voltage(Channel.CH1)}")
        print(f"通道1 测量电流: {ps.measure_current(Channel.CH1)}")
        print(f"通道1 测量功率: {ps.measure_power(Channel.CH1)}")
        print(f"通道2 测量电压: {ps.measure_voltage(Channel.CH2)}")
        print(f"通道2 测量电流: {ps.measure_current(Channel.CH2)}")
        print(f"通道2 测量功率: {ps.measure_power(Channel.CH2)}")

