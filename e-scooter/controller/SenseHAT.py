from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
from threading import Thread




class SenseHAT:

    def __init__(self):
        self.sense_hat = SenseHat()
        self.controller = None

        self.input_thread = Thread(target=self.readEvent)
        self.input_thread.start()

    def set_controller(self, controller):
        self.controller = controller

    def getTemperature(self):
        return self.sense_hat.getTemperature()
    
    def readEvent(self):
        try:
            while True:
                for event in self.sense_hat.stick.get_events():
                    print(f"Retning: {event.direction}, Handling: {event.action}")
                    self.controller.newInputEvent(event)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Avslutter")
            self.sense_hat.clear()

    def sos(self):
        self.sense_hat.show_message("SOS", scroll_speed=0.05, text_colour=[255, 0, 0], back_colour=[0, 0, 0])
