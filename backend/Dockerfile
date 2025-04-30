FROM node:20 AS frontend-builder

WORKDIR /app
COPY frontend/app/ ./

RUN npm install
RUN npm run build




FROM python:3.11-slim AS backend

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY backend/app/ /app/app
COPY --from=frontend-builder /app/dist /frontend/app/dist

ENV APP_NAME="E-scooter-backend"
ENV APP_VERSION="0.1-SNAPSHOT"
ENV APP_AUTHORS="By students at NTNU, Trondheim, Norway, 2025"

# Alternatives: "PROD", "TEST"
ENV DEPLOYMENT_MODE="PROD"  
ENV DISABLE_MQTT="False"
ENV DISABLE_WEATHER="False"
ENV DISABLE_TRANSACTIONS="False"

# MQTT CONFIG - PROD
ENV MQTT_HOST_PROD="10.22.51.44"
ENV MQTT_PORT_PROD="1885"
ENV MQTT_TOPIC_INPUT_PROD="escooter/response/#"
ENV MQTT_TOPIC_OUTPUT_PROD="escooter/command"

# MQTT CONFIG - TEST
ENV MQTT_HOST_TEST="10.22.51.44"
ENV MQTT_PORT_TEST="1885"
ENV MQTT_TOPIC_INPUT_TEST="escooter/response/#"
ENV MQTT_TOPIC_OUTPUT_TEST="escooter/command"

# HTTP CONFIG - PROD
ENV HTTP_HOST_PROD="127.0.0.1"
ENV HTTP_PORT_PROD="8080"

# HTTP CONFIG - TEST
ENV HTTP_HOST_TEST="127.0.0.1"
ENV HTTP_PORT_TEST="8080"

# WEATHER API CONFIG
ENV WEATHER_API_URL="https://api.met.no/weatherapi/locationforecast/2.0/compact"
ENV WEATHER_API_CONTENT_TYPE="application/json"
ENV WEATHER_API_USER_AGENT="e-scooter-school-project"
ENV WEATHER_API_CONTACT_INFO="jorgen.finsveen@ntnu.no"

# WEATHER CONFIG
ENV WEATHER_TEMPERATURE_THRESHOLD="0"

# TRANSACTION CONFIG
ENV TRANSACTION_COST_UNLOCK="15"
ENV TRANSACTION_COST_PER_MINUTE="5"
ENV TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON="5"

EXPOSE 1883
EXPOSE 8080


CMD ["python", "/app/app/__main__.py"]





FROM nginx:stable AS nginx

COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
