import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, Request, Query
from app.service import single_ride_service, multi_ride_service

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"

TEST_COORDINATES = (63.41947, 10.40174)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_app():
    """
    Returns the FastAPI app instance.
    This function is used to get the app instance in other modules.
    """
    return app



def set_mqtt_client(mqtt_client : object) -> None:
    """
    Set the MQTT client for the app.
    The MQTT client is stored in the app-state.
    """
    app.state.mqtt_client = mqtt_client



def set_db_client(db_client : object) -> None:
    """
    Set the db client for the app.
    The db client is stored in the app-state.
    """
    app.state.db_client = db_client



def set_single_ride_service() -> None:
    """
    Set the single ride service for the app.
    The single ride service is stored in the app-state.
    """
    app.state.single_ride_service = single_ride_service.single_ride_service()



def set_multi_ride_service() -> None:
    """
    Set the multi ride service for the app.
    The multi ride service is stored in the app-state.
    """
    app.state.multi_ride_service = multi_ride_service.multi_ride_service()



@app.on_event("startup")
def startup_event():
    set_single_ride_service()
    set_multi_ride_service()


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    Returns:
        dict: A dictionary containing a message: <code>"Hello from backend!"</code>.
    """
    logger.debug("Request: HTTP GET /")
    return {"message": "Hello from backend!"}



@app.get("/robots.txt", include_in_schema=False)
def robots_txt():
    """
    Robots.txt endpoint for the API.
    Creates a robots.txt file for the API, making it easier to see what endpoints are available.
    This is useful for debugging and development purposes.
    The robots.txt file is not intended for production use. Will return HTTP 401 Forbidden 
    if app is deployed in prod.

    Returns:
        Response:
        ``` 
        DEVELOPMENT_MODE == 'TEST' 
        curl -X GET http://localhost:8000/robots.txt -> 200 # OK: Returns robots.txt content.
        
        DEVELOPMENT_MODE == 'PROD'
        curl -X GET http://localhost:8000/robots.txt -> 401 # Forbidden: Returns nothing.
        ```
    """
    if DEPLOYMENT_MODE == 'PROD':
        return Response(status_code=401)
    lines = [
        "User-agent: *",
    ]
    arr = ["/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect"]

    for route in app.routes:
        if hasattr(route, "path") and not route.path.startswith("/robots.txt") and route.path not in arr:
            lines.append(f"Endpoint: {route.path}")

    return Response("\n".join(lines), media_type="text/plain")



@app.post("/scooter/{uuid}/single-unlock")
async def scooter_unlock_single(
    uuid: str, 
    request: Request,
    user_id: str = Query(..., description="ID of the user trying to unlock the scooter")
):
    """
    Unlock a scooter with the given UUID.
    This endpoint is used to unlock a scooter for a single user.
    Args:
        uuid (str): UUID of the scooter to unlock.
        request (Request): FastAPI request object.
        user_id (str): ID of the user trying to unlock the scooter. (Query parameter)
    Returns:
        dict: A dictionary containing a message indicating the result of the unlock operation.

    Example:
        ```
        curl -X POST http://localhost:8000/scooter/1234/single-unlock -> "unlock successful"
        curl -X POST http://localhost:8000/scooter/1235/single-unlock -> "battery too low"
        ```
    """
    logger.debug("Request: HTTP POST /scooter/{uuid}/single-unlock?user_id={user_id}")
    if True:
        resp = request.app.state.single_ride_service.unlock_scooter(uuid, user_id)

        if not resp[0]:
            logger.warning(f"Single scooter unlock failed:")
            logger.warning(f"\tscooter-id: \t{uuid}")
            logger.warning(f"\tresponse: \t{resp[1]}")
        return {"message": resp[1]}
    else:
        if DISABLE_MQTT:
            return {"message": f"TEST: scooter_unlock_single({uuid})"}



@app.post("/scooter/{uuid}/single-lock")
async def scooter_lock_single(
    uuid: str, 
    request: Request,
    user_id: str = Query(..., description="ID of the user trying to unlock the scooter")
):
    """
    Lock a scooter with the given UUID.
    This endpoint is used to lock a scooter for a single user.
    Args:
        uuid (str): UUID of the scooter to lock.
        request (Request): FastAPI request object.
        user_id (str): ID of the user trying to unlock the scooter. (Query parameter)
    Returns:
        dict: A dictionary containing a message indicating the result of the lock operation.
    Example:
        ```
        curl -X POST http://localhost:8000/scooter/1234/single-lock -> "lock successful"
        curl -X POST http://localhost:8000/scooter/1235/single-lock -> "invalid parking location"
        ```
    """
    logger.debug("Request: HTTP POST /scooter/{uuid}/single-lock?user_id={user_id}")
    if True:
        resp = request.app.state.single_ride_service.lock_scooter(uuid, user_id)

        if not resp[0]:
            logger.warning(f"Single scooter lock failed:")
            logger.warning(f"\tscooter-id: \t{uuid}")
            logger.warning(f"\tresponse: \t{resp[1]}")
        return {"message": resp[1]}
    else:
        if DISABLE_MQTT:
            return {"message": f"TEST: scooter_ulock_single({uuid})"}



@app.get("/test-weather")
async def test_weather():
    """
    This endpoint is used to test the weather API.
    Returns:
        dict: A dictionary containing a message indicating the result of the weather API test.
    Example:
        ```
        curl -X GET http://localhost:8000/test-weather -> 
            "acceptable conditions <br/> temperature: 11.0 <br/> humidity: 72.4"

        curl -X GET http://localhost:8000/test-weather ->  
            "insufficient conditions <br/> temperature: -2.5 <br/> humidity: 38.1"
        ```
    """
    resp = weather.is_weather_ok(TEST_COORDINATES[0], TEST_COORDINATES[1])
    return {"message": resp[1]}
