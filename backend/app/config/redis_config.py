# backend/app/config/redis_config.py

import redis

def get_redis_connection():
    r = redis.Redis(
        host='redis',   # nombre del servicio de redis en docker-compose
        port=6379, 
        db=0,
        decode_responses=True  # para que no te devuelva bytes, sino strings
    )
    return r
