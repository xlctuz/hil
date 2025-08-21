from domain.ports.pcie_1762h_port import Pcie1762hPort
from domain.models.pcie_1762h import Pcie1762h, Status
import time


deviceDescription = "PCIE-1762H,BID#0"
profilePath = u"pcie-1762h.xml"
startPort = 0
portCount = 1


class Pcie1762hAdapter(Pcie1762hPort):
    def run_test(self, pcie_1762h: Pcie1762h):
        from Automation.BDaq.InstantDoCtrl import InstantDoCtrl

        instantDoCtrl = None
        try:
            instantDoCtrl = InstantDoCtrl(deviceDescription)
            instantDoCtrl.loadProfile = profilePath

            port = instantDoCtrl.readAny(0, 2)[1]
            for c in pcie_1762h.do_channels:
                i = c.index // 8
                j = c.index % 8
                if c.status == Status.HIGH:
                    port[i] |= 1 << j
                elif c.status == Status.LOW:
                    port[i] &= ~(1 << j)

            instantDoCtrl.writeAny(0, 2, port)
            time.sleep(0.5)
            return instantDoCtrl.readAny(0, 2)[1]
        finally:
            if instantDoCtrl:
                instantDoCtrl.dispose()

    def get_di(self, pcie_1762h: Pcie1762h):
        from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
        instantDiCtrl = None
        try:
            instantDiCtrl = InstantDiCtrl(deviceDescription)
            instantDiCtrl.loadProfile = profilePath

            return instantDiCtrl.readAny(0, 2)[1]
        finally:
            if instantDiCtrl:
                instantDiCtrl.dispose()

    def set_do_channel_name(self, pcie_1762h: Pcie1762h, index: int, name: str):
        channel = next((ch for ch in pcie_1762h.do_channels if ch.index == index), None)
        if channel:
            channel.name = name

    def set_do_channel_status(self, pcie_1762h: Pcie1762h, index: int, status: Status):
        channel = next((ch for ch in pcie_1762h.do_channels if ch.index == index), None)
        if channel:
            channel.status = status