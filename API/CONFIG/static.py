import asyncio

# -- 공유 데이터 저장소 --
# IoT 디바이스 응답 메세지를 저장하고, FastAPI 요청 핸들러가 가져갈 큐
# 이 큐는 어플리케이션 전체에서 단 하나만 존재해야 한다.
iot_response_queue = asyncio.Queue()


# MQTT 상수 설정
request_scan_topic = "request/device-status"
response_scan_topic = "response/+/device-status"