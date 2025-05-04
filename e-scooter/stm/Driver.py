import logging
from stmpy import Driver


class ScooterDriver:
    """
    Dette er en driver
    
    """
    def __init__(self):
        self.machines = []
        self._logger = logging.getLogger(__name__)
        self._driver = Driver()

    def add_machine(self, machine):
        self.machines.append(machine)
        self._driver.add_machine(machine)

    def start(self):
        self._driver.start()

    def stop(self):
        self._driver.stop()

    def send(self, message, state_machine):
        self._logger.debug(f"{state_machine}: {message}")
        self._driver.send(message, state_machine)