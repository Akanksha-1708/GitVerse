import time
from fastapi import FastAPI, HTTPException, Request
from services.github_service import github_service
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

app=FastAPI(
    title="Gitverse Core Engine",
    description="High-throughput GitHub developer analytics API",
    version="2.0.0"
)
# CORS setup (to connect with frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: adds exact latency header to prove sub-100ms caching in resume
@app.middleware("http")
async def add_process_time_header(request:Request, call_next):
    start_time=time.pref_counter()
    response=await call_next(request)
    process_time=(time.pref_counter()-start_time)*1000  # i milliseconds
    response.headers["X-Response-Time-Ms"]=f"{ process_time:.2f}"
    return response

@app.get("/health")
async def health_check():
    return{
        "status": "healthy",
        "service": settings.APP_NAME,
        "env": settings.ENVIRONMENT
    }

@app.get("api/developer/{username}")
async def get_developer_metrics(username: str):
    try:
        data=await github_service.calculate_developer_analytics(username)
        return {"success": True, "data":data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub data: {str(e)}")

@app.get("/api/compare/{user1}/{user2}")
async def compare_developers(user1: str, user2: str):
    try:
        import asyncio
        d1, d2 = await asyncio.gather(
            github_service.calculate_developer_analytics(user1),
            github_service.calculate_developer_analytics(user2)
        )
        return {"success": True, "developer1": d1, "developer2": d2}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))