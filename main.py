import os
from dotenv import load_dotenv

from contextlib import asynccontextmanager
from fastapi import FastAPI

from API import routers
from API.REDIS.redis_client import RedisClient
from API.MQTT.mqtt_subscriber import BoMQTTClient
from API.CONFIG.bogger import BoggerDevLogger

# __init__setting
logger = BoggerDevLogger(__name__).logger
load_dotenv(dotenv_path='mqtt_secret.env')

# 환경 변수 값 읽기
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

missing_vars = []
if not isinstance(MQTT_BROKER_HOST, str):
    missing_vars.append(MQTT_BROKER_HOST)
if not isinstance(MQTT_BROKER_PORT, str):
    missing_vars.append(MQTT_BROKER_PORT)
if not isinstance(MQTT_USERNAME, str):
    missing_vars.append(MQTT_USERNAME)
if not isinstance(MQTT_PASSWORD, str):
    missing_vars.append(MQTT_PASSWORD)

if missing_vars:
    error_message = f"❌ 서버 초기화 실패: 다음 필수 환경 변수가 누락되었습니다: {', '.join(missing_vars)}"
    logger.error(error_message)
    raise ValueError(error_message)

# 포트 값이 정상이라면 int로 변환
try:
    MQTT_BROKER_PORT = int(MQTT_BROKER_PORT)
except (ValueError, TypeError):
    error_message = f'❌ 서버 초기화 실패: MQTT_BROKER_PORT가 유효한 숫자가 아닙니다: {MQTT_BROKER_PORT}'
    logger.error(error_message)
    raise ValueError(error_message)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting lifespan")

    logger.info("Starting connect mqtt client")
    mqtt_client = BoMQTTClient(
        broker= MQTT_BROKER_HOST,
        port= MQTT_BROKER_PORT,
        id= MQTT_USERNAME,
        pw= MQTT_PASSWORD,
    )
    mqtt_client.connect()
    mqtt_client.loop_start()

    # logger.info("Starting connect redis client")
    # redis = RedisClient()
    # redis.connect()

    # 앱 상태에 mqtt_client 저장
    app.state.mqtt_client = mqtt_client
    # app.state.redis_client = redis

    logger.info("Successfully lifespan setting")
    yield

    mqtt_client.disconnect()
    # redis.disconnect()
app = FastAPI(lifespan=lifespan)

# app = FastAPI()
@app.get("/")
async def root():
    return {"message": "routing FastAPI"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(routers.router, prefix="/api", tags=["api"])


