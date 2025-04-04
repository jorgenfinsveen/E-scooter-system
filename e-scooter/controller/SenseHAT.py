from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
from threading import Thread




class SenseHAT:

    def __init__(self):
        self.sense_hat = SenseHat()
        self.controller = None

        self.input_thread = Thread(target=self.readEvent)
        
        

    def set_controller(self, controller):
        self.controller = controller
        self.input_thread.start()
        self.temperature_thread = Thread(target=self.checkTemperature)
        self.temperature_thread.start()

    
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

    def checkTemperature(self):
        try:
            while True:
                temperature = self.sense_hat.get_temperature()
                print(f"Temperatur: {temperature:.2f}°C")
                if temperature < 2:
                    print("Temperature is below 2°C. ")
                    self.controller.sendTemperature()
                time.sleep(300) 
        except KeyboardInterrupt:
            print("Avslutter temperaturkontroll")

    def sos(self):
        self.sense_hat.show_message("SOS", scroll_speed=0.05, text_colour=[255, 0, 0], back_colour=[0, 0, 0])

    def stop_sos(self):
        self.sense_hat.show_message("SAFE", scroll_speed=0.05, text_colour=[0,255,0], back_colour = [0,0,0])

    def unlock_escooter(self):
        self.sense_hat.show_message("UNLOCK", scroll_speed=0.05, text_colour=[0, 255, 0], back_colour=[0, 0, 0])

    def lock_escooter(self):
        self.sense_hat.show_message("LOCK", scroll_speed=0.05, text_colour=[255, 0, 0], back_colour=[0, 0, 0])