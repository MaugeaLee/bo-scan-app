from fastapi import APIRouter, Request

from API.CONFIG.static import *

router = APIRouter()

@router.get("/device-status")
async def scan_device_status(request: Request):
    mqtt_client = request.app.state.mqtt_client
    mqtt_client.publish(
        topic = request_scan_topic,
        message="1"
    )

    return {"status": "published", "topic": request_scan_topic, "message": "aa"}


