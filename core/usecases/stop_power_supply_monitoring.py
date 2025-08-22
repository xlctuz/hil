from core.logger import logger
from core.interfaces.scheduler_port import SchedulerPort


class StopPowerSupplyMonitoring:
    def __call__(self, scheduler: SchedulerPort):
        if scheduler:
            logger.info("Stopping power supply monitoring")
            scheduler.stop_polling()