import logging
from API.CONFIG.bogger import BoggerDevLogger
from API.MQTT.mqtt_subscriber import BoMQTTClient

from fastapi import APIRouter, Request

logger = BoggerDevLogger(__name__).logger
router = APIRouter()

@router.get("/mqtt_test/{data}")
async def mqtt_test(request: Request, data: bool):
    mqtt_client = request.state.mqtt_client
    mqtt_client.mqtt_client.publish("test/topic", data)
    logger.info(f"mqtt 정상 publish: {data}  | topic: test/topic")
    return {"test/topic": data}


