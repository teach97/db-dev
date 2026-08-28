import os

import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"],
    decode_responses=True,
    # 현재 Redis 서버가 HELLO/RESP3를 지원하지 않으므로 RESP2 사용
    protocol=2,
)
