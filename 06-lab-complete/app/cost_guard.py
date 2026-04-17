"""
Cost Guard Module — Quản lý ngân sách.
Hỗ trợ Fallback sang Memory nếu Redis không sẵn sàng.
"""
import time
import redis
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

class CostGuard:
    def __init__(self, redis_url: str, daily_budget: float):
        self.daily_budget = daily_budget
        self.redis_available = False
        self._memory_cost = 0.0

        if redis_url:
            try:
                self.r = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=2)
                self.r.ping()
                self.redis_available = True
            except Exception as e:
                logger.warning(f"⚠️ CostGuard: Redis connection failed. Using Memory.")

    def _get_key(self):
        return f"daily_cost:{time.strftime('%Y-%m-%d')}"

    def check_and_record_cost(self, input_tokens: int, output_tokens: int):
        new_cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
        
        if self.redis_available:
            try:
                key = self._get_key()
                pipe = self.r.pipeline()
                pipe.incrbyfloat(key, new_cost)
                pipe.expire(key, 86400)
                results = pipe.execute()
                if results[0] > self.daily_budget:
                    raise HTTPException(503, "Budget exhausted (Redis)")
                return
            except HTTPException: raise
            except Exception: pass

        # Fallback
        self._memory_cost += new_cost
        if self._memory_cost > self.daily_budget:
            raise HTTPException(503, "Budget exhausted (Memory)")

    @property
    def current_cost(self):
        if self.redis_available:
            try: return float(self.r.get(self._get_key()) or 0)
            except: pass
        return self._memory_cost

guardian = CostGuard(settings.redis_url, settings.daily_budget_usd)
