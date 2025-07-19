import logging
import json
import threading

import paho.mqtt.client as mqtt

from API.CONFIG.bogger import BoggerDevLogger
from API.CONFIG.static import request_scan_topic, response_scan_topic, iot_response_queue


class BoMQTTClient:
    def __init__(self, broker="localhost", port=1883, id:str=None, pw:str=None, logger:logging.Logger=None):
        self.logger = logger or BoggerDevLogger(self.__class__.__name__).logger
        self.broker = broker
        self.port = port
        self.id = id
        self.pw = pw

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        MQTT client 연결 콜백 함수
        :param client: 클라이언트 인스턴스 
        :param userdata: 사용자가 설정한 데이터 
        :param flags: 연결 플래그
        :param rc: 연결 결과 코드 (Reson Code)
        """
        if rc == 0:
            self.client.subscribe(response_scan_topic)
            self.logger.info("MQTT 브로커에 성공적으로 연결되었습니다.")
        elif rc == 1:
            self.logger.error(f"MQTT connection error rc: {rc} - 잘못된 프로토콜 버전 ")
        elif rc == 2:
            self.logger.erorr(f"MQTT connection error rc: {rc} -  유효하지 않은 프로토콜")
        elif rc == 3:
            self.logger.error(f"MQTT connection error rc: {rc} - 서버를 사용할 수 없음")
        elif rc == 4:
            self.logger.error(f"MQTT connection error rc: {rc} - 잘못된 사용자 이름 또는 비밀번호")
        elif rc == 5:
            self.logger.error(f"MQTT connection error rc: {rc} - 인증 실패")
        else:
            self.logger.error(f"MQTT connection error rc: {rc} - 알 수 없는 에러")
            
    def on_disconnect(self, client, userdata, rc):
        """
         MQTT client disconnect 콜백 함수
        :param client: 클라이언트 인스턴스
        :param userdata: 사용자가 설정한 데이터
        :param rc: 연결 해제 결과 코드
        """
        if rc == 0:
            self.client.unsubscribe(response_scan_topic)
            self.logger.info(f"MQTT client의 {response_scan_topic}가 정상적으로 종료되었습니다.")
            self.logger.info("MQTT client가 정상적으로 연결 해제 되었습니다.")
        else:           
            self.logger.error(f"MQTT client disconnection error : 알 수 없는 연결 실패 rc: {rc}")

    def on_message(self, client, userdata, msg):
        """ 메세지 수신시의 호출 콜백 함수"""
        try:
            payload_str = msg.payload.decode('utf-8')

            # 메세지 입력 전에 최대한 유효성 검증하기
            # 큐에 메세지 입력
            iot_response_queue.put_nowait(payload_str)
            self.logger.info(f"Received message ; from topic: {msg.topic} ; successfully input in queue.")
        except Exception as e:
            self.logger.error(f"MQTT on_message error: {e}",)

    def connect(self):
        self.logger.debug(f"broker: {self.broker} ; port: {self.port} ; username: {self.id} ; password: {self.pw} - 본 로그는 개발 완료후 삭제해 주세요")
        if self.id and self.pw:
            # id, pw가 있어야 id, pw 로그인 코드 실행
            self.client.username_pw_set(username=self.id, password=self.pw)
            
        self.client.connect(self.broker, self.port)
        self.logger.info(f"Connected to broker: {self.broker}:{self.port}")

    def disconnect(self):
        self.client.disconnect()
        self.logger.info(f"Disconnected from broker: {self.broker}:{self.port}")

    def loop_start(self):
        self.client.loop_start()
        self.logger.info("MQTT Loop forever Start")

    def publish(self, topic: str, message: str):
        self.client.publish(topic, message, qos=1) # 기존 메세지 저장해 두는 것, retain=True)
        self.logger.info(f"Published to topic: {topic}  / message: {message}")


if __name__ == "__main__":
    mqtt_client = BoMQTTClient()
    mqtt_client.connect()
    mqtt_client.loop_forever()


