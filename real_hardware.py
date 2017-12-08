from hardware import DummyHardware
from time import sleep
import pigpio

class RealHardware(DummyHardware):
    pi = pigpio.pi()
    switch_pin = {'1':26, '2':16, '3':6, '4':5}
    switch_position = {'1':{'straight':1175, 'curve':1975}, '2':{'straight':1975, 'curve':1175}, '3':{'straight':1175, 'curve':1975}, '4':{'straight':1975, 'curve':1175}}

    def set_switch_state(self, command):
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], RealHardware.switch_position[command['id']][command['value']])
        sleep(0.2)
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], 0)


    def __init__(self):
        super().__init__()
        self._command_functions = {'switch' : self.set_switch_state
        }



    def set_physical_state(self, command):
        self._command_functions.get(command['type'], super().set_physical_state)(command)