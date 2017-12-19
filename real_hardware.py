from hardware import DummyHardware
from time import sleep
import pigpio
# from dccpi import *

class RealHardware(DummyHardware):
    pi = pigpio.pi()
    switch_pin = {'1':26, '2':16, '3':6, '4':5}
    switch_position = {'1':{'straight':1175, 'curve':1975}, '2':{'straight':1975, 'curve':1175}, '3':{'straight':1175, 'curve':1975}, '4':{'straight':1975, 'curve':1175}}

    def set_switch_state(self, command):
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], RealHardware.switch_position[command['id']][command['value']])
        sleep(1.1)
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], 0)

    def set_throttle_state(self, command):
        speed = command['value']
        if speed > 0 and self._direction == 0:
            self._direction = 1
            # self._train.reverse()
        elif speed < 0:
            speed = -speed
            if self.direction == 1:
                self._direction = 0
                # self._train.reverse()
        # self._train.speed(speed)

    def set_lights_state(self, command):
        pass
        # self._train.fl(command['value'] == 'on')

    def __init__(self):
        super().__init__()
        self._command_functions = {
        'switch' : self.set_switch_state,
        'throttle' : self.set_throttle_state,
        'lights' : self.set_lights_state
        }
        # e = DCCRPiEncoder()
        # controller = DCCController(e)
        # self._train = DCCLocomotive("train", 6) #TODO real address is not 6
        # self._direction = 1

        # controller.register(self._train)

        # controller.start()


    def set_physical_state(self, command):
        self._command_functions.get(command['type'], super().set_physical_state)(command)
