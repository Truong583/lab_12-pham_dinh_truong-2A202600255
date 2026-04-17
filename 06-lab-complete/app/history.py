"""
History Module — Quản lý lịch sử hội thoại.
Hỗ trợ Fallback Memory nếu không có Redis.
"""
import redis
import json
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class History:
    def __init__(self, redis_url: str, max_history: int = 10):
        self.max_history = max_history
        self.redis_available = False
        self._memory_history = {} # {user_id: [messages]}

        if redis_url:
            try:
                self.r = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=2)
                self.r.ping()
                self.redis_available = True
            except Exception as e:
                logger.warning(f"⚠️ History: Redis connection failed. Using Memory.")

    def add_message(self, user_id: str, role: str, content: str):
        if self.redis_available:
            try:
                key = f"history:{user_id}"
                message = json.dumps({"role": role, "content": content})
                pipe = self.r.pipeline()
                pipe.lpush(key, message)
                pipe.ltrim(key, 0, self.max_history - 1)
                pipe.expire(key, 3600)
                pipe.execute()
                return
            except: pass

        # Fallback
        if user_id not in self._memory_history:
            self._memory_history[user_id] = []
        self._memory_history[user_id].append({"role": role, "content": content})
        if len(self._memory_history[user_id]) > self.max_history:
            self._memory_history[user_id].pop(0)

    def get_history(self, user_id: str) -> list[dict]:
        if self.redis_available:
            try:
                key = f"history:{user_id}"
                raw = self.r.lrange(key, 0, -1)
                return [json.loads(m) for m in reversed(raw)]
            except: pass
        return self._memory_history.get(user_id, [])

history_manager = History(settings.redis_url)
