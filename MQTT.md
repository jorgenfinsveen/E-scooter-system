# Run MQTT

## Public deployment

### Mosquitto config - MacOS
```sh
sudo nano /opt/homebrew/etc/mosquitto/mosquitto.conf

# Paste these lines:
listener 1883
allow_anonymous true
```


### MacOS 
```sh
# Start MQTT server
mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf

# Get IP address
ipconfig getifaddr en0
```

### Docker
```sh
docker run -d \
  --name mosquitto \
  -p 1883:1883 \
  -v "$(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf" \
  eclipse-mosquitto
```

### Publish
```sh
mosquitto_pub -h <ip-address> -t test/topic -m "hello"
```

## Local deployment
```sh
mosquitto -v
```