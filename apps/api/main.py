import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from services.github_service import github_service
from services.ai_service import ai_service
from config.settings import settings
from pydantic import BaseModel

app = FastAPI(
    title="GitVerse Core Engine",
    description="High-throughput GitHub developer analytics & AI intelligence API",
    version="2.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for Latency Header
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Response-Time-Ms"] = f"{process_time:.2f}"
    return response

# Request Schemas
class BulletRequest(BaseModel):
    repo_name: str
    description: str = ""
    language: str = "TypeScript"

class AuditRequest(BaseModel):
    repo_name: str
    description: str = ""
    language: str = "TypeScript"
    stars: int = 0
    forks: int = 0

class ChatRequest(BaseModel):
    username: str
    query: str

# Base Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME, "env": settings.ENVIRONMENT}

@app.get("/api/developer/{username}")
async def get_developer_metrics(username: str):
    try:
        data = await github_service.calculate_developer_analytics(username)
        return {"success": True, "data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# 🤖 ALL 5 AI ENDPOINTS
# =========================================================================

# 💡 Feature 1: Developer Persona
@app.get("/api/ai/persona/{username}")
async def get_developer_persona(username: str):
    try:
        user_data = await github_service.calculate_developer_analytics(username)
        persona = await ai_service.generate_developer_persona(
            user_data["profile"],
            user_data["top_repositories"]
        )
        return {"success": True, "persona": persona}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 💡 Feature 2: STAR Resume Bullets
@app.post("/api/ai/resume-bullets")
async def generate_resume_bullets(req: BulletRequest):
    try:
        bullets = await ai_service.generate_star_resume_bullets(req.repo_name, req.description, req.language)
        return {"success": True, "bullets": bullets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 💡 Feature 3: Repo Health & Security Audit
@app.post("/api/ai/repo-audit")
async def audit_repository(req: AuditRequest):
    try:
        audit = await ai_service.audit_repository(req.repo_name, req.description, req.language, req.stars, req.forks)
        return {"success": True, "audit": audit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 💡 Feature 4: "Ask My GitHub" Chatbot
@app.post("/api/ai/chat")
async def ask_my_github(req: ChatRequest):
    try:
        user_data = await github_service.calculate_developer_analytics(req.username)
        reply = await ai_service.ask_my_github_chat(req.username, user_data, req.query)
        return {"success": True, "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 💡 Feature 5: AI Interview Simulator
@app.get("/api/ai/interview-prep/{username}")
async def get_interview_prep(username: str):
    try:
        user_data = await github_service.calculate_developer_analytics(username)
        questions = await ai_service.generate_interview_questions(username, user_data)
        return {"success": True, "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))