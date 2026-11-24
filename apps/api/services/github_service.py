import httpx
from typing import Dict,Any,List
from config.settings import settings
from services.cache_service import cache
import asyncio

class GitHubService:
    BSE_URL="https://api.github.com"
    def _headers(self)->Dict[str,str]:
        headers={"Accept":"application/vnd.github.v3+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"]=f"Bearer {settings.GTIHUB_TOKEN}"
        return headers

    async def get_user_profile(self,username:str)->Dict[str,Any]:
        cache_key=f"gh:user_profile:{username.lower()}"
        cached=await cache.get(cache_key)
        if cached:
            cached["_cached"]=True
            return cached

        async with httpx.AsyncClient(headers=self._headers(),timeout=10.0) as client:
            res=await client.get(f"{self.BASE_URL}/users/{username}")
            if res.status_code==404:
                raise ValueError("GitHub user not found")
            res.raise_for_status()
            data=res.json()

        await cache.set(cache_key,data,ttl=3600)
        data["_cached"]=False
        return data

    async def get_user_repos(self,username:str)->List[Dict[str,Any]]:
        cache_key=f"gh:repos:{username.lower()}"
        cached=await cache.get(cache_key)
        if cached:
            return cached 

        async with httpx.AsyncClient(headers=self._headers(),timeout=15.0) as client:
            res=await client.get(f"{self.BASE_URL}/users/{username}/repos",
                                 params={"per_page":100,"sort":"updated","type":"owner"})
            res.raise_for_status()
            repos=res.json()

        await cache.set(cache_key,repos,ttl=3600)
        return repos
