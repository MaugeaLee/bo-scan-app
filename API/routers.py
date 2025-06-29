from fastapi import APIRouter

from API.MQTT import mqtt_test_application

router = APIRouter()
router.include_router(mqtt_test_application.router, prefix="/test", tags=["test"])

@router.get("/")
async def get_items():
    return [{"item": "item1"}, {"item": "item2"}]
