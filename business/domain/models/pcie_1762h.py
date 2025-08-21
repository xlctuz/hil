from enum import Enum


class Status(Enum):
    HIGH = "high"
    LOW = "low"
    NA = "na"


class Pcie1762hDiChannel:
    def __init__(self, index):
        self.index = index
        self.name = ""


class Pcie1762hDoChannel:
    def __init__(self, index):
        self.index = index
        self.name = ""
        self.status = Status.NA


class Pcie1762h:
    def __init__(self):
        self.do_channels = [Pcie1762hDoChannel(i) for i in range(16)]
        self.di_channels = [Pcie1762hDiChannel(i) for i in range(16)]