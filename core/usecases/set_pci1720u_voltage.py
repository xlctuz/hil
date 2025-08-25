from core.interfaces.pci1720u_port import Pci1720uPort
from core.entities.pci1720u import Pci1720u


class SetPci1720uVoltage:
    def __init__(self, pci1720u_port: Pci1720uPort):
        self.pci1720u_port = pci1720u_port

    def __call__(self, pci1720u: Pci1720u, channel_index: int, voltage: float):
        self.pci1720u_port.set_voltage(pci1720u, channel_index, voltage)
