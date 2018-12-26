import hardware
import os
# import connections
from threading import Thread
from queue import Queue
from threading import Lock
import time
class CommandQueue:
    def __init__(self, clients, type):
        if type == 'dummy':
            self._hardware = hardware.DummyHardware();
        else:

            real_hardware = __import__('real_hardware')
            self._hardware = real_hardware.RealHardware();

        self._clients = clients
        self._command_queue =Queue()
        self._hardware_change_applier = Thread(target=self.do_next, args=())
        self._hardware_change_applier.start()
        self.lock = Lock()

        self.queue({'type':'switch', 'id':'1', 'value':'straight'})
        self.queue({'type':'switch', 'id':'2', 'value':'straight'})
        self.queue({'type':'switch', 'id':'3', 'value':'straight'})
        self.queue({'type':'switch', 'id':'4', 'value':'straight'})
        self.queue({'type':'throttle', 'id':'1', 'value':0})
        self.queue({'type':'lights', 'id':'1', 'value':'off'})

    def queue(self, command):
        self.lock.acquire()
        try:
            self._command_queue.put(command)
            self._hardware.set_logical_state(command)
        finally:
            self.lock.release()
        self._clients.message_clients(self._hardware.get_logical_state())


    def do_next(self):
        while True:
            self._hardware.set_physical_state(self._command_queue.get())

    def get_state(self):
        return self._hardware.get_logical_state()
