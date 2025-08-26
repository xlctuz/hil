class StopRM550MonitoringUseCase:
    def __init__(self, start_monitoring_use_case):
        self.start_monitoring_use_case = start_monitoring_use_case

    def execute(self):
        self.start_monitoring_use_case.stop()
