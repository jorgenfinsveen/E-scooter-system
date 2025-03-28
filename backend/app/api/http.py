import os
from app.logic import weather, transaction
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"

TEST_COORDINATES = (63.41947, 10.40174)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_app():
    return app

def set_mqtt_client(mqtt_client : object) -> None:
    app.state.mqtt_client = mqtt_client

@app.get("/")
async def root():
    if DEPLOYMENT_MODE == 'TEST':
        print(f"Incoming request: /")
    return {"message": "Hello from backend!"}


@app.get("/robots.txt", include_in_schema=False)
def robots_txt():
    lines = [
        "User-agent: *",
    ]
    arr = ["/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect"]

    for route in app.routes:
        if hasattr(route, "path") and not route.path.startswith("/robots.txt") and route.path not in arr:
            lines.append(f"Endpoint: {route.path}")

    return Response("\n".join(lines), media_type="text/plain")


@app.post("/scooter/{uuid}/single-unlock")
async def scooter_unlock_single(uuid: str, request: Request):
    if DEPLOYMENT_MODE == 'PROD':
        mqtt_client = request.app.state.mqtt_client
        resp = mqtt_client.e_scooter_connect_single(uuid)

        status = resp[0]
        msg    = resp[1]

        if status:
            return {"message": "unlock successful"}
        else:
            return {"message": msg}
    else:
        if DISABLE_MQTT:
            print(f"Incoming request: /scooter/{uuid}/single-unlock")
            return {"message": f"TEST: scooter_unlock_single({uuid})"}


@app.post("/scooter/{uuid}/single-lock")
async def scooter_lock_single(uuid: str, request: Request):
    if DEPLOYMENT_MODE == 'PROD':
        mqtt_client = request.app.state.mqtt_client
        resp = mqtt_client.e_scooter_connect_single(uuid)

        status = resp[0]
        msg    = resp[1]

        if status:
            return {"message": "lock successful"}
        else:
            return {"message": msg}
    else:
        if DISABLE_MQTT:
            print(f"Incoming request: /scooter/{uuid}/single-lock")
            return {"message": f"TEST: scooter_ulock_single({uuid})"}


@app.get("/test-weather")
async def test_weather():
    resp = weather.is_weather_ok(TEST_COORDINATES[0], TEST_COORDINATES[1])
    return {"message": resp[1]}
