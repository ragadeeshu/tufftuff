import hardware
import os
# import connections
from threading import Thread
from threading import Event
from threading import Lock
import time
class CommandQueue:
    def __init__(self, clients):
        self._hardware = hardware.DummyHardware();
        self._clients = clients
        self._command_list = []
        self._event = Event()
        self._hardware_change_applier = Thread(target=self.do_next, args=())
        self._hardware_change_applier.start()
        self.lock = Lock()

        self._hardware.set_logical_state({'type':'switch', 'id':'1', 'value':'straight'})
        self.queue({'type':'switch', 'id':'1', 'value':'straight'})

    def queue(self, command):
        self.lock.acquire()
        try:
            self._command_list.append(command)
            self._hardware.set_logical_state(command)
            self._event.set()
        finally:
            self.lock.release()
        self._clients.message_clients(self._hardware.get_logical_state())


    def do_next(self):
        while True:
            self._event.wait()
            self._event.clear()
            self.lock.acquire()
            try:
                while self._command_list:
                    self._hardware.set_physical_state(self._command_list[0])
                    del(self._command_list[0])
            finally:
                self.lock.release()

    def get_state(self):
        return self._hardware.get_logical_state()
