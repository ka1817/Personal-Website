# Katta Sai Pranav Reddy — Personal Portfolio & AI Console

<div align="center">

![Portfolio Banner](https://img.shields.io/badge/AI%20%26%20ML-Engineer-06b6d4?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-f97316?style=for-the-badge&logo=groq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**A modern, responsive, interactive, and containerized personal portfolio website showcasing AI/ML projects, Agentic RAG architectures, MLOps workflows, and research achievements.**

[Live GitHub Profile](https://github.com/ka1817) • [LinkedIn](https://linkedin.com/in/pranav-reddy-katta) • [Email](mailto:kattapranavreddy@gmail.com)

</div>

---

## 🌟 Key Highlights & Features

- ⚡ **Groq LLM AI Console (`llama-3.3-70b-versatile`)**: Integrated with your personal chatbot architecture ([`ka1817/LLM_Personal_Chatbot`](https://github.com/ka1817/LLM_Personal_Chatbot)) to answer natural language questions about your projects, internships, GATE rank, and stack.
- 🐘 **PostgreSQL Contact Form Integration**: Direct database connection to save contact submissions (`name`, `email`, `subject`, `message`, `created_at`) via `DATABASE_URL`.
- 🎨 **Executive UI/UX Design**: Clean, modern dark-mode aesthetic with custom glow animations, responsive typography, and theme selector (*Cyber Cyan*, *Neon Violet*, *Matrix Green*).
- 🌌 **Constellation Particle Physics Canvas**: Interactive neural background reacting to cursor movement and viewport sizing.
- 🗂️ **Filterable Projects Showcase**: Categorized by *Agentic AI & RAG*, *MLOps & Cloud*, *Healthcare & NLP*, and *Data Science*, featuring live GitHub repo links and interactive deep-dive architecture modals.
- 🔊 **Real-time Web Audio Synthesizer**: Subtle futuristic audio feedback synthesized natively via the Web Audio API with instant mute toggle.
- 📄 **Integrated Resume Viewer & Downloader**: Direct PDF viewer modal and one-click download.
- 🐳 **Dockerized & Production-Ready**: Multi-stage lightweight Dockerfile and Docker Compose configuration.

---

## ⚙️ Environment Variables Configuration

Create a `.env` file in the root directory (this file is excluded by `.gitignore` and `.dockerignore` for security):

```env
# Groq API Key (powers the interactive AI assistant with Llama-3.3-70B)
GROQ_API_KEY=your_groq_api_key_here

# PostgreSQL Database Connection String (stores contact form messages)
DATABASE_URL=postgresql://username:password@host:port/database_name
```

---

## 🚀 Quick Start (Local Development)

### 1. Run with Python FastAPI (Recommended)
```bash
# Clone repository
git clone https://github.com/ka1817/Personal-Website.git
cd Personal-Website

# Install dependencies
pip install -r requirements.txt

# Start FastAPI portfolio server
python app.py
```
Open your browser at **[http://localhost:8000](http://localhost:8000)**.

---

## 🐳 Docker Deployment

### Run with Docker Compose
```bash
docker compose up -d --build
```
Access the application on **[http://localhost:8000](http://localhost:8000)**.

---

## 📂 Project Architecture

```
Personal_Website/
├── app.py                  # FastAPI server with Groq LLM & PostgreSQL contact handlers
├── requirements.txt        # Python backend dependencies (FastAPI, Groq, psycopg2, asyncpg)
├── Dockerfile              # Production multi-stage Docker build
├── docker-compose.yml      # Container orchestration with .env support
├── .dockerignore           # Excluded build artifacts & credentials
├── .gitignore              # Git ignored patterns (securing .env)
├── index.html              # Modern, responsive portfolio interface
├── PranavR_Resume.pdf      # Official PDF Resume
├── static/
│   ├── css/
│   │   └── style.css       # Custom Cyberpunk & Glassmorphic styling
│   ├── js/
│   │   ├── main.js         # Interactivity, Groq AI console, contact dispatch
│   │   └── particles.js    # Interactive canvas constellation particle engine
│   └── assets/
│       └── PranavR_Resume.pdf
└── README.md               # Project documentation
```

---

## 📬 Contact & Connect

- **Name**: Katta Sai Pranav Reddy
- **Email**: [kattapranavreddy@gmail.com](mailto:kattapranavreddy@gmail.com)
- **GitHub**: [github.com/ka1817](https://github.com/ka1817)
- **LinkedIn**: [linkedin.com/in/pranav-reddy-katta](https://linkedin.com/in/pranav-reddy-katta)
- **Location**: Hyderabad, India (Open to Remote / Relocation)