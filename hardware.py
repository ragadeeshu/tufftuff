class DummyHardware:
    def get_logical_state(self):
        return "DummyHardware says hi!"

class RealHardware(DummyHardware):
    def get_logical_state(self):
        return "RealHardware says hi!"
