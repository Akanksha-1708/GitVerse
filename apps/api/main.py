import time
from fastapi import FastAPI, HTTPException, Request
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

