import httpx
from typing import Dict,Any,List
from config.settings import settings
from services.cache_service import cache
import asyncio

class GitHubService:
    BASE_URL="https://api.github.com"
    def _headers(self)->Dict[str,str]:
        headers={"Accept":"application/vnd.github.v3+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"]=f"Bearer {settings.GITHUB_TOKEN}"
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

    async def calculate_developer_analytics(self,username:str)->Dict[str,Any]:
        cache_key=f"gh:analytics:{username.lower()}"
        cached=await cache.get(cache_key)
        if cached:
            cached["_from_cache"]=True
            return cached

        user,repos=await asyncio.gather(
            self.get_user_profile(username),
            self.get_user_repos(username)
        )

        total_stars=sum(r.get("stargazers_count",0) for r in repos)
        total_forks=sum(r.get("forks_count",0) for r in repos)

        # primary language frequency breakdown
        lang_counts:Dict[str,int]={}
        for r in repos:
            lang=r.get("language")
            if lang:
                lang_counts[lang]=lang_counts.get(lang,0)+1

        # Top 6 repositories sorted by stars
        top_repos=sorted(repos,key=lambda x:x.get("stargazers_count",0), reverse=True)[:6]
        analytics={
            "username": username,
            "_from_cache": False,
            "profile": {
                "name": user.get("name") or user.get("login"),
                "login": user.get("login"),
                "avatar_url": user.get("avatar_url"),
                "bio": user.get("bio"),
                "location": user.get("location"),
                "blog": user.get("blog"),
                "html_url": user.get("html_url"),
                "created_at": user.get("created_at")
            },
            "metrics": {
                "total_repos": len(repos),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "followers": user.get("followers", 0),
                "following": user.get("following", 0)
            },
            "languages": lang_counts,
            "top_repositories": [
                {
                    "name": r["name"],
                    "description": r.get("description"),
                    "stars": r.get("stargazers_count", 0),
                    "forks": r.get("forks_count", 0),
                    "language": r.get("language"),
                    "html_url": r["html_url"],
                    "updated_at": r["updated_at"]
                }
                for r in top_repos
            ]
        }
        await cache.set(cache_key,analytics,ttl=1800)
        return analytics
    
github_service = GitHubService()