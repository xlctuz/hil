from core.interfaces.scheduler_port import SchedulerPort
from PySide6.QtCore import QTimer, QObject, Signal, Slot


class QtSchedulerAdapter(SchedulerPort):
    """Qt-based scheduler adapter that emits a signal at specified intervals"""
    
    def __init__(self):
        self._timer = None
        self._is_running = False
        self._callback = None
        
    def start_polling(self, interval: float, callback: callable):
        """Start polling at the specified interval (in seconds)"""
        self._callback = callback
        
        # Create and configure the timer
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_timeout)
        self._timer.setInterval(int(interval * 1000))  # Convert to milliseconds
        self._timer.start()
        
        self._is_running = True
    
    def stop_polling(self):
        """Stop the polling"""
        if self._timer and self._is_running:
            self._timer.stop()
            self._timer = None
            self._is_running = False
    
    @Slot()
    def _on_timeout(self):
        """Call the callback when the timer interval is reached"""
        if self._callback:
            self._callback()