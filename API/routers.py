from fastapi import APIRouter

from API.MQTT import mqtt_test_application
from API.SCAN import api_scan
router = APIRouter()
router.include_router(mqtt_test_application.router, prefix="/test", tags=["test"])
router.include_router(api_scan.router, prefix="/scan", tags=["scan"])
@router.get("/")
async def get_items():
    return [{"item": "item1"}, {"item": "item2"}]
