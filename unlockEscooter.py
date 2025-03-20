from stmpy import Machine, Driver


class UnlockEscooter:
    def __init__(self):
        self.stm = None


    def unlock(self):
        self.stm.send('unlock')

    def lock(self):
        self.stm.send('lock')

    def message(self, msg):
        print(f"Message: {msg}")


t0 = {
    'source': 'initial',
    'target': 'locked'
}

t1 = {
    'trigger': 'bad_conditions',
    'source': 'locked',
    'target': 'locked',
}

t2 = {
    'trigger': 'unlock',
    'source': 'locked',
    'target': 'unlocked',
    'effect': 'unlock()'
}

t3 = {
    'trigger': 'bad_conditions',
    'source': 'unlocked',
    'target': 'locked',
    'effect': 'message("bad conditions"); lock()'
}

escooter = UnlockEscooter()
machine = Machine(name="escooter", transitions=[t0, t1, t2], obj=escooter)
escooter.stm = machine


driver = Driver()
driver.add_machine(machine)
driver.start()