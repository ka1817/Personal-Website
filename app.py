"""
Katta Sai Pranav Reddy - Personal Portfolio Server
FastAPI Web Application, PostgreSQL Contact Integration & Groq AI Interactive Console
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("portfolio")

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
    from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# Groq Client Initialization
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import AsyncGroq
        groq_client = AsyncGroq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialized successfully with GROQ_API_KEY.")
    except Exception as e:
        logger.warning(f"Could not initialize AsyncGroq client: {e}")

# PostgreSQL Helper Functions
def init_db():
    """Initializes PostgreSQL table for contact messages if DATABASE_URL is configured."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.info("DATABASE_URL is not set in .env. Skipping database table initialization.")
        return

    try:
        import psycopg2
        # Clean URL format if needed (e.g. postgres:// -> postgresql://)
        clean_url = db_url.strip().strip('"\'')
        if clean_url.startswith("postgres://"):
            clean_url = clean_url.replace("postgres://", "postgresql://", 1)

        conn = psycopg2.connect(clean_url)
        cur = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("PostgreSQL contact_messages table verified / created successfully.")
    except Exception as e:
        logger.error(f"Error initializing PostgreSQL table: {e}")

def save_contact_to_db(name: str, email: str, subject: str, message: str) -> bool:
    """Saves a contact message into PostgreSQL database."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.warning(f"[CONTACT - NO DB CONFIGURED] From: {name} <{email}> | Subject: {subject}")
        return False

    try:
        import psycopg2
        clean_url = db_url.strip().strip('"\'')
        if clean_url.startswith("postgres://"):
            clean_url = clean_url.replace("postgres://", "postgresql://", 1)

        conn = psycopg2.connect(clean_url)
        cur = conn.cursor()
        insert_sql = """
        INSERT INTO contact_messages (name, email, subject, message, created_at)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_sql, (name, email, subject, message, datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Successfully saved contact message from {email} to PostgreSQL.")
        return True
    except Exception as e:
        logger.error(f"Failed to save contact message to PostgreSQL: {e}")
        return False


# Candidate Knowledge Database & System Prompt for Groq AI Console
SYSTEM_PROMPT = """You are an expert AI recruiter and personal portfolio assistant representing Katta Sai Pranav Reddy.
Your purpose is to answer questions from recruiters, engineers, hiring managers, and visitors about Pranav's background, technical skills, projects, achievements, and experience.

You must strictly adhere to the following rules:
1. Zero Hallucination: Answer questions using ONLY the information provided in the "Candidate Database" below. Do not infer, guess, or invent any metrics or skills not explicitly provided.
2. Handle Missing Info Gracefully: If a user asks a question that cannot be answered by the provided data, respond with: "I don't have that specific information in my context, but you can reach out to Pranav directly at kattapranavreddy@gmail.com to discuss it."
3. Tone: Concise, professional, confident, knowledgeable, and highly technical.
4. Direct Answers: Do not use robotic prefixes like "According to the provided data" or "Based on the context". Answer questions naturally and directly.

--- CANDIDATE DATABASE ---

**Identity & Contact:**
* Full Name: Katta Sai Pranav Reddy
* Location: Hyderabad, India (Open to Remote and Relocation)
* Email: kattapranavreddy@gmail.com
* GitHub: https://github.com/ka1817 (Username: ka1817, 93+ public repositories)
* LinkedIn: https://www.linkedin.com/in/pranav-reddy-katta (pranav-reddy-katta)
* Role: AI & Machine Learning Engineer | Data Scientist | MLOps Specialist

**Education:**
* B.Tech in Artificial Intelligence and Machine Learning
  - Anurag University, Hyderabad, India (09/2021 – 04/2025)
  - CGPA: 8.29 / 10.0
* Class XII / Intermediate – MPC (Maths, Physics, Chemistry)
  - Sri Chaitanya Junior College, Hyderabad, India (06/2019 – 05/2021)
  - Score: 98%

**Key Achievements:**
* GATE 2026 – Data Science & Artificial Intelligence (DA):
  - All India Rank: AIR 5262 (93rd Percentile) in national-level examination.

**Work Experience & Internships:**
1. AI Varient (04/2026 – 07/2026) | Data Science Intern
   - Engineered an end-to-end ML pipeline for Alzheimer's disease classification, achieving a 93% recall rate by building and hyperparameter tuning Random Forest models.
   - Conducted comprehensive Exploratory Data Analysis (EDA) to uncover key predictive features, optimize data preprocessing workflows, and enhance overall model interpretability.
2. Unified Mentor Pvt. Ltd. (09/2024 – 10/2024) | Data Science Intern
   - Developed and optimized machine learning models to predict employee attrition, identifying key turnover drivers through data preprocessing.
   - Designed interactive analytics dashboards to visualize attrition patterns and presented strategic data-driven recommendations to HR stakeholders.
3. iNeuron Intelligence Pvt. Ltd. (10/2024 – 11/2024) | Machine Learning Intern
   - Conducted extensive data preprocessing and EDA on large customer datasets to identify behavioral patterns.
   - Developed customer segmentation ML models using K-Means clustering, achieving a Silhouette Score of 0.82.

**Key Technical Projects:**
1. BigBasket SmartCart – AI-Driven Shopping Assistant (GitHub: ka1817/BigBasket-SmartCart-AI-Assistant-for-BigBasket-Shopping)
   - Built a RAG-based AI shopping assistant enabling semantic product search with 95% retrieval accuracy.
   - Engineered a FAISS vector index and Cross-Encoder retrieval re-ranking pipeline (0.89 relevance score).
   - Designed scalable microservices architecture using FastAPI and Docker, reducing response latency to ~2 seconds.
   - Automated CI/CD pipelines with GitHub Actions and AWS EC2, reducing deployment time by 40%.
2. Netflix Customer Churn Prediction – End-to-End ML System (GitHub: ka1817/Customer-Churn-Prediction-in-the-Telecom-Industry-Using-Machine-Learning)
   - Developed an ML pipeline predicting customer churn, achieving 99% recall via hyperparameter tuning.
   - Established MLOps workflows using DVC for data versioning, AWS S3 for artifact storage, and MLflow for experiment tracking.
   - Deployed a containerized FastAPI REST API with automated GitHub Actions CI/CD to AWS EC2.
3. Agentic RAG-Powered Medical Assistant (GitHub: ka1817/Agentic-RAG-Powered-Medical-Assistant)
   - Autonomous multi-agent biomedical question answering system combining biomedical embeddings, recursive query rewriting, and factual citation verification.
4. Alzheimer's Disease Diagnostic Pipeline (GitHub: ka1817/Alzheimer-s_Disease_Classification-)
   - Clinical ML diagnostic pipeline reaching 93% recall rate on clinical features with feature importance analysis.
5. AI for Smarter SQL Analytics (GitHub: ka1817/AI_for_Smarter_SQL_Analytics)
   - Natural language to SQL query generation, schema-aware prompting, and execution safety checks.
6. AskTube – AI Assistant for Video Insights (GitHub: ka1817/AskTube-AI-Assistant-for-Video-Insights)
   - Video transcription analysis, timestamped semantic retrieval, and chapter summarization.
7. Chat_PDF – RAG Enhanced Document Q&A Bot (GitHub: ka1817/Chat_PDF)
   - Conversational PDF assistant with LangChain vector embeddings and conversational memory.

**Technical Skills:**
* Tools & MLOps: MLflow, DVC, Docker, Git, GitHub Actions, AWS (EC2, S3, ECR), FAISS, Pinecone, Hugging Face, LangChain, LangSmith, FastAPI, Streamlit.
* Programming: Python, SQL, HTML5, CSS3, JavaScript, Scikit-learn, TensorFlow, Keras, Statistics.
* ML Domains: Data Preprocessing, EDA, Feature Engineering, Model Training & Evaluation, Hyperparameter Tuning, Clustering, MLOps, Semantic Search, RAG, CNN, RNN, GPT, Transformers, Fine-Tuning, Prompt Engineering.
* Data Visualization: Pandas, NumPy, Matplotlib, Seaborn.
--- END CANDIDATE DATABASE ---"""


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Katta Sai Pranav Reddy Portfolio & AI Console API",
        description="Backend service powering portfolio, PostgreSQL contact storage, and Groq LLM Assistant",
        version="2.1.0"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static assets mount
    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Request / Response Models
    class ChatRequest(BaseModel):
        query: str

    class ContactForm(BaseModel):
        name: str
        email: str
        subject: str
        message: str

    @app.on_event("startup")
    async def startup_event():
        init_db()

    @app.get("/", response_class=HTMLResponse)
    async def serve_home():
        index_file = BASE_DIR / "index.html"
        if index_file.exists():
            return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
        return HTMLResponse("<h1>Portfolio Under Construction</h1>", status_code=404)

    @app.get("/health")
    async def health_check():
        db_configured = bool(os.getenv("DATABASE_URL"))
        groq_configured = bool(os.getenv("GROQ_API_KEY"))
        return {
            "status": "healthy",
            "engineer": "Katta Sai Pranav Reddy",
            "database_configured": db_configured,
            "groq_api_configured": groq_configured,
            "version": "2.1.0"
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
            "core_stack": ["Python", "Docker", "MLflow", "FAISS", "LangChain", "FastAPI", "AWS", "Groq", "PostgreSQL"]
        }

    @app.post("/api/chat")
    async def ai_chat_assistant(req: ChatRequest):
        """Generates AI assistant answers using Groq LLM (groq/compound-mini) or fallback."""
        user_query = req.query.strip()
        if not user_query:
            return {"reply": "Please enter a question or command to get started."}

        api_key = os.getenv("GROQ_API_KEY")

        # 1. If GROQ_API_KEY is available in .env, call Groq LLM
        if api_key:
            try:
                from groq import AsyncGroq
                client = AsyncGroq(api_key=api_key)
                chat_completion = await client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_query}
                    ],
                    model="groq/compound-mini",
                    temperature=0.2,
                    max_tokens=600,
                )
                answer = chat_completion.choices[0].message.content
                return {"reply": answer}
            except Exception as e:
                logger.error(f"Groq API Error: {e}")
                # Fallback to local heuristic engine if Groq call fails

        # 2. Local Heuristic Engine fallback if GROQ_API_KEY is not yet added to .env
        q = user_query.lower()
        if any(w in q for w in ["bigbasket", "shopping", "smartcart"]):
            reply = (
                "🛒 <strong>BigBasket SmartCart</strong>: RAG-based AI shopping assistant enabling "
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
                "(93rd Percentile) in Data Science & Artificial Intelligence (DA)."
            )
        elif any(w in q for w in ["education", "college", "university", "study", "cgpa", "degree"]):
            reply = (
                "🎓 <strong>Education</strong>: B.Tech in Artificial Intelligence & Machine Learning at "
                "<strong>Anurag University, Hyderabad</strong> (09/2021 – 04/2025) with a CGPA of <strong>8.29/10</strong>. "
                "Intermediate MPC from Sri Chaitanya Junior College with <strong>98%</strong>."
            )
        elif any(w in q for w in ["intern", "experience", "work", "ineuron", "varient", "mentor"]):
            reply = (
                "💼 <strong>Internship Experience</strong>:<br/>"
                "1. <strong>AI Varient</strong> (04/2026–07/2026): Data Science Intern – Alzheimer's diagnostic pipeline with 93% recall.<br/>"
                "2. <strong>Unified Mentor</strong> (09/2024–10/2024): Data Science Intern – Employee attrition predictive modeling & dashboards.<br/>"
                "3. <strong>iNeuron Intelligence</strong> (10/2024–11/2024): ML Intern – Customer segmentation with K-Means (0.82 Silhouette Score)."
            )
        elif any(w in q for w in ["skill", "stack", "tool", "docker", "mlops", "python", "aws", "langchain"]):
            reply = (
                "⚙️ <strong>Skills & Tech Stack</strong>:<br/>"
                "• <em>MLOps & Cloud:</em> MLflow, DVC, Docker, GitHub Actions, AWS (EC2, S3, ECR), PostgreSQL<br/>"
                "• <em>Generative AI & LLMs:</em> LangChain, LangSmith, FAISS, Pinecone, Hugging Face, Groq, RAG<br/>"
                "• <em>Core ML & DL:</em> Python, Scikit-Learn, TensorFlow, Keras, SQL, FastAPI, Statistics"
            )
        elif any(w in q for w in ["contact", "email", "phone", "reach", "hire", "linkedin"]):
            reply = (
                "📬 <strong>Contact Details</strong>:<br/>"
                "• Email: <a href='mailto:kattapranavreddy@gmail.com' class='text-cyan-400 underline'>kattapranavreddy@gmail.com</a><br/>"
                "• GitHub: <a href='https://github.com/ka1817' target='_blank' class='text-purple-400 underline'>github.com/ka1817</a><br/>"
                "• LinkedIn: <a href='https://linkedin.com/in/pranav-reddy-katta' target='_blank' class='text-blue-400 underline'>pranav-reddy-katta</a>"
            )
        elif any(w in q for w in ["groq", "api", "key", "model"]):
            reply = (
                "🤖 The AI Console is integrated with <strong>Groq API (llama-3.3-70b-versatile)</strong>. "
                "Add your <code>GROQ_API_KEY</code> into the <code>.env</code> file to unlock live ultra-fast LLM responses!"
            )
        else:
            reply = (
                f"Katta Sai Pranav Reddy is an AI & ML Engineer specializing in Agentic RAG architectures, "
                f"MLOps (MLflow, DVC, Docker, AWS), and production data science systems. Type <code>help</code>, "
                f"ask about his projects, or configure <code>GROQ_API_KEY</code> in <code>.env</code> for full conversational reasoning."
            )

        return {"reply": reply}

    @app.post("/predict")
    async def handle_prediction(req: ChatRequest):
        """Streaming prediction endpoint matching the LLM_Personal_Chatbot repository specification."""
        api_key = os.getenv("GROQ_API_KEY")

        async def generate_response():
            if api_key:
                try:
                    from groq import AsyncGroq
                    client = AsyncGroq(api_key=api_key)
                    stream = await client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": req.query}
                        ],
                        model="groq/compound-mini",
                        temperature=0.2,
                        max_tokens=600,
                        stream=True
                    )
                    async for chunk in stream:
                        content = chunk.choices[0].delta.content or ""
                        if content:
                            yield content
                    return
                except Exception as e:
                    yield f"Error connecting to Groq LLM: {str(e)}"
                    return

            # Fallback message
            yield f"Sai Pranav Reddy is an AI/ML Engineer with expertise in RAG, MLOps, and Docker. (To enable live Groq streaming, please set GROQ_API_KEY in your .env file)."

        return StreamingResponse(generate_response(), media_type="text/plain")

    @app.post("/api/contact")
    async def submit_contact(payload: ContactForm, background_tasks: BackgroundTasks):
        """Processes contact form and saves details to PostgreSQL database."""
        name = payload.name.strip()
        email = payload.email.strip()
        subject = payload.subject.strip()
        message = payload.message.strip()

        if not name or not email or not message:
            raise HTTPException(status_code=400, detail="Name, email, and message are required.")

        # Save to PostgreSQL
        saved = save_contact_to_db(name, email, subject, message)

        if saved:
            return {
                "status": "success",
                "storage": "postgresql",
                "message": "Thank you! Your message has been securely recorded to the PostgreSQL database."
            }
        else:
            return {
                "status": "success",
                "storage": "local_received",
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
