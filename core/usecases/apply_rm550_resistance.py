from core.interfaces.rm550_port import RM550Port

class ApplyRM550ResistanceUseCase:
    def __init__(self, rm550_adapter: RM550Port):
        self.rm550_adapter = rm550_adapter

    def execute(self, resistance: float):
        return self.rm550_adapter.set_resistance(resistance)
