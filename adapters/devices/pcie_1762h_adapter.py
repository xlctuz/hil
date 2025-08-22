from core.interfaces.pcie_1762h_port import Pcie1762hPort
from core.entities.pcie_1762h import Pcie1762h, Status
from Automation.BDaq import *
from core.logger import logger
import traceback


class Pcie1762hAdapter(Pcie1762hPort):
    def __init__(self):
        # Device configuration
        self.device_description = "PCI-1762,BID#0"
        self.start_channel = 0
        self.channel_count = 16

    def run_test(self, pcie_1762h: Pcie1762h):
        '''Run a test on the PCIE-1762H device'''
        # Create an instance of the instant digital output
        instant_do = InstantDoCtrl()

        # Set the device description
        instant_do.selectedDevice = DeviceInformation(self.device_description)

        # Prepare the data to write (set all DO channels based on pcie_1762h configuration)
        data = 0  # Start with all channels low
        for channel in pcie_1762h.do_channels:
            if channel.status == Status.HIGH:
                # Set the bit corresponding to this channel to high
                data |= (1 << channel.index)

        logger.info(f"Writing data {data} to digital output channels")

        # Write the data to the digital output channels
        instant_do.writeAny(self.start_channel, self.channel_count, [data])

        # Clean up
        instant_do.dispose()

    def get_di(self, pcie_1762h: Pcie1762h) -> int:
        '''Get digital input values from the PCIE-1762H device'''
        # Create an instance of the instant digital input
        instant_di = InstantDiCtrl()

        # Set the device description
        instant_di.selectedDevice = DeviceInformation(self.device_description)

        # Read data from digital input channels
        data = instant_di.readAny(self.start_channel, self.channel_count)

        # Clean up
        instant_di.dispose()

        logger.info(f"Read data {data} from digital input channels")

        return data