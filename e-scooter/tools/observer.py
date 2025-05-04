from tools.singleton import singleton


@singleton
class State:
    """
    The State class implements the observer pattern.
    It allows subjects to subscribe to state changes.
    """
    def __init__(self):
        self.state = "initial"
        self.subscribers = []

    def set(self, state):
        """
        Set the state and notify all subscribers.
        """
        self.state = state
        self._notify()

    def get(self):
        """
        Get the current state.
        """
        return self.state
    
    def subscribe(self, subject):
        """
        Subscribe a subject to state changes.
        """
        self.subscribers.append(subject)

    def _notify(self):
        for subject in self.subscribers:
            subject.notify()