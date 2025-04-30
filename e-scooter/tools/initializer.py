import logging
from stmpy import Machine
from stm.Driver import ScooterDriver
from tools.singleton import singleton
from stm.WeatherLock import WeatherLock, getWeatherTransitions
from stm.CrashDetection import CrashDetection, getCrashTransitions

@singleton
class Initializer:

    def __init__(self, main_controller):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Initializer: __init__")
        self.main_controller = main_controller

    def init_driver(self):
        driver = ScooterDriver()
        weather_lock   = WeatherLock()
        crash_detector = CrashDetection()
        weather_lock_stm   = Machine(transitions=getWeatherTransitions(), obj=weather_lock,   name='weather_lock')
        crash_detector_stm = Machine(transitions=getCrashTransitions(),   obj=crash_detector, name='crash_detector')
        weather_lock.stm   = weather_lock_stm
        crash_detector.stm = crash_detector_stm
        driver.add_machine(weather_lock_stm)
        driver.add_machine(crash_detector_stm)

        self.main_controller.setDriver(driver)
