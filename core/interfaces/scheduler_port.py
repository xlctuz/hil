from abc import ABC, abstractmethod
from typing import Callable, Any


class SchedulerPort(ABC):
    """Port interface for scheduling tasks"""
    
    @abstractmethod
    def start_polling(self, interval: float, callback: Callable[[], Any]):
        """Start polling at the specified interval (in seconds)"""
        pass
    
    @abstractmethod
    def stop_polling(self):
        """Stop the polling"""
        pass