from stmpy import Machine, Driver


class Driver:
    """
    Dette er en driver
    
    """
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def start(self):
        for machine in self.machines:
            machine.start()

    def stop(self):
        for machine in self.machines:
            machine.stop()
