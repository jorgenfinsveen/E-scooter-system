import logging
from stmpy import Driver


class ScooterDriver:
    """
    The ScooterDriver class manages the state machines for the scooter.
    It initializes the driver and adds state machines to it.
    """
    def __init__(self):
        self.machines = []
        self._logger = logging.getLogger(__name__)
        self._driver = Driver()

    def add_machine(self, machine):
        """
        Add a state machine to the driver.
        """
        self.machines.append(machine)
        self._driver.add_machine(machine)

    def start(self):
        """
        Start the driver.
        """
        self._driver.start()

    def stop(self):
        """
        Stop the driver.
        """
        self._driver.stop()

    def send(self, message, state_machine):
        """
        Send a message to the specified state machine.
        """
        self._logger.debug(f"{state_machine}: {message}")
        self._driver.send(message, state_machine)