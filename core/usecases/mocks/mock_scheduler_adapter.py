from core.interfaces.scheduler_port import SchedulerPort
import time
import threading
from typing import Callable, Any


class MockSchedulerAdapter(SchedulerPort):
    """Mock scheduler adapter for testing"""
    
    def __init__(self):
        self._timer = None
        self._is_running = False
        self._interval = 0
        self._callback = None
        
    def start_polling(self, interval: float, callback: Callable[[], Any]):
        """Start polling at the specified interval (in seconds)"""
        self._interval = interval
        self._callback = callback
        self._is_running = True
        
        # Start a thread to run the polling loop
        self._timer = threading.Thread(target=self._polling_loop, daemon=True)
        self._timer.start()
    
    def stop_polling(self):
        """Stop the polling"""
        self._is_running = False
        if self._timer and self._timer.is_alive():
            self._timer.join(timeout=1)  # Wait for up to 1 second for the thread to finish
    
    def _polling_loop(self):
        """The polling loop that runs in a separate thread"""
        while self._is_running:
            time.sleep(self._interval)
            if self._is_running and self._callback:
                self._callback()