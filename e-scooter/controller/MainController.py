from tools.singleton import singleton


X = [0,   0, 0]
r = [255, 0, 0]
R = [0, 0, 255]
G = [0,   255, 0]

dott_green = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, G, G, X, X, X,
    X, X, X, G, G, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
]

dott_red = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, r, r, X, X, X,
    X, X, X, r, r, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
]

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



@singleton
class MainController:

    def __init__(self, scooter_id: int):
        self.scooter_id = scooter_id
        self.mqtt_client = None
        self.driver = None
        self.sense_controller = None
        self.middle_pressed_count = 0
        self.locked = True
        self._first_unlock = True

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def get_scooter_id(self):
        return self.scooter_id

    def setDriver(self, driver):
        self.driver = driver

    def setSense(self, controller_sense_hat):
        self.controller_sense_hat = controller_sense_hat
        self.controller_sense_hat.set_pixels(dott_red)

    def unlock(self):
        self.controller_sense_hat.set_pixels(dott_green)
        self.locked = False
        if not self._first_unlock:
            from tools.initializer import Initializer
            initializer = Initializer(self)
            initializer.init_driver()
            self._first_unlock = False
        self.driver.start()

    def lock(self):
        self.controller_sense_hat.lock_escooter(dott_red)
        self.locked = True
        self.driver.stop()

    def request_temperature(self):
        temperature = self.controller_sense_hat.check_temperature()
        message = "temperature_valid" if temperature >= 2 else "temperature_invalid"
        self.logger.debug(f"Temperature: {temperature:.2f}°C" - f" {message}")
        self.driver.send(message, "weather_lock")

    def sendTemperature(self):
        self.driver.send("lock", "weather_lock")

    def newInputEvent(self, event):
        if not self._show_arrow(event.direction, event.action):
            self.controller_sense_hat.set_pixels(dott_green)
        if event.action == "pressed" and event.direction == "middle":
            if self.middle_pressed_count %2 == 0:
                self.driver.send("crash", 'crash_detector')
                self.middle_pressed_count += 1
                self.controller_sense_hat.sos()
            else:
                self.driver.send("safe", 'crash_detector')
                self.middle_pressed_count += 1
                self.controller_sense_hat.stop_sos()

    def _show_arrow(self, direction, action):
        if not self.locked and (action == "pressed" or action == "held"):
            if direction == "up":
                self.controller_sense_hat.set_pixels(arrow_up)
                return True
            elif direction == "down":
                self.controller_sense_hat.set_pixels(arrow_down)
                return True
            elif direction == "left":
                self.controller_sense_hat.set_pixels(arrow_left)
                return True
            elif direction == "right":
                self.controller_sense_hat.set_pixels(arrow_right)
                return True
        return False