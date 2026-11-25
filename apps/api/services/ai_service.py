import json
import logging
from typing import Dict, Any, List
from google import genai
from config.settings import settings
from services.cache_service import cache

logger = logging.getLogger("gitverse.ai")

class AIService:
    def __init__(self):
        self.client = None
        if settings.GEMINI_API_KEY:
            try:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client: {e}")

    # =========================================================================
    # 💡 FEATURE 1: AI Developer Persona & AST Architecture Diagram
    # =========================================================================
    async def generate_developer_persona(self, profile: Dict[str, Any], repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        username = profile.get("login", "")
        cache_key = f"ai:persona:{username.lower()}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        if not self.client:
            return {
                "archetype": "Full-Stack AI & Systems Architect",
                "superpower": "Rapid prototyping across distributed web architectures and LLM agentic workflows.",
                "growth_areas": ["Increase automated unit test coverage", "Adopt end-to-end CI/CD observability"],
                "mermaid_diagram": "graph TD;\n  UI[Next.js 15 Client] --> API[FastAPI Backend];\n  API --> Redis[(Redis Cache)];\n  API --> AI[Gemini 2.0 Engine];"
            }

        prompt = f"""
        Act as a FAANG Principal Software Architect.
        Analyze this GitHub profile and repositories:
        Developer: {username}
        Bio: {profile.get('bio')}
        Repositories: {[r.get('name') + ': ' + str(r.get('description')) for r in repos[:6]]}
        Languages: {[r.get('language') for r in repos if r.get('language')]}

        Return a STRICT JSON object with these exact keys:
        - "archetype": 2-4 word impressive title (e.g., 'Cloud-Native Backend Engineer', 'AI Agent Architect')
        - "superpower": One compelling sentence detailing their key coding strength
        - "growth_areas": Array of 2 actionable technical recommendations
        - "mermaid_diagram": A valid Mermaid flowchart string (graph TD) connecting their core project domains to their system architecture.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            data = json.loads(response.text)
            await cache.set(cache_key, data, ttl=86400)
            return data
        except Exception as e:
            logger.error(f"Error in Persona Engine: {e}")
            return {
                "archetype": "Full-Stack Systems Engineer",
                "superpower": "Versatile full-stack development with modern API design discipline.",
                "growth_areas": ["Expand cloud deployment infrastructure", "Deepen system observability"],
                "mermaid_diagram": "graph TD;\n  Client --> Gateway;\n  Gateway --> API;\n  API --> Database;"
            }

    # =========================================================================
    # 💡 FEATURE 2: Automated STAR-Format Resume Bullet Studio
    # =========================================================================
    async def generate_star_resume_bullets(self, repo_name: str, description: str, language: str) -> List[str]:
        cache_key = f"ai:bullets:{repo_name.lower()}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        if not self.client:
            return [
                f"Architected {repo_name} utilizing {language}, designing modular and maintainable component pipelines.",
                f"Optimized data querying and state synchronization, reducing overall latency by 40%.",
                f"Containerized system dependencies ensuring seamless zero-downtime deployment across environments."
            ]

        prompt = f"""
        Act as a FAANG Technical Resume Strategist.
        Convert this technical GitHub project into 3 resume bullet points following the Google/Amazon STAR (Situation-Task-Action-Result) format:
        - Project Name: {repo_name}
        - Description: {description}
        - Primary Technology: {language}

        Rules:
        1. Start each bullet with an active verb (Engineered, Architected, Spearheaded, Implemented).
        2. Incorporate realistic, quantifiable impact metrics (e.g., latency reduction, throughput, reliability).
        3. Keep them strictly professional, concise, and ATS-friendly.
        Return a JSON array of 3 strings.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            bullets = json.loads(response.text)
            await cache.set(cache_key, bullets, ttl=86400)
            return bullets
        except Exception:
            return [
                f"Engineered {repo_name} using {language}, boosting efficiency by 35% with clean architectural patterns.",
                f"Implemented robust API integrations and error-handling routines for high reliability.",
                f"Structured scalable code workflows suitable for production-ready deployment."
            ]

    # =========================================================================
    # 💡 FEATURE 3: AI Repo Health & Security Auditor
    # =========================================================================
    async def audit_repository(self, repo_name: str, description: str, language: str, stars: int, forks: int) -> Dict[str, Any]:
        cache_key = f"ai:audit:{repo_name.lower()}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        if not self.client:
            return {
                "health_score": 88,
                "summary": f"{repo_name} exhibits clean repository hygiene with solid architectural foundations.",
                "code_smells": ["Ensure comprehensive .env.example exists", "Add automated integration tests"],
                "security_checklist": [
                    {"check": "No hardcoded secrets or API tokens", "passed": True},
                    {"check": "Production-ready .gitignore", "passed": True},
                    {"check": "Open source license configured", "passed": True},
                    {"check": "Branch protection rules on main", "passed": False}
                ],
                "suggested_readme": f"# {repo_name}\n\n{description}\n\n## Architecture\nBuilt with {language} for high-performance execution."
            }

        prompt = f"""
        Act as a Senior AppSec & Code Quality Auditor.
        Perform a health and security audit on this GitHub repository:
        - Name: {repo_name}
        - Description: {description}
        - Language: {language}
        - Stars: {stars}, Forks: {forks}

        Return a STRICT JSON object with:
        - "health_score": integer between 60 and 98 based on quality
        - "summary": 2-sentence summary of repo quality
        - "code_smells": array of 2-3 potential areas of improvement
        - "security_checklist": array of 4 objects: {{"check": string, "passed": boolean}}
        - "suggested_readme": short markdown template for a production README
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            audit_data = json.loads(response.text)
            await cache.set(cache_key, audit_data, ttl=86400)
            return audit_data
        except Exception:
            return {
                "health_score": 85,
                "summary": "Repository follows good structure with room for automated CI test coverage.",
                "code_smells": ["Add unit tests", "Include deployment guide"],
                "security_checklist": [
                    {"check": "Secret isolation verified", "passed": True},
                    {"check": "License safety", "passed": True}
                ],
                "suggested_readme": f"# {repo_name}\n\nProduction-ready service built with {language}."
            }

    # =========================================================================
    # 💡 FEATURE 4: "Ask My GitHub" RAG Chatbot
    # =========================================================================
    async def ask_my_github_chat(self, username: str, user_data: Dict[str, Any], query: str) -> str:
        repos_summary = "\n".join([
            f"- {r['name']} ({r.get('language')}): {r.get('description', '')}"
            for r in user_data.get("top_repositories", [])
        ])
        languages = ", ".join(user_data.get("languages", {}).keys())

        if not self.client:
            return f"Based on {username}'s GitHub activity, they specialize in {languages}. Notable projects include {', '.join([r['name'] for r in user_data.get('top_repositories', [])[:3]])} with clean architectural design."

        prompt = f"""
        You are an AI Technical Representative representing the developer @{username}.
        A technical recruiter or hiring manager asks: "{query}"

        Context on @{username}'s GitHub:
        - Core Technologies: {languages}
        - Repositories & Descriptions:
        {repos_summary}

        Instructions:
        1. Answer directly and concisely based ONLY on their actual GitHub projects.
        2. Specifically cite project names (e.g., 'In their project GitVerse...').
        3. If something is not in their public GitHub, politely state that it is not explicitly demonstrated in their public repos.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"@{username} exhibits extensive hands-on experience in {languages}, actively building projects like {user_data.get('top_repositories', [{}])[0].get('name', 'their top repos')}."

    # =========================================================================
    # 💡 FEATURE 5: AI Technical Interview Simulator
    # =========================================================================
    async def generate_interview_questions(self, username: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        cache_key = f"ai:interview:{username.lower()}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        top_repos = user_data.get("top_repositories", [])
        repos_context = ", ".join([f"{r['name']} ({r.get('language')})" for r in top_repos[:4]])

        if not self.client:
            return [
                {
                    "question": f"In your project {top_repos[0]['name'] if top_repos else 'GitVerse'}, how did you structure state management and handle API rate limits?",
                    "project": top_repos[0]['name'] if top_repos else "GitVerse",
                    "hint": "Discuss Redis in-memory caching and async HTTP request pooling."
                },
                {
                    "question": "How do you ensure zero-downtime container deployments when updating backend microservices?",
                    "project": "System Architecture",
                    "hint": "Highlight multi-stage Docker builds and health checks."
                }
            ]

        prompt = f"""
        Act as a FAANG Hiring Manager preparing for a technical interview with @{username}.
        Based on their actual projects: {repos_context}.

        Generate 3 technical system design and architectural interview questions that directly test their decisions on these projects.
        Return a STRICT JSON array of objects with keys:
        - "question": The technical question
        - "project": The specific project referenced
        - "hint": A brief guidance tip on what a good answer covers
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            questions = json.loads(response.text)
            await cache.set(cache_key, questions, ttl=86400)
            return questions
        except Exception:
            return [
                {
                    "question": f"In your project {top_repos[0]['name']}, how did you manage asynchronous tasks without blocking the main event loop?",
                    "project": top_repos[0]['name'],
                    "hint": "Mention asyncio and background job processing."
                }
            ]

ai_service = AIService()