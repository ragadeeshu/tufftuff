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
        self._commandList = []
        self._event = Event()
        self._hardware_change_applier = Thread(target=self.do_next, args=())
        self._hardware_change_applier.start()
        self.lock = Lock()

    def queue(self, command):
        self.lock.acquire()
        try:
            self._commandList.extend(command)
            self._hardware.set_logical_state(command['type'], command['id'], command['value'])
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
                while(self._commandList):
                    self._hardware.set_physical_state(self._commandList[0])
                    del(self._songlist[0])
            finally:
                self.lock.release()

    def get_state(self):
        return self._hardware.get_logical_state()
