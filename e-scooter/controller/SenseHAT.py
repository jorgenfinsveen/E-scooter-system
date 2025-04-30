import logging
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
from threading import Thread




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

    def checkTemperature(self):
        try:
            while self._readTemperature:
                temperature = self.sense_hat.get_temperature()
                self._logger.debug(f"Temperatur: {temperature:.2f}°C")
                if temperature < 2:
                    self._logger.debug("Temperature is below 2°C. ")
                    self.controller.sendTemperature()
                    self.lock_escooter()

                    break
                if self.first_login:
                    self.unlock_escooter()
                    self.first_login = False
                time.sleep(3) 
        except KeyboardInterrupt:
            self._logger.debug("Avslutter temperaturkontroll")

    def sos(self):
        for i in range(3):
            self.sense_hat.show_message("SOS", scroll_speed=0.1, text_colour=[255, 0, 0], back_colour=[0, 0, 0])

    def stop_sos(self):
        for i in range(2):
            self.sense_hat.show_message("SAFE", scroll_speed=0.1, text_colour=[0,255,0], back_colour = [0,0,0])

    def unlock_escooter(self):
        self.sense_hat.show_message("UNLOCK", scroll_speed=0.1, text_colour=[0, 255, 0], back_colour=[0, 0, 0])  
        self._readTemperature = True
        self.temperature_thread = Thread(target=self.checkTemperature)
        self.temperature_thread.start()

    def lock_escooter(self):
        self.sense_hat.show_message("LOCK", scroll_speed=0.1, text_colour=[255, 0, 0], back_colour=[0, 0, 0])
        self._readTemperature = False
        self.temperature_thread.join()
    
  
"""   
    def ambulance(self):
        for _ in range(5):
            self.sense_hat.set_pixels(255, 0, 0)
            time.sleep(0.01)
            self.sense_hat.set_pixels(0,0,0)
            time.sleep(0.01) 
"""