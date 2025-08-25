from core.logger import logger
from core.interfaces.scheduler_port import SchedulerPort


class StopPcie1762hMonitoring:
    def __call__(self, scheduler: SchedulerPort):
        if scheduler:
            logger.info("Stopping PCIE-1762H monitoring")
            scheduler.stop_polling()
