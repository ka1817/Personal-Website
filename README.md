# Katta Sai Pranav Reddy — Personal Portfolio & AI Console

<div align="center">

![Portfolio Banner](https://img.shields.io/badge/AI%20%26%20ML-Engineer-06b6d4?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**A modern, responsive, interactive, and containerized personal portfolio website showcasing AI/ML projects, Agentic RAG architectures, MLOps workflows, and research achievements.**

[Live GitHub Profile](https://github.com/ka1817) • [LinkedIn](https://linkedin.com/in/pranav-reddy-katta) • [Email](mailto:kattapranavreddy@gmail.com)

</div>

---

## 🌟 Key Highlights & Features

- 🧠 **Interactive AI Terminal / Shell v2.4**: Type CLI commands (`about`, `skills`, `projects`, `gate`, `experience`, `resume`) or ask natural questions about Pranav's background, research, and stack.
- 🎨 **Modern Cyberpunk Glassmorphism UI**: Built with Tailwind CSS, custom glow animations, responsive typography, and theme selector (Cyber Cyan, Neon Violet, Matrix Green).
- 🌌 **Constellation Particle Physics Canvas**: Interactive neural background reacting to cursor movement and viewport sizing.
- 🗂️ **Filterable Projects Showcase**: Categorized by *Agentic AI & RAG*, *MLOps & Cloud*, *Healthcare & NLP*, and *Data Science*, featuring live GitHub repo links and interactive deep-dive architecture modals.
- 🔊 **Real-time Web Audio Synthesizer**: Subtle futuristic audio feedback on interaction with instant mute toggle (zero external audio file dependencies).
- 📄 **Integrated Resume Viewer & Downloader**: Direct PDF viewer modal and one-click download.
- 🐳 **Dockerized & Production-Ready**: Multi-stage lightweight Dockerfile and Docker Compose configuration for immediate zero-config deployment.

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

### Run with Docker CLI
```bash
# Build the Docker image
docker build -t saipranav-portfolio .

# Run container on port 8000
docker run -d -p 8000:8000 --name saipranav-portfolio saipranav-portfolio
```

---

## 📂 Project Architecture

```
Personal_Website/
├── app.py                  # FastAPI server with AI chat & stats endpoints
├── requirements.txt        # Python backend dependencies
├── Dockerfile              # Production multi-stage Docker build
├── docker-compose.yml      # Container orchestration
├── .dockerignore           # Excluded build artifacts
├── .gitignore              # Git ignored patterns
├── index.html              # Main interactive portfolio interface
├── PranavR_Resume.pdf      # Official PDF Resume
├── static/
│   ├── css/
│   │   └── style.css       # Custom Cyberpunk & Glassmorphic styling
│   ├── js/
│   │   ├── main.js         # Interactivity, AI console, audio synth & modals
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