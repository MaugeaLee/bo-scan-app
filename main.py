from contextlib import asynccontextmanager
from fastapi import FastAPI

from API import routers
from API.REDIS.redis_client import RedisClient
from API.MQTT.mqtt_subscriber import BoMQTTClient
from API.CONFIG.bogger import BoggerDevLogger

logger = BoggerDevLogger(__name__).logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting lifespan")
    mqtt_client = BoMQTTClient(
        broker='localhost',
        port=1883,
    )
    mqtt_client.connect()
    mqtt_client.loop_start()

    redis = RedisClient()
    redis.connect()

    # 앱 상태에 mqtt_client 저장
    app.state.mqtt_client = mqtt_client
    app.state.redis_client = redis

    yield

    mqtt_client.disconnect()
    redis.disconnect()
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "routing FastAPI"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(routers.router, prefix="/api", tags=["api"])
