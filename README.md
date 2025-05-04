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

- [Installation Guide](#installation-guide)
  - [Full-stack Application](#setting-up-the-full-stack-application)
  - [E-scooter Software](#setting-up-the-e-scooter-software)
- [Architecture](#architecture)
  - [Overview](#overview)
  - [Database](#database)
- [Communication](#communication)
  - [MQTT](#mqtt)
  - [HTTP](#http)
- [Components](#components)
  - [Back-end](#back-end)
  - [Front-end](#front-end)
  - [E-scooter](#e-scooter)
  - [Docker, Mosquitto, and Nginx](#docker-mosquitto-and-nginx)
- [E-scooter Status Codes](#e-scooter-status-codes)
- [State Machines](#state-machines)
  - [WeatherLock](#weatherlock)
  - [CrashDetection](#crashdetection)
- [AI Declaration](#ai-declaration)


## Installation Guide

### Setting up the full-stack application

The full-stack application includes:
* Back-end
* Front-end
* Nginx (Web server)
* Mosquitto (MQTT broker)

#### Cloning the repo
First, you need to clone this repository to the machine which is to run the back-end:
```sh
git clone https://github.com/jorgenfinsveen/E-scooter-system.git
```

#### Installing dependencies
Now, you need to ensure that you have [Docker](https://www.docker.com) and [Docker Compose)[https://docs.docker.com/compose/) installed. It is used for containerization and deployment of the application, and can be installed as follows:

__Windows__:
```powershell
winget install --id Docker.DockerDesktop -e
```

__MacOS__:
```sh
brew install --cask docker
```

__Linux (Ubuntu/Debian)__:
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Now, you will need to install mosquitto and Nginx. You may find the download for your system here:
* Mosquitto: _[downloads](https://mosquitto.org/download/)_
* Nginx: _[downloads](https://nginx.org/en/download.html)_

#### Setting up environment variables
When this is done, you need to insert environment files (.env) at the following locations:
* [backend/app/](/backend/app/)
  * ```.env.prod```
  * ```.env.test```
* [frontend/app/](/frontend/app/)
  * ```.env```
  * ```.env.production```

 This should be the content of the back-end environment files:

 __.env.prod__:
 ```env
DB_NAME=[name of your production database]
DB_HOST=[production database host]
DB_PORT=[port of the production database host]
DB_USER=[production database username]
DB_PASSWORD=[production database password]
```

 __.env.test__:
 ```env
DB_NAME=[name of your test database]
DB_HOST=[test database host]
DB_PORT=[port of the test database host]
DB_USER=[test database username]
DB_PASSWORD=[test database password]
```

This should be the content of the front-end environment files:

__.env__:
```env
VITE_API_URL=/api/v1/
```

__.env.production__:
```env
VITE_API_URL=/api/v1/
```

#### Deploying the application
Now, you may deploy the application by opening a terminal on the location of the root-catalogue of the project and run the following commands:
```sh
docker-compose build # build the containers
docker-compose up -d # deploy the containers. d: detaches the process
docker-compose logs -f #show logs. f: display logs from the containers
```
In order to take the containers down and up, you may run the following commands:
```sh
docker-compose down # take down the containers
docker-compose up -d # deploy the containers
```

The application is now reachable through the front-end at ```http:[ip-of-your-computer]:8080```


### Setting up the e-scooter software

#### Cloning the repo
First, you need to clone this repository to the Raspberry Pi:
```sh
git clone https://github.com/jorgenfinsveen/E-scooter-system.git
```

#### Installing dependencies

Firstly, this software requires that you have equipped the Raspberry Pi with a [Sense HAT](https://www.raspberrypi.com/products/sense-hat/).
The e-scooter application runs in Python, so you need to ensure that you have this installed:
```sh
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```


Now, you need to install Python dependencies for the project. You may install everything you need by opening a terminal on your Raspberry Pi in the root-catalogue of the cloned repo and run the following commands:
```sh
pip install sense-hat
pip install -r requirements.txt
```

#### Running the application
In order to run the application, open a terminal and move to the directory named ```e-scooter```. Run the following command:
```sh
ID=1            # The scooter_id of the scooter that the software should represent.
HOST=127.0.0.1  # The IP-address of the computer that runs the full-stack application.
PORT=1883       # The port of the MQTT broker (1883 by default)

python __main__.py --id="$ID" --host="$HOST" --port="$PORT"
```

After doing this, a red 4x4 square should appear on the SenseHAT.







## Architecture
### Overview

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

<br/><img src="/docs/deployment-diagram.png"/> <br/>

All components are deployed in containers as specified in [docker-compose.yaml](/docker-compose.yaml), where the containers are mounted following the [Dockerfile](/backend/Dockerfile). The containers were deployed on a Raspberry Pi Compute Module 5, while the e-scooter software was deployed on a separate Raspberry Pi 4 equipped with a Sense HAT.

### Database
The system stores data a MariaDB/MySQL database issued from an external service provider, [Loopia](https://www.loopia.no). Please refer to the [database schema](/docs/database-schema.png) for details regarding the design.
<br/><br/> <img src="/docs/database-schema.png"/> <br/>

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
1. If the [WeatherLock](/e-scooter/stm/WeatherLock.py) state machine receives the trigger ```temperature_invalid``` when in the state ```awaiting-weather-report```, the escooter is locked, and the status int is set to ```2```.
2. If the [CrashDetection](/e-scooter/stm/CrashDetection.py) state machine receives the trigger ```t```when in the state ```crash_detected```, the escooter is locked, and the status in is set to ```4```.

### HTTP
The back-end utilizes [FastAPI](https://fastapi.tiangolo.com) in order to set up a REST API, allowing communication between front-end and back-end. This is implemented in [http.py](/backend/app/api/http.py). In order to expose the end-points, you may run the application using the following environment variable:
```dockerfile
# Alternatives: "PROD", "TEST"
ENV DEPLOYMENT_MODE="TEST"
```
This will make it possible to view all available end-points by visiting the following end-point in your browser, Postman, curL, or your preferred API inspection tool:
```url
http:[ip of host]:8080/robots.txt
```
You will then receive a response as follows:
```html
User-agent: *
Endpoint: /static
Endpoint: /assets
Endpoint: /api/v1/
Endpoint: /api/v1/scooter/{uuid}/single-unlock
Endpoint: /api/v1/scooter/{uuid}/single-lock
Endpoint: /api/v1/test-weather
Endpoint: /api/v1/scooter/{uuid}
Endpoint: /api/v1/user/{id}
Endpoint: /api/v1/rental/{rental_id}
Endpoint: /api/v1/rental/ok/{rental_id}
Endpoint: /api/v1/rental
Endpoint: /{full_path:path}
Endpoint: /api/v1/
Endpoint: /api/v1/scooter/{uuid}/single-unlock
Endpoint: /api/v1/scooter/{uuid}/single-lock
Endpoint: /api/v1/test-weather
Endpoint: /api/v1/scooter/{uuid}
Endpoint: /api/v1/user/{id}
Endpoint: /api/v1/rental/{rental_id}
Endpoint: /api/v1/rental/ok/{rental_id}
Endpoint: /api/v1/rental
```


The application consists of the following end-points:

#### GET

| Endpoint                               | Queryparameters                                                       | Description                                                                                                         |
|----------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| /api/v1/                               |                                                                       | Returns {"message": "Hello from backend!"}                                                                          |
| /api/v1/test-weather                   |                                                                       | Returns a string indicating whether the current weather conditions are suitable for riding at the coordinates of Trondheim.     |
| /api/v1/scooter/{```scooter_id```}     | ```scooter_id```: The ID of the scooter to get.                       | Returns the information of a scooter instance.                                                                      |
| /api/v1/user/{```user_id```}           | ```user_id```: The ID of the user to get.                             | Returns the information of a user instance.                                                                         |
| /api/v1/rental/{```rental_id```}       | ```rental_id```: The ID of the rental to get.                         | Returns the information of a rental instance.                                                                       |
| /api/v1/rental?user_id=```{user_id```} | ```user_id```: The ID of the user associated with an active rental.   | Returns the user's active rental session given that it exists.                                                      |
| /api/v1/rental/ok/{```rental_id```}    | ```rental_id```: The ID of the rental to check if still is active.    | Checks whether a rental is still active, and returns redirect end-points based on the status of the rented scooter. |


#### POST

| Endpoint                                                     | Parameter 1                                                                     | Parameter 2                                                | Description                                                                                                             |
|--------------------------------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| /api/v1/scooter/{```scooter_id```}/single-unlock?user_id={```user_id```} | ```scooter_id```: The ID of the scooter to unlock when starting a rental session.     | ```user_id```: The ID of the user which are to rent the scooter. | Starts an active rental session and requests the back-end to instruct the scooter to unlock through MQTT.               |
| /api/v1/scooter/{```scooter_id```}/single-lock?user_id={```user_id```}   | ```scooter_id```: The ID of the scooter to lock when ending an active rental session. | ```user_id```: The ID of the user which are renting the scooter. | Ends an active rental session, process payment, and requests the back-end to instruct the scooter to lock through MQTT. |

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
* [__components__](/frontend/app/src/components)
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

The __pages__-catalogue contains the different pages the front-end consists of, where the primary chain-of-view is ```RentScooter -> ActiveRental -> InactiveRental```. Failing to unlock an e-scooter would direct the user from _RentScooter.tsx_ to _ErrorPage.tsx_, whereas a premature session termination would direct the user from _ActiveRental.tsx_ to _AbortPage.tsx_, which again displays _EmergencyAbort.tsx_ or _WeatherAbort.tsx_ depending on the cause of the termination. The front-end will almost immediately redirect the user to an abort-page upon a session termination. This was done by having the front-end continuously check with the back-end whether the rental is still active, where the back-end responds with a redirect upon a session termination, otherwise an empty response. The __comopnents__ contains smaller components which are displayed in the UI, such as buttons, input-fields, images, and interactive maps.


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

The __api__-catalogue contains the MQTT-client which is used to communicate with the back-end. One may find the controllers in __controller__, where _MainController.py_ has the responsibility of the entire e-scooter, while _SenseHAT.py_ represents an interface to the Sense HAT. Furthermore, the __stm__-catalogue contains the two state machines which ensures that a session terminates upon low temperatures or a crash, as well as a driver-class to contain the state machines. Lastly, the __tools__-catalogue contains a [singleton](https://refactoring.guru/design-patterns/singleton) annotation, which was used to annotate the controllers and the MQTT-client as singletons, and _initializer.py_, which is used to initialize and restart the driver containing the state machines.


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

The status codes are defined in JSON-format in the back-end, and can be found [here](/backend/app/resources).

## State machines
The e-scooter software utilizes state machines using the [stmpy](https://falkr.github.io/stmpy/) library in Python.

### WeatherLock
The statemachine is implemented in [__CrashDetection.py__](/e-scooter/stm/CrashDetection.py), and illustrated in [weather_lock.png](/docs/weather_lock.png). A brief description of states, transitions, triggers, and effects:

| Source state            | Target state            | Trigger                      | Effect                                          |
|-------------------------|-------------------------|------------------------------|-------------------------------------------------|
| initial                 | idle                    |                              | start timer "t": 3 seconds                      |
| idle                    | awaiting-weather-report | timer "t"                    | get temperature from Sense HAT                  |
| awaiting-weather-report | idle                    | temperature >= 2 deg Celsius | start timer "t": 3 seconds                      |
| awaiting-weather-report | locked                  | temperature < 2 deg Celsius  | lock scooter, send alert to back-end (status=2) |

<br/><img src="/docs/weather_lock.png"/> <br/><br/><br/>

### CrashDetection 
The statemachine is implemented in [__WeatherLock.py__](/e-scooter/stm/WeatherLock.py), and illustrated in [crash_detection.png](/docs/crash_detection.png). A brief description of states, transitions, triggers, and effects:
| Source state   | Target state   | Trigger                                | Effect                                           |
|----------------|----------------|----------------------------------------|--------------------------------------------------|
| initial        | standby        |                                        |                                                  |
| standby        | crash-detected | crash (SenseHAT joystick pressed once) | start timer "t": 10 seconds, display SOS message |
| crash-detected | standby        | safe (SenseHAT joystick pressed twice) | stop timer "t", display SAFE message             |
| crash-detected | distress       | timer "t"                              | lock scooter, send alert to back-end (status=4)  |

<br/><img src="/docs/crash_detection.png"/> <br/><br/><br/>

## AI declaration
Generative AI has been used for some aspects of the project. This includes comment generation, debugging, and code generation of the singleton annotation. The models used is primarily OpenAI's ChatGPT 4o. The group would like to emphasize that GenAI has not been used to generate functional parts of the software, and that the ideas and design choices are based on the intuition of the authors, not GenAI. For writing the vision document and system specification, OpenAI's ChatGPT 4o has been used to fix LaTeX-related syntax errors, not text-generation. AI have been used to some extent for spell-checking. No images have been produced using GenAI.
