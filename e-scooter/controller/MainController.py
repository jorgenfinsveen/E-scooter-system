from api.mqtt import MQTTClient
from controller.SenseHAT import SenseHAT

X = [0,   0, 0]       
R = [255, 0, 0]

arrow_up = [
    X, X, X, R, R, X, X, X,
    X, X, R, R, R, R, X, X,
    X, R, X, R, R, X, R, X,
    R, X, X, R, R, X, X, R,
    X, X, X, R, R, X, X, X,
    X, X, X, R, R, X, X, X,
    X, X, X, R, R, X, X, X,
    X, X, X, R, R, X, X, X
]

arrow_left = [
    X, X, X, X, R, X, X, X,
    X, X, X, R, R, X, X, X,
    X, X, R, X, R, X, X, X,
    X, R, X, X, R, X, X, X,
    X, R, R, R, R, R, R, R,
    X, R, X, X, R, X, X, X,
    X, X, R, X, R, X, X, X,
    X, X, X, R, R, X, X, X
]

arrow_down = arrow_up[::-1] 

arrow_right = [row[::-1] for row in [arrow_left[i:i+8] for i in range(0, 64, 8)]]
arrow_right = [pixel for row in arrow_right for pixel in row]




class MainController:

    def __init__(self):
        self.mqtt_client = MQTTClient()
        self.driver = None
        self.sense_controller = None
        self.middle_pressed_count = 0

    def setDriver(self, driver):
        self.driver = driver

    def setSense(self, controller):
        self.sense_hat = SenseHAT()
        self.sense_controller = controller


    def unlock(self, payload):
        self.driver.start()
        self.sense_hat.unlock_escooter()


    def lock(self, payload):
        self.driver.stop()
        self.sense_hat.lock_escooter()

    def sendTemperature(self):
        self.driver.send("lock", "weather_lock")

    def newInputEvent(self, event):
        self._show_arrow(event.direction)

        if event.action == "pressed":
            if self.middle_pressed_count %2 == 0:
                self.driver.send("crash", 'crash_detector')
                self.middle_pressed_count += 1
                self.sense_hat.sos()
            else:
                self.driver.send("safe", 'crash_detector')
                self.middle_pressed_count += 1
                self.sense_hat.stop_sos()


    def _show_arrow(self, direction):
        if direction == "up":
            self.sense_controller.set_pixels(arrow_up)
        elif direction == "down":
            self.sense_controller.set_pixels(arrow_down)
        elif direction == "left":
            self.sense_controller.set_pixels(arrow_left)
        elif direction == "right":
            self.sense_controller.set_pixels(arrow_right)
