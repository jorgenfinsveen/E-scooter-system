from api.mqtt import MQTTClient
from controller.SenseHAT import SenseHat

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

    def setDriver(self, driver):
        self.driver = driver

    def setSense(self, controller):
        self.sense_controller = controller


    def unlock(self, payload):
        self.driver.start()


    def lock(self, payload):
        self.driver.stop()

    def newInputEvent(self, event):
        self._show_arrow(event.direction)

        if event.directon == "middle":
            self.driver.send("crash", 'crash_detector')


    def _show_arrow(self, direction):
        if direction == "up":
            self.sense_controller.set_pixels(arrow_up)
        elif direction == "down":
            self.sense_controller.set_pixels(arrow_down)
        elif direction == "left":
            self.sense_controller.set_pixels(arrow_left)
        elif direction == "right":
            self.sense_controller.set_pixels(arrow_right)
