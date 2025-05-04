# E-scooter system for TTM4115

The system is built using the component-philosophy, where the application consists of several independent main-modules. On the high-level aspect, the system consists of the following components: 
* __Back-end__: Python based.
  * _HTTP_: Implements a REST API for communication with the front-end.
  * _MQTT_: Communicates with the e-scooter through a publish-subscribe messaging pattern.
  * _MySQL_: Stores data about users, rentals, and e-scooters on an external MySQL/MariaDB database server.
  * _Services_: Implements several service-classes acting as interfaces between API endpoints and logic.
  * _Logic_: Implements standalone sub-modules for specific functions such as price calculations and weather updates from the MET API.
* __Front-end__: React/TypeScript.
  * _HTTP_ : Communicates with the back-end through the REST API implementation.
* __E-scooter__: Python based.
  * _MQTT_: Communicates with the back-end through MQTT.
  * _State Machines_: Implements state machines for temperature measurement and crash detection.
  * _Controllers_: Interfaces for controlling the scooter in general and Sense HAT.
* __Mosquitto__: MQTT broker.
* __Nginx__: Web server.
