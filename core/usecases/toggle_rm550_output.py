from core.interfaces.rm550_port import RM550Port

class ToggleRM550OutputUseCase:
    def __init__(self, rm550_adapter: RM550Port):
        self.rm550_adapter = rm550_adapter

    def execute(self, is_enabled: bool):
        if is_enabled:
            return self.rm550_adapter.enable_output()
        else:
            return self.rm550_adapter.disable_output()
