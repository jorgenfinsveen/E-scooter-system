
import time
import logging
from threading import Thread
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED # type: ignore




class SenseHAT:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.sense_hat = SenseHat()
        self.controller = None
        self.first_login = True
        self.input_thread = Thread(target=self.readEvent)     

    def set_controller(self, controller):
        self.controller = controller
        self.input_thread.start()
 
    def readEvent(self):
        try:
            while True:
                for event in self.sense_hat.stick.get_events():
                    self._logger.debug(f"Retning: {event.direction}, Handling: {event.action}")
                    self.controller.newInputEvent(event)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self._logger.debug("Avslutter")
            self.sense_hat.clear()

    def check_temperature(self):
        return self.sense_hat.get_temperature()

    def sos(self):
        for _ in range(3):
            self.sense_hat.show_message("SOS", scroll_speed=0.1, text_colour=[255, 0, 0], back_colour=[0, 0, 0])

    def stop_sos(self):
        for _ in range(1):
            self.sense_hat.show_message("SAFE", scroll_speed=0.1, text_colour=[0,255,0], back_colour=[0,0,0])
        
    def unlock_escooter(self):
        self.sense_hat.show_message("UNLOCK", scroll_speed=0.05, text_colour=[0, 255, 0], back_colour=[0, 0, 0])  

    def lock_escooter(self, pixels=None):
        self.sense_hat.show_message("LOCK", scroll_speed=0.05, text_colour=[255, 0, 0], back_colour=[0, 0, 0]) 
        if pixels is not None:
            self.sense_hat.set_pixels(pixels)

    def set_pixels(self, pixels):
        self.sense_hat.set_pixels(pixels)

    def clear(self):
        self.sense_hat.clear()   
