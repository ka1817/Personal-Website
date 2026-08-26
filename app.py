"""
Katta Sai Pranav Reddy - Personal Portfolio Server
FastAPI Web Application & AI Interactive Assistant Backend
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Katta Sai Pranav Reddy Portfolio API",
        description="Backend service powering personal portfolio, AI assistant, and contact services",
        version="2.0.0"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static assets
    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Request Models
    class ChatQuery(BaseModel):
        query: str

    class ContactForm(BaseModel):
        name: str
        email: str
        subject: str
        message: str

    @app.get("/", response_class=HTMLResponse)
    async def serve_home():
        index_file = BASE_DIR / "index.html"
        if index_file.exists():
            return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
        return HTMLResponse("<h1>Portfolio Under Construction</h1>", status_code=404)

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "engineer": "Katta Sai Pranav Reddy",
            "role": "AI & ML Engineer / Data Scientist",
            "version": "2.0.0"
        }

    @app.get("/resume")
    async def get_resume():
        resume_path = BASE_DIR / "PranavR_Resume.pdf"
        if not resume_path.exists():
            resume_path = BASE_DIR / "static" / "assets" / "PranavR_Resume.pdf"
        if resume_path.exists():
            return FileResponse(
                path=str(resume_path),
                filename="PranavR_Resume.pdf",
                media_type="application/pdf"
            )
        raise HTTPException(status_code=404, detail="Resume PDF not found")

    @app.get("/api/stats")
    async def get_portfolio_stats():
        return {
            "public_repositories": 93,
            "gate_rank": "AIR 5262 (Data Science & AI)",
            "cgpa": 8.29,
            "rag_accuracy": "95%",
            "model_recall": "99%",
            "core_stack": ["Python", "Docker", "MLflow", "FAISS", "LangChain", "FastAPI", "AWS"]
        }

    @app.post("/api/chat")
    async def ai_chat_assistant(payload: ChatQuery):
        q = payload.query.lower().strip()
        
        # Knowledge reasoning rules
        if any(w in q for w in ["bigbasket", "shopping", "smartcart"]):
            reply = (
                "🛒 <strong>BigBasket SmartCart</strong>: Built a RAG-based AI shopping assistant enabling "
                "semantic product search with 95% retrieval accuracy and 0.89 relevance score using FAISS and Cross-Encoder re-ranking. "
                "Containerized with Docker & FastAPI on AWS EC2, cutting latency to ~2 seconds."
            )
        elif any(w in q for w in ["churn", "netflix", "customer"]):
            reply = (
                "📊 <strong>Netflix Customer Churn ML System</strong>: End-to-end MLOps pipeline achieving 99% recall. "
                "Integrated DVC for data versioning, MLflow for experiment tracking, and AWS S3 artifact management, "
                "deployed with automated GitHub Actions CI/CD to AWS EC2."
            )
        elif any(w in q for w in ["gate", "rank", "score"]):
            reply = (
                "🏆 <strong>GATE 2026 DA Achievement</strong>: Sai Pranav secured All India Rank <strong>5262</strong> "
                "in Data Science & Artificial Intelligence (DA)."
            )
        elif any(w in q for w in ["education", "college", "university", "study", "cgpa"]):
            reply = (
                "🎓 <strong>Education</strong>: B.Tech in Artificial Intelligence & Machine Learning at "
                "<strong>Anurag University, Hyderabad</strong> (2021–2025) with a CGPA of <strong>8.29/10</strong>. "
                "Intermediate MPC from Sri Chaitanya Junior College with <strong>98%</strong>."
            )
        elif any(w in q for w in ["intern", "experience", "work"]):
            reply = (
                "💼 <strong>Internship Experience</strong>:<br/>"
                "1. <strong>AI Varient</strong> (04/2026–07/2026): Data Science Intern – Engineered Alzheimer's classification pipeline with 93% recall.<br/>"
                "2. <strong>Unified Mentor</strong> (09/2024–10/2024): Data Science Intern – Employee attrition predictive modeling and HR analytics dashboards."
            )
        elif any(w in q for w in ["skill", "stack", "tool", "docker", "mlops", "python"]):
            reply = (
                "⚙️ <strong>Skills & Tooling</strong>:<br/>"
                "• <em>MLOps & Cloud:</em> MLflow, DVC, Docker, GitHub Actions, AWS (EC2, S3, ECR)<br/>"
                "• <em>Generative AI:</em> LangChain, LangSmith, FAISS, Pinecone, Hugging Face, RAG<br/>"
                "• <em>Core ML:</em> Python, Scikit-Learn, TensorFlow, Keras, PyTorch, SQL, FastAPI"
            )
        elif any(w in q for w in ["contact", "email", "phone", "reach", "hire", "linkedin"]):
            reply = (
                "📬 <strong>Get in Touch</strong>:<br/>"
                "• Email: <a href='mailto:kattapranavreddy@gmail.com' class='text-cyan-400 underline'>kattapranavreddy@gmail.com</a><br/>"
                "• GitHub: <a href='https://github.com/ka1817' target='_blank' class='text-purple-400 underline'>github.com/ka1817</a><br/>"
                "• LinkedIn: <a href='https://linkedin.com/in/pranav-reddy-katta' target='_blank' class='text-blue-400 underline'>pranav-reddy-katta</a>"
            )
        else:
            reply = (
                f"Hello! I am Sai Pranav's AI assistant. Sai Pranav is an AI & ML Engineer specializing in "
                f"Agentic RAG, MLOps, and production Dockerized microservices. Ask me about his projects, GATE rank, "
                f"internships, or skills!"
            )

        return {"reply": reply}

    @app.post("/api/contact")
    async def submit_contact(payload: ContactForm):
        print(f"[PORTFOLIO CONTACT] From: {payload.name} ({payload.email}) | Subject: {payload.subject}")
        return {
            "status": "success",
            "message": "Thank you! Your message has been received by Sai Pranav."
        }


def run_simple_server(port=8000):
    import http.server
    import socketserver
    
    os.chdir(str(BASE_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    
    print(f"[*] Starting Standard HTTP Server on http://0.0.0.0:{port}")
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


def main():
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    if FASTAPI_AVAILABLE and "--simple" not in sys.argv:
        print(f"[*] Launching FastAPI Portfolio Server on http://{host}:{port}")
        uvicorn.run("app:app", host=host, port=port, reload=False)
    else:
        run_simple_server(port)


if __name__ == "__main__":
    main()
