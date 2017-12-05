class DummyHardware:
    def __init__(self):
        self._state = {}

    def set_logical_state(self, command):
        self._state.setdefault(command['type'],{})[command['id']]=command['value']


    def set_physical_state(self, command):
        print("Dummy is setting physical state")
        print(command)
        print("Dummy state set")

    def get_logical_state(self):
        return "DummyHardware says hi!"

class RealHardware(DummyHardware):
    def get_logical_state(self):
        return "RealHardware says hi!"
