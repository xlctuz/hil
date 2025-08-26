from core.interfaces.rm550_port import RM550Port
from core.interfaces.scheduler_port import SchedulerPort
from typing import Callable

class StartRM550MonitoringUseCase:
    def __init__(self, rm550_adapter: RM550Port, scheduler: SchedulerPort):
        self.rm550_adapter = rm550_adapter
        self.scheduler = scheduler
        self.timer = None

    def execute(self, on_update: Callable[[float, bool], None]):
        def update_task():
            try:
                resistance = self.rm550_adapter.get_current_resistance()
                is_enabled = self.rm550_adapter.get_output_state()
                on_update(resistance, is_enabled)
            except Exception as e:
                # Handle exceptions, e.g., device disconnected
                print(f"Error during RM550 monitoring: {e}")

        self.timer = self.scheduler.start_polling(1.0, update_task) # Update every 1 second

    def stop(self):
        if self.timer:
            self.scheduler.stop_polling()
            self.timer = None
