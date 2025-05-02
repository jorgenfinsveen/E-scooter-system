# E-scooter system

__Project details__:
* Course: [TTM4115 - Design of Communicating Systems](https://www.ntnu.edu/studies/courses/TTM4115#tab=omEmnet)
* Location: [Norwegian University of Science and Technology](https://www.ntnu.edu) (Trondheim)
* Term: Spring 2025

__Authors__: 
* [Iqra Arshad](https://github.com/iqrarars)
* [Fabrice Baricako](https://github.com/Fabrice-bar)
* [Jørgen Finsveen](https://github.com/jorgenfinsveen)
* [Vebjørn Langsæter](https://github.com/0Propan)
* [Magnus Olsen](https://github.com/MagnusAOlsen)

## Table of Contents

- [Architecture](#architecture)
  - [Database](#database)
- [Communication](#communication)
  - [MQTT](#mqtt)
    - [Requesting an Unlock/Lock Request](#requesting-an-unlocklock-request)
    - [Responding to an Unlock/Lock Request](#responding-to-an-unlocklock-request)
    - [Aborting a Session Upon Low Temperature or Crash](#aborting-a-session-upon-low-temperature-or-crash)
- [Components](#components)
  - [Back-end](#back-end)
  - [Front-end](#front-end)
  - [E-scooter](#e-scooter)
  - [Docker, Mosquitto, and Nginx](#docker-mosquitto-and-nginx)
- [E-scooter Status Codes](#e-scooter-status-codes)
- [State Machines](#state-machines)
  - [WeatherLock](#weatherlock)
  - [CrashDetection](#crashdetection)
- [AI Declaration](#ai-declatation)



## Architecture
The system is built using the component-philosophy, where the application consists of several independent main-modules. On the high-level aspect, the system consists of the following components: 
* [__Back-end__](/backend): Python based.
  * _HTTP_: Implements a REST API for communication with the front-end.
  * _MQTT_: Communicates with the e-scooter through a publish-subscribe messaging pattern.
  * _MySQL_: Stores data about users, rentals, and e-scooters on an external MySQL/MariaDB database server.
  * _Services_: Implements several service-classes acting as interfaces between API endpoints and logic.
  * _Logic_: Implements standalone sub-modules for specific functions such as price calculations and weather updates from the MET API.
* [__Front-end__](/frontend): React/TypeScript.
  * _HTTP_ : Communicates with the back-end through the REST API implementation.
* [__E-scooter__](escooter): Python based.
  * _MQTT_: Communicates with the back-end through MQTT.
  * _State Machines_: Implements state machines for temperature measurement and crash detection.
  * _Controllers_: Interfaces for controlling the scooter in general and Sense HAT.
* [__Mosquitto__](https://mosquitto.org): MQTT broker.
* [__Nginx__](https://nginx.org): Web server.

All components are deployed in containers as specified in [docker-compose.yaml](/docker-compose.yaml), where the containers are mounted following the [Dockerfile](/backend/Dockerfile). The containers were deployed on a Raspberry Pi Compute Module 5, while the e-scooter software was deployed on a separate Raspberry Pi 4 equipped with a Sense HAT.

### Database
The system stores data a MariaDB/MySQL database issued from an external service provider, [Loopia](https://www.loopia.no). Please refer to the [database schema](/docs/database-schema.png) for details regarding the design.

## Communication
The system, being a communicative system, utilizes MQTT and  REST API (HTTP) for communication between components:

### MQTT
The MQTT broker was deployed as its own container, using [Mosquitto](https://mosquitto.org). MQTT was utilized to establish communication between the back-end and the e-scooter, where the publish-subscribe pattern were ideal for our use-cases, and a popular choice for IoT.

#### Requesting an unlock/lock request
Upon a front-end request to unlock/lock an e-scooter, the back-end sends a JSON-encoded message on the topic ```escooter/command/[scooter_id]```. The payload is as follows:
```py
{
    "id": 1,                    # Server ID             (int)
    "uuid": 2,                  # Scooter ID            (int)
    "command": "unlock",        # Command [lock|unlock] (bool)
    "coride": False,            # Coride [True|False]   (str)
    "num_coriders": 0,          # Number of coriders    (int)
    "coriders": [],             # Coriders              (list)
    "timestamp": time.time()    # Timestamp             (time)
}
```

#### Responding to an unlock/lock request
When an e-scooter receives an unlock/lock request, it responds with a JSON-encoded message on the topic ```escooter/response/#``` given that the requirements are satisfied. The payload is as follows:
```py
{
    "id": 1,                    # Server ID             (int)
    "uuid": 2,                  # Scooter ID            (int)
    "battery": 100,             # Battery               (int)
    "status": 0,                # Status                (int)
    "abort": False              # Abort                 (bool)
    "timestamp": time.time(),   # Timestamp             (time)
    "location": {
        "latitude":  63.4197,       # Latitude  (float)
        "longitude": 10.4018        # Longitude (float)
    }
}
```

#### Aborting a session upon low temperature or crash
Upon a situation where the e-scooter needs to terminate an active session, it will send the following payload to the back-end over MQTT at the ```escooter/response/#``` topic:
```py
{
    "id": 1,                    # Server ID             (int)
    "uuid": 2,                  # Scooter ID            (int)
    "battery": 100,             # Battery               (int)
    "status": 4,                # Status                (int)
    "abort": True               # Abort                 (bool)
    "timestamp": time.time(),   # Timestamp             (time)
    "location": {
        "latitude":  63.4197,       # Latitude  (float)
        "longitude": 10.4018        # Longitude (float)
    }
}
```
__Situations where the e-scooter will terminate an active session__:
1. If the [WeatherLock](/escooter/stm/WeatherLock.py] state machine receives the trigger ```temperature_invalid``` when in the state ```awaiting-weather-report```, the escooter is locked, and the status int is set to ```2```.
2. If the [CrashDetection](/escooter/stm/CrashDetection.py) state machine receives the trigger ```t```when in the state ```crash_detected```, the escooter is locked, and the status in is set to ```4```.

## Components
The system is built using the component-philosophy, where the application consists of several independent modules:
### Back-end
The back-end is written in Python and is organized into several layers, which can be represented as follows:
* [__api__](/backend/app/api):
  * _database.py_
  * _http.py_
  * _mqtt.py_ 
* [__service__](/backend/app/service):
  * _single_ride_service.py_
  * _multi_ride_service.py_
  * _internal_service.py_ 
* [__logic__](/backend/app/logic):
  * _transaction.py_
  * _weather.py_
* [__tools__](/backend/app/tools):
  * _singleton.py_

It follows a very modular-based design, where all control-flows starts at either _http.py_ upon a REST API request from a user who wishes to unlock or lock an e-scooter, or _mqtt.py_ upon an MQTT alert from the e-scooter aborting an active session. Upon such events, the request is processed by the respective service-implementations, where _single_ride_service.py_ is responsible for locking/unlocking a single e-scooter upon a request from front-end, _multi_ride_service.py_ upon a co-riding request, and _internal_service.py_ upon an abort session instruction from the e-scooter. The logic-component is mainly used by _single_ride_service.py_ in order to check the weather using the [MET API](https://developer.yr.no), and calculating price of rentals. The tool-catalogue contains _singleton.py_, which implements an annotation which can be used to annotate classes, effectively making them follow the [singleton](https://refactoring.guru/design-patterns/singleton) design pattern. This was used on all service interfaces, as well as the database- and MQTT-client. The file _database.py_ contains an interface to the database.


### Front-end
The front-end is written in TypeScript using the React.js framework. It consists of the following:
* [__comopnents__](/frontend/app/src/components)
  * _CoRideButton.tsx_
  * _Image.tsx_
  * _Location.tsx_
  * _LockButton.tsx_
  * _UnlockButton.tsx_
  * _UserIdInput.tsx_
* [__pages__](/frontend/app/src/pages)
  * [__abort__](/frontend/app/src/pages/abort)
    * _EmergencyAbort.tsx_
    * _WeatherAbort.tsx_
  * _AbortPage.tsx_
  * _ActiveRental.tsx_
  * _ErrorPage.tsx_
  * _InactiveRental.tsx_
  * _RentScooter.tsx_

The __pages__-catalogue contains the different pages the front-end consists of, where the primary chain-of-view is ```RentScooter -> ActiveRental -> InactiveRental```. Failing to unlock an e-scooter would direct the user from _RentScooter.tsx_ to _ErrorPage.tsx_, whereas a premature session termination would direct the user from _ActiveRental.tsx_ to _AbortPage.tsx_, which again displays _EmergencyAbort.tsx_ or _WeatherAbort.tsx_ depending on the cause of the termination. The front-end will almost immediately redirect the user to an abort-page upon a session termination. This was done by having the front-end continuosly check with the back-end wether the rental is still active, where the back-end responds with a redirect upon a session termination, otherwise an empty response. The __comopnents__ contains smaller components which are displayed in the UI, such as buttons, input-fields, images, and interactive maps.


### E-scooter
The e-scooter is written in Python, and deployed on a Raspberry Pi 4 equipped with a Sense HAT. The component consists of the following:
* [__api__](/e-scooter/api)
  * _mqtt.py_
* [__controller__](/e-scooter/controller)
  * _MainController.py_
  * _SenseHAT.py_ 
* [__stm__](/e-scooter/stm)
  * _CrashDetection.py_
  * _WeatherLock.py_
  * _Driver.py_ 
* [__tools__](/e-scooter/tools)
  * _initializer.py_
  * _singleton.py_

The __api__-catalogue contains the MQTT-client which is used to communicate with the back-end. One may find the controllers in __controller__, where _MainController.py_ has the responsibility of the entire e-scooter, while _SenseHAT.py_ represents an interface to the Sense HAT. Furthermore, the __stm__-catalogue contains the two state machines which ensures that a session terminates upon low temperatures or a crash, as well as a driver-class to contain the state machines. Latsly, the __tools__-catalogue contains a [singleton](https://refactoring.guru/design-patterns/singleton) annotation, which was used to annotate the controllers and the MQTT-client as singletons, and _initializer.py_, which is used to initialize and restart the driver containing the state machines.


### Docker, Mosquitto, and Nginx
The last components, Mosquitto and Nginx are not comprised of software that the group has developed themselves, but rather open-source tools for hosting an MQTT broker and a web server. Both are deployed in separate containers through Docker.
* Mosquitto setup -> [docker/mosquitto](/docker/mosquitto)
* Nginx setup -> [docker/nginx](/docker/nginx)


## E-scooter status codes
The e-scooter uses a status-code which is used to represent the state of the e-scooter. The protocol is established through the e-scooter software, the back-end, and the database. The status codes are as follows:

| __Code__ | __Description__  | __Redirect-endpoint__  |
|------|----------------------|--------------------|
| 0    | ok                   |                    |
| 1    | battery low          | low-battery        |
| 2    | bad weather          | bad-weather        |
| 3    | crash sensor error   | scooter-inoperable |
| 4    | distress             | emergency          |
| 5    | weather sensor error | scooter-inoperable |
| 6    | gps error            | scooter-inoperable |
| 7    | operational error    | scooter-inoperable |
| 8    | battery error        | scooter-inoperable |
| 9    | invalid parking      | invalid-parking    |
| 10   | charging             | charging           |
| 11   | unlocked             | scooter-occupied   |

The status codes has been written down in JSON-format in the back-end, and can be found [here](/backend/app/resources).

## State machines
The e-scooter software utilizes state machines using the [stmpy](https://falkr.github.io/stmpy/) library in Python. The state machines are implemented in [__CrashDetection.py__](/e-scooter/stm/CrashDetection.py) and [__WeatherLock.py__](/e-scooter/stm/WeatherLock.py). To see an illustration of the state machines, you may find these here: [weather_lock.png](/docs/weather_lock.png), [crash_detection](/docs/crash_detection.png). 

### WeatherLock
The statemachine is implemented in [__CrashDetection.py__](/e-scooter/stm/CrashDetection.py), and illustrated in [weather_lock.png](/docs/weather_lock.png). A brief description of states, transitions, triggers, and effects:

| Source state            | Target state            | Trigger                      | Effect                                          |
|-------------------------|-------------------------|------------------------------|-------------------------------------------------|
| initial                 | idle                    |                              | start timer "t": 3 seconds                      |
| idle                    | awaiting-weather-report | timer "t"                    | get temperature from Sense HAT                  |
| awaiting-weather-report | idle                    | temperature >= 2 deg Celsius | start timer "t": 3 seconds                      |
| awaiting-weather-report | locked                  | temperature < 2 deg Celsius  | lock scooter, send alert to back-end (status=2) |

### CrashDetection 
The statemachine is implemented in [__WeatherLock.py__](/e-scooter/stm/WeatherLock.py), and illustrated in [crash_detection.png](/docs/crash_detection.png). A brief description of states, transitions, triggers, and effects:
| Source state   | Target state   | Trigger                                | Effect                                           |
|----------------|----------------|----------------------------------------|--------------------------------------------------|
| initial        | standby        |                                        |                                                  |
| standby        | crash-detected | crash (SenseHAT joystick pressed once) | start timer "t": 10 seconds, display SOS message |
| crash-detected | standby        | safe (SenseHAT joystick pressed twice) | stop timer "t", display SAFE message             |
| crash-detected | distress       | timer "t"                              | lock scooter, send alert to back-end (status=4)  |


## AI declatation
Generative AI has been used for some aspects of the project. This includes comment generation, debugging, and code generation og the singleton annotation. The models used is primarily OpenAI's ChatGPT 4o. The group would like to emphasize that GenAI has not been used to generate functional parts of the software, and that the ideas and design choices are based on the intuition of the authors, not GenAI. For writing the vision document and system specification, OpenAI's ChatGPT 4o has been used to fix LaTeX-related syntax errors, not text-generation. AI have been used to some extent for spell-checking. No images has been produced using GenAI.
