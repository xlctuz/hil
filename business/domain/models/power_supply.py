from enum import StrEnum


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


class PowerSupplyChannel:
    def __init__(self, index):
        self.index = index
        self.voltage = None
        self.current = None


class PowerSupply:
    def __init__(self, resource_name="", baud_rate=9600):
        self.resource_name = resource_name
        self.baud_rate = baud_rate
        self.channels = [
            PowerSupplyChannel(0),
            PowerSupplyChannel(1),
            PowerSupplyChannel(2)
        ]
        # Add instrument attribute for hardware adapter
        self.instrument = None