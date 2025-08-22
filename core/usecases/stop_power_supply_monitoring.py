from core.logger import logger


class StopPowerSupplyMonitoring:
    def __call__(self, poller, thread):
        if poller:
            logger.info("Stopping power supply poller")
            poller.stop()

        if thread and thread.isRunning():
            logger.info("Waiting for poller thread to finish")
            thread.quit()
            thread.wait()