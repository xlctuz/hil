from domain.ports.power_supply_port import PowerSupplyPort
from domain.models.power_supply import PowerSupply, IO, Channel
import pyvisa
from contextlib import contextmanager
from .visa_resource_manager import rm


# These command classes are moved from the original power_supply_it6302.py
# They are kept here as they are implementation details of the hardware adapter
class PowerSupplyError(Exception):
    pass


class ParameterError(PowerSupplyError):
    def __init__(self, message):
        super().__init__(message)


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


class PowerSupplyAdapter(PowerSupplyPort):
    def open(self, power_supply: PowerSupply):
        power_supply.instrument = rm.open_resource(power_supply.resource_name)
        power_supply.instrument.baud_rate = power_supply.baud_rate
        power_supply.instrument.data_bits = 8
        power_supply.instrument.parity = pyvisa.constants.Parity.none
        power_supply.instrument.stop_bits = pyvisa.constants.StopBits.one
        power_supply.instrument.read_termination = '\n'
        power_supply.instrument.write_termination = '\n'
        power_supply.instrument.timeout = 5000
        power_supply.instrument.flush(pyvisa.constants.VI_READ_BUF | pyvisa.constants.VI_WRITE_BUF)

    def close(self, power_supply: PowerSupply):
        if hasattr(power_supply, 'instrument') and power_supply.instrument:
            print(f"close power supply")
            power_supply.instrument.close()

    def _write(self, power_supply: PowerSupply, cmd):
        if not hasattr(power_supply, 'instrument') or not power_supply.instrument:
            raise PowerSupplyError("Power supply not opened")
        power_supply.instrument.write(cmd)

    def _read(self, power_supply: PowerSupply):
        if not hasattr(power_supply, 'instrument') or not power_supply.instrument:
            raise PowerSupplyError("Power supply not opened")
        return power_supply.instrument.read()

    def get_idn(self, power_supply: PowerSupply) -> str:
        self._write(power_supply, "*IDN?")
        response = self._read(power_supply)
        return response

    def set_voltage(self, power_supply: PowerSupply, channel: int, voltage: float):
        self._write(power_supply, PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt(voltage)
                    .result())

    def get_voltage(self, power_supply: PowerSupply, channel: int) -> float:
        self._write(power_supply, PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().volt()
                    .result())
        return float(self._read(power_supply))

    def set_current(self, power_supply: PowerSupply, channel: int, current: float):
        self._write(power_supply, PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr(current)
                    .result())

    def get_current(self, power_supply: PowerSupply, channel: int) -> float:
        self._write(power_supply, PowerSupplyCommand().syst().rem()
                    .next().root().inst().nsel(channel)
                    .next().root().sour().curr()
                    .result())
        return float(self._read(power_supply))

    def set_voltage_current(self, power_supply: PowerSupply, channel: Channel, voltage: float, current: float):
        self._write(power_supply, PowerSupplyCommand().syst().rem()
                    .next().root().sour().appl(channel, voltage, current)
                    .result())

    def measure_current(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        self._write(power_supply, PowerSupplyCommand().meas().curr(channel).result())
        return self._read(power_supply)

    def measure_voltage(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        self._write(power_supply, PowerSupplyCommand().meas().volt(channel).result())
        return self._read(power_supply)

    def measure_power(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        self._write(power_supply, PowerSupplyCommand().meas().pow(channel).result())
        return self._read(power_supply)

    def set_on_off(self, power_supply: PowerSupply, io: IO, channel: Channel = Channel.ALL):
        if channel == Channel.ALL:
            self._write(power_supply, PowerSupplyCommand().syst().rem().next().root().outp(io).result())
        else:
            self._write(power_supply, PowerSupplyCommand().syst().rem()
                        .next().root().inst().sel(channel)
                        .next().root().sour().outp(io)
                        .result())


@contextmanager
def open_power_supply(power_supply: PowerSupply, adapter: PowerSupplyAdapter):
    try:
        adapter.open(power_supply)
        yield power_supply
    except Exception as e:
        # If there was an error, we still want to try to close the instrument if it was opened
        try:
            adapter.close(power_supply)
        except:
            # If closing also fails, we don't want to mask the original error
            pass
        raise
    else:
        # Only close if there was no exception
        adapter.close(power_supply)