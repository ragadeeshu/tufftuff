import pigpio
from hardware import DummyHardware
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Queue, Process

class RealHardware(DummyHardware):
    pi = pigpio.pi()
    switch_pin = {'1':26, '2':16, '3':6, '4':5}
    switch_position = {'1':{'straight':1190, 'curve':1625}, '2':{'straight':1650, 'curve':1270}, '3':{'straight':1160, 'curve':1600}, '4':{'straight':1260, 'curve':880}}

    def set_switch_state(self, command):
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], RealHardware.switch_position[command['id']][command['value']])
        sleep(0.1)
        RealHardware.pi.set_servo_pulsewidth(RealHardware.switch_pin[command['id']], 0)
        sleep(0.1)

    def set_throttle_state(self, command):
        speed = command['value']
        if speed > 0:
            self._dccpi_queue.put(b'direction tuff forward\n')
        elif speed < 0:
            speed = -speed
            self._dccpi_queue.put(b'direction tuff backward\n')
        self._dccpi_queue.put(bytes('speed tuff ' + str(speed) + '\n', 'utf-8'))

    def set_lights_state(self, command):
        self._dccpi_queue.put(bytes('fl tuff ' + command['value'] + '\n', 'utf-8'))

    def do_dccpi(self):
        outfile = open('dccpioutput', "w")
        self._dccpi = Popen(['/home/pi/go/bin/dccpi'], stdin=PIPE, stdout=outfile)
        self._dccpi.stdin.write(b'register tuff 3\n') #Default decoder address is 3
        self._dccpi.stdin.flush()
        self._dccpi.stdin.write(b'power on\n')
        self._dccpi.stdin.flush()
        while True:
            command = self._dccpi_queue.get()
            print(command)
            self._dccpi.stin.write(command)
            self._dccpi.stdin.flush()


    def __init__(self):
        super().__init__()
        self._command_functions = {
        'switch' : self.set_switch_state,
        'throttle' : self.set_throttle_state,
        'lights' : self.set_lights_state
        }
        self._dccpi_queue =Queue()
        self._dccpu_applier = Process(target=self.do_dccpi)
        self._dccpu_applier.start()

    def set_physical_state(self, command):
        self._command_functions.get(command['type'], super().set_physical_state)(command)
