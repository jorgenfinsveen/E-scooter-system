import sys
from api.mqtt import MQTTClient
from stm.Driver import Driver
from stm.CrashDetection import CrashDetection, getCrashTransitions
from stm.WeatherLock import WeatherLock, getWeatherTransitions
from stmpy import Machine
from controller.MainController import MainController
from controller.SenseHAT import SenseHAT




if len(sys.argv) < 2:
    print("Please provide a parameter.")
    print("Usage: python3 -m e-scooter <param>")
    exit(1)

param = sys.argv[1]


if __name__ == "__main__":

    main_controller = MainController()

    HOST = "10.22.51.44"
    PORT = 1885

    mqtt_client = MQTTClient(host=HOST, port=PORT, controller=main_controller)

    driver = Driver()

    crash_detector = CrashDetection()
    crash_detector_stm = Machine(transitions=getCrashTransitions(), obj=crash_detector, name='crash_detector')
    crash_detector.stm = crash_detector_stm
    driver.add_machine(crash_detector_stm)


    weather_lock = WeatherLock()
    weather_lock_stm = Machine(transitions=getWeatherTransitions(), obj=weather_lock, name='weather_lock')
    weather_lock.stm = weather_lock_stm
    driver.add_machine(weather_lock_stm)


    senseHat = SenseHAT()
    main_controller.setDriver(driver)
    main_controller.setSense(senseHat)
    senseHat.set_controller(main_controller)




"""
driver = Driver()
driver.add_machine(machine)
driver.start()
"""