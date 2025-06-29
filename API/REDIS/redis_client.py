import redis
import logging
import time
import sys
from API.CONFIG.bogger import BoggerDevLogger

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0, retries=3, retry_delay=2, logger:logging.Logger=None):
        self.logger = logger or BoggerDevLogger(self.__class__.__name__).logger
        self.host = host
        self.port = port
        self.db = db
        self.retries = retries
        self.retry_delay = retry_delay
        self.r_client = None


    def connect(self):
        attempt = 0
        # 연결 확인과 재연결 반복
        while attempt < self.retries:
            try:
                self.r_client = redis.Redis(host=self.host, port=self.port, db=self.db, socket_connect_timeout=5)
                # ping으로 redis server 연결 가능 확인
                if self.r_client.ping():
                    self.logger.info("Redis 서버의 PING 연결 확인.")
                    break
                else:
                    self.logger.warning("Redis 서버의 PING 연결 실패.")
            except redis.exceptions.ConnectionError as connect_error:
                self.logger.error(f"❌ Redis 연결 실패 (시도 {attempt + 1}/{self.retries}) : {connect_error}")
            except Exception as e:
                self.logger.error(f"⚠️ 예기치 못한 오류 : {e}")

            attempt += 1
            time.sleep(self.retry_delay)

        if self.r_client.ping():
            self.logger.info("🟢 Redis 정상 연결 확인.")
        else:
            # 반복 끝에 연결 실패
            self.logger.error(f"🚨 Redis retry 횟수 초과. 프로세스를 종료.")
            # 프로세스 종료
            sys.exit(1)

    def disconnect(self):
        self.r_client.close()
        self.logger.info("Redis client가 정상적으로 종료되었습니다.")

if __name__ == "__main__":
    r = RedisClient()