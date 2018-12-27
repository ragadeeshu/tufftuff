import hardware
import os
from queue import Queue
from multiprocessing import Lock, Queue, Process
import time
class CommandQueue:
    # 1 is outer, 2 is middle and 3 is inner
    loop_commands = {
    '1':[{'type':'switch', 'id':'4', 'value':'straight'}, {'type':'switch', 'id':'1', 'value':'straight'}, {'type':'switch', 'id':'3', 'value':'curve'}, {'type':'switch', 'id':'2', 'value':'straight'}],
    '2':[{'type':'switch', 'id':'4', 'value':'curve'}, {'type':'switch', 'id':'3', 'value':'straight'}, {'type':'switch', 'id':'2', 'value':'straight'}],
    '3':[{'type':'switch', 'id':'4', 'value':'straight'}, {'type':'switch', 'id':'1', 'value':'curve'}, {'type':'switch', 'id':'2', 'value':'curve'}]
    }

    def __init__(self, clients, type):
        if type == 'dummy':
            self._hardware = hardware.DummyHardware();
        else:

            real_hardware = __import__('real_hardware')
            self._hardware = real_hardware.RealHardware();

        self._clients = clients
        self._command_queue =Queue()
        self._hardware_change_applier = Process(target=self.do_next)
        self._hardware_change_applier.start()
        self.lock = Lock()

        self.queue({'type':'switch', 'id':'1', 'value':'straight'})
        self.queue({'type':'switch', 'id':'2', 'value':'straight'})
        self.queue({'type':'switch', 'id':'3', 'value':'straight'})
        self.queue({'type':'switch', 'id':'4', 'value':'straight'})
        self.queue({'type':'loop', 'id':'3', 'value':'off'})
        self.queue({'type':'loop', 'id':'2', 'value':'off'})
        self.queue({'type':'loop', 'id':'1', 'value':'on'})
        self.queue({'type':'throttle', 'id':'1', 'value':0})
        self.queue({'type':'lights', 'id':'1', 'value':'off'})

    def queue(self, command):
        self.lock.acquire()
        try:
            if command['type'] == "switch" or command['type'] == "loop":
                self._hardware.set_logical_state({'type':'loop', 'id':'1', 'value':'off'})
                self._hardware.set_logical_state({'type':'loop', 'id':'2', 'value':'off'})
                self._hardware.set_logical_state({'type':'loop', 'id':'3', 'value':'off'})

            if command['type'] == "loop" and command['value'] == 'on':
                self._hardware.set_logical_state(command)
                for subcommand in CommandQueue.loop_commands[command['id']]:
                    self._command_queue.put(subcommand)

            else:
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
