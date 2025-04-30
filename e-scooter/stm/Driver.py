import logging
from stmpy import Machine, Driver


class Driver:
    """
    Dette er en driver
    
    """
    def __init__(self):
        self.machines = []
        self._logger = logging.getLogger(__name__)

    def add_machine(self, machine):
        self.machines.append(machine)

    def start(self):
        for machine in self.machines:
            machine.start()

    def stop(self):
        for machine in self.machines:
            machine.stop()

    def send(self, message, state_machine):
        self._logger.debug(f"{state_machine}: {message}")