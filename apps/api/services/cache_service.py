import json
import logging
from typing import Optional, Any
import redis.asyncio as redis
from config.settings import settings

logger=logging.getLogger("gitverse.cache")

class CacheService:
    def __init__(self):
        self.client=None
        try:
            self.client=redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=2.0
            )
        except Exception as e:
            logger.warning(f"Redis initialization notice:{e}")

    async def get(self,key:str)->Optional[Any]:
        if not self.client:
            return None
        try:
            data=await self.client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            return None
        return None

    async def set(self,key:str,value:Any,ttl:int=settings.CACHE__TTL_SECONDS):
        if not self.client:
            return
        try:
            await self.client.setex(key,ttl,json.dumps(value))
        except Exception:
            pass

cache=CacheService()