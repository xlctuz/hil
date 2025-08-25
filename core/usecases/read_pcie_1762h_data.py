from core.entities.pcie_1762h import Pcie1762h
from core.interfaces.pcie_1762h_port import Pcie1762hPort
from core.logger import logger


class ReadPcie1762hData:
    def __init__(self, pcie_1762h_port: Pcie1762hPort):
        self.pcie_1762h_port = pcie_1762h_port

    def __call__(self, pcie_1762h: Pcie1762h) -> int:
        logger.info(f"Reading DIO data for pcie_1762h id: {pcie_1762h.id}")
        
        if not pcie_1762h:
            raise ValueError("PCIE-1762H configuration not provided")

        try:
            di_data = self.pcie_1762h_port.get_di(pcie_1762h)
            return di_data
        except Exception as e:
            logger.error(f"Error reading DIO status: {str(e)}")
            raise e
