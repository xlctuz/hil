import sys
import os
from Automation.BDaq.InstantAoCtrl import InstantAoCtrl
from Automation.BDaq.BDaqApi import TArray, AdxEnumToString, BioFailed
from core.interfaces.pci1720u_port import Pci1720uPort
from core.entities.pci1720u import Pci1720u
from core.logger import logger

class Pci1720uAdapter(Pci1720uPort):
    def __init__(self):
        self.instantAoCtrl = None

    def _initialize_device(self, device_number: int):
        if self.instantAoCtrl:
            self.instantAoCtrl.Dispose()

        device_description = self.get_device_description(device_number)
        self.instantAoCtrl = InstantAoCtrl(device_description)

    def set_voltage(self, pci1720u: Pci1720u, channel_index: int, voltage: float):
        try:
            self._initialize_device(pci1720u.device_number)

            # The driver expects a list/array of voltages
            voltages = TArray(float, 1)
            voltages[0] = voltage

            ret = self.instantAoCtrl.Write(channel_index, 1, voltages)
            if BioFailed(ret):
                raise Exception(f"Failed to set voltage on channel {channel_index}")

            logger.info(f"Set PCI-1720U Channel {channel_index} to {voltage}V")

        except Exception as e:
            logger.error(f"Error setting PCI-1720U voltage: {e}")
            raise e
        finally:
            if self.instantAoCtrl:
                self.instantAoCtrl.Dispose()
                self.instantAoCtrl = None

    def get_device_description(self, device_number: int) -> str:
        # This logic might need adjustment based on how devices are enumerated
        return f"PCI-1720U,BID#{device_number}"
