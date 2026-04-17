"""
Rate Limiter Module — Chống spam request.
Hỗ trợ cơ chế Fallback: Nếu không có Redis sẽ dùng Memory.
"""
import time
import redis
import logging
from collections import deque
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, redis_url: str, limit: int):
        self.limit = limit
        self.redis_available = False
        self.memory_storage = {} # Fallback storage

        if redis_url:
            try:
                self.r = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=2)
                self.r.ping()
                self.redis_available = True
                logger.info("✅ RateLimiter: Connected to Redis")
            except Exception as e:
                logger.warning(f"⚠️ RateLimiter: Redis connection failed ({e}). Falling back to Memory.")

    def check(self, key: str):
        now = time.time()
        if self.redis_available:
            try:
                redis_key = f"rate_limit:{key}"
                pipe = self.r.pipeline()
                pipe.lpush(redis_key, str(now))
                pipe.ltrim(redis_key, 0, self.limit)
                pipe.expire(redis_key, 60)
                pipe.llen(redis_key)
                results = pipe.execute()
                if results[-1] > self.limit:
                    raise HTTPException(429, "Rate limit exceeded (Redis)")
                return
            except HTTPException: raise
            except Exception as e:
                logger.error(f"Redis error in limiter: {e}")

        # Fallback to Memory
        if key not in self.memory_storage:
            self.memory_storage[key] = deque()
        
        window = self.memory_storage[key]
        while window and now - window[0] > 60:
            window.popleft()
            
        if len(window) >= self.limit:
            raise HTTPException(429, f"Rate limit exceeded (Memory): {self.limit} req/min")
        
        window.append(now)

limiter = RateLimiter(settings.redis_url, settings.rate_limit_per_minute)
