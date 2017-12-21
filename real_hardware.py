import pigpio
from hardware import DummyHardware
from time import sleep
from subprocess import Popen, PIPE, STDOUT

class RealHardware(DummyHardware):
    pi = pigpio.pi()
    switch_pin = {'1':26, '2':16, '3':6, '4':5}
    switch_position = {'1':{'straight':1175, 'curve':1975}, '2':{'straight':1975, 'curve':1175}, '3':{'straight':1175, 'curve':1975}, '4':{'straight':1975, 'curve':1175}}

    def set_switch_state(self, command):
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], RealHardware.switch_position[command['id']][command['value']])
        sleep(0.1)
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], 0)

    def set_throttle_state(self, command):
        speed = command['value']
        if speed > 0:
            self._dccpi.stdin.write(b'direction tuff forward\n')
            self._dccpi.stdin.flush()
        elif speed < 0:
            speed = -speed
            self._dccpi.stdin.write(b'direction tuff backward\n')
            self._dccpi.stdin.flush()
        self._dccpi.stdin.write(bytes('speed tuff ' + str(speed) + '\n', 'utf-8'))
        self._dccpi.stdin.flush()

    def set_lights_state(self, command):
        self._dccpi.stdin.write(bytes('fl tuff ' + command['value'] + '\n', 'utf-8'))

    def __init__(self):
        super().__init__()
        self._command_functions = {
        'switch' : self.set_switch_state,
        'throttle' : self.set_throttle_state,
        'lights' : self.set_lights_state
        }
        outfile = open('dccpioutput', "w")
        self._dccpi = Popen(['dccpi'], stdin=PIPE, stdout=outfile)
        self._dccpi.stdin.write(b'register tuff 6\n') #TODO real address is not 6
        self._dccpi.stdin.flush()
        self._dccpi.stdin.write(b'power on\n')
        self._dccpi.stdin.flush()


    def set_physical_state(self, command):
        self._command_functions.get(command['type'], super().set_physical_state)(command)
