from fastapi import APIRouter, Request
import asyncio
import json
from API.CONFIG.bogger import BoggerDevLogger
from API.CONFIG.static import request_scan_topic, response_scan_topic, iot_response_queue

logger = BoggerDevLogger(__name__).logger
router = APIRouter()

@router.get("/device-status")
async def scan_device_status(request: Request):
    mqtt_client = request.app.state.mqtt_client
    mqtt_client.publish(
        topic = request_scan_topic,
        message="1"
    )
    # -- Queue를 이용한 비동기 데이터 상태 관리 --
    # 디바이스 응답을 비동기로 기다림
    try:
        timeout = 1 # 응답 대기 시간 (초)
        response_payload_str = await asyncio.wait_for(iot_response_queue.get(), timeout=timeout) # response_quere에서 메세지를 비동기적을 ㅗ가져옴
        logger.info(response_payload_str)
        print(response_payload_str)
        return json.dumps(response_payload_str)

    except asyncio.TimeoutError:
        logger.error(f"MQTT on_message timeout: {timeout}초 내에 IoT 디바이스로부터 응답을 받지 못했습니다.")
        return {'error': 'Timeout waiting for device response'}, 504
    except json.JSONDecodeError:
        logger.error(f"MQTT on_message return error: 수신된 응답이 유효한 JSON 형식이 아닙니다.")
        return {'error': 'Invalid JSON response from device'}, 500
    except Exception as e:
        logger.error(f'MQTT on_message error: 예상치 못한 오류 발생: {e}')
        return {'error', f'An unexpected error occurred: {str(e)}'}, 500


