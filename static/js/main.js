
document.addEventListener("DOMContentLoaded", () => {
  let audioCtx = null;
  let soundEnabled = localStorage.getItem("sound_enabled") === "true";

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
  }

  function playTone(freq, type, duration, gainVal = 0.05) {
    if (!soundEnabled) return;
    try {
      initAudio();
      if (!audioCtx) return;
      if (audioCtx.state === "suspended") audioCtx.resume();

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = type || "sine";
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

      gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
      console.debug("Audio error:", e);
    }
  }

  function playClickSound() {
    playTone(800, "sine", 0.04, 0.03);
  }

  function playSuccessSound() {
    playTone(523.25, "triangle", 0.08, 0.05);
    setTimeout(() => playTone(659.25, "triangle", 0.12, 0.05), 60);
  }

  function playBlipSound() {
    playTone(1200, "sine", 0.03, 0.02);
  }

  // Sound Toggle Button
  const soundToggleBtn = document.getElementById("sound-toggle-btn");
  const soundIcon = document.getElementById("sound-icon");

  function updateSoundIcon() {
    if (soundIcon) {
      soundIcon.className = soundEnabled
        ? "fa-solid fa-volume-high text-xs text-cyan-400"
        : "fa-solid fa-volume-xmark text-xs text-slate-500";
    }
  }
  updateSoundIcon();

  if (soundToggleBtn) {
    soundToggleBtn.addEventListener("click", () => {
      soundEnabled = !soundEnabled;
      localStorage.setItem("sound_enabled", soundEnabled);
      updateSoundIcon();
      if (soundEnabled) {
        initAudio();
        playSuccessSound();
        showToast("Audio FX Enabled");
      } else {
        showToast("Audio FX Muted");
      }
    });
  }

  const cursor = document.getElementById("custom-cursor");
  const cursorDot = document.getElementById("custom-cursor-dot");

  if (cursor && cursorDot) {
    window.addEventListener("mousemove", (e) => {
      cursor.style.left = `${e.clientX}px`;
      cursor.style.top = `${e.clientY}px`;
      cursorDot.style.left = `${e.clientX}px`;
      cursorDot.style.top = `${e.clientY}px`;
    });

    document.querySelectorAll("a, button, input, textarea, .project-card, .term-chip").forEach((el) => {
      el.addEventListener("mouseenter", () => {
        cursor.classList.add("hovering");
        playBlipSound();
      });
      el.addEventListener("mouseleave", () => {
        cursor.classList.remove("hovering");
      });
    });
  }

  const typedTextEl = document.getElementById("typed-text");
  if (typedTextEl) {
    const roles = [
      "AI & Machine Learning Engineer",
      "Agentic RAG Architect",
      "MLOps & Docker Specialist",
      "Data Scientist & Fast-API Developer",
      "GATE 2026 DA (AIR 5262)"
    ];
    let roleIdx = 0;
    let charIdx = 0;
    let isDeleting = false;
    let typeDelay = 90;

    function typeLoop() {
      const currentRole = roles[roleIdx];

      if (isDeleting) {
        typedTextEl.textContent = currentRole.substring(0, charIdx - 1);
        charIdx--;
        typeDelay = 40;
      } else {
        typedTextEl.textContent = currentRole.substring(0, charIdx + 1);
        charIdx++;
        typeDelay = 90;
      }

      if (!isDeleting && charIdx === currentRole.length) {
        typeDelay = 2000;
        isDeleting = true;
      } else if (isDeleting && charIdx === 0) {
        isDeleting = false;
        roleIdx = (roleIdx + 1) % roles.length;
        typeDelay = 400;
      }

      setTimeout(typeLoop, typeDelay);
    }

    setTimeout(typeLoop, 800);
  }

  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const mobileIcon = document.getElementById("mobile-icon");

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
      const isOpen = !mobileMenu.classList.contains("hidden");
      mobileIcon.className = isOpen ? "fa-solid fa-xmark text-lg" : "fa-solid fa-bars text-lg";
      playClickSound();
    });

    document.querySelectorAll(".mobile-nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        mobileMenu.classList.add("hidden");
        if (mobileIcon) mobileIcon.className = "fa-solid fa-bars text-lg";
      });
    });
  }

  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");

  window.addEventListener("scroll", () => {
    let current = "";
    const scrollY = window.pageYOffset;

    sections.forEach((section) => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 120;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });

  const themeMenuBtn = document.getElementById("theme-menu-btn");
  const themeDropdown = document.getElementById("theme-dropdown");
  const themeOpts = document.querySelectorAll(".theme-opt");

  if (themeMenuBtn && themeDropdown) {
    themeMenuBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      themeDropdown.classList.toggle("hidden");
      playClickSound();
    });

    document.addEventListener("click", () => {
      themeDropdown.classList.add("hidden");
    });

    themeOpts.forEach((opt) => {
      opt.addEventListener("click", () => {
        const theme = opt.getAttribute("data-theme");
        document.body.setAttribute("data-theme", theme);
        localStorage.setItem("portfolio_theme", theme);
        themeDropdown.classList.add("hidden");
        playSuccessSound();
        showToast(`Theme switched to ${opt.innerText.trim()}`);
      });
    });

    const savedTheme = localStorage.getItem("portfolio_theme");
    if (savedTheme) {
      document.body.setAttribute("data-theme", savedTheme);
    }
  }

  const filterBtns = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      playClickSound();
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");

      projectCards.forEach((card) => {
        const category = card.getAttribute("data-category");
        if (filter === "all" || category === filter) {
          card.style.display = "flex";
          card.classList.add("animate-fade-in");
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  const projectDatabase = {
    bigbasket: {
      title: "BigBasket SmartCart – AI-Driven Shopping Assistant",
      subtitle: "Semantic Retrieval & Microservices Architecture",
      repo: "https://github.com/ka1817/BigBasket-SmartCart-AI-Assistant-for-BigBasket-Shopping",
      body: `
        <div class="space-y-4">
          <p class="text-slate-300">An intelligent conversational e-commerce search assistant engineered to replace rigid keyword search with intuitive semantic intent understanding.</p>
          
          <div class="bg-slate-950 p-4 rounded-xl border border-white/10 font-mono text-xs space-y-2">
            <div class="text-cyan-400 font-bold">System Architecture:</div>
            <div class="text-slate-300">User Query &rarr; FastAPI Endpoint &rarr; Embedding Model (Sentence-Transformers) &rarr; FAISS Index Search (Top-K) &rarr; Cross-Encoder Re-Ranking &rarr; Filtered Catalog Response</div>
          </div>

          <h4 class="font-bold text-white text-sm">Key Engineering Innovations:</h4>
          <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300">
            <li>Achieved <strong class="text-cyan-400">95% retrieval accuracy</strong> and a 0.89 relevance score using cross-encoder re-ranking.</li>
            <li>Containerized the entire stack with <strong class="text-purple-400">Docker</strong>, cutting end-to-end API response latency to ~2 seconds.</li>
            <li>Built automated CI/CD deployment pipelines using <strong class="text-emerald-400">GitHub Actions</strong> targeting AWS EC2 instances, reducing release cycles by 40%.</li>
          </ul>
        </div>
      `
    },
    churn: {
      title: "Netflix Customer Churn Prediction ML System",
      subtitle: "End-to-End MLOps Pipeline & Cloud Deployment",
      repo: "https://github.com/ka1817/Customer-Churn-Prediction-in-the-Telecom-Industry-Using-Machine-Learning",
      body: `
        <div class="space-y-4">
          <p class="text-slate-300">Production-grade machine learning system designed to anticipate subscriber churn through automated feature engineering and experiment tracking.</p>

          <div class="bg-slate-950 p-4 rounded-xl border border-white/10 font-mono text-xs space-y-2">
            <div class="text-purple-400 font-bold">MLOps Workflow:</div>
            <div class="text-slate-300">Raw Data &rarr; DVC Versioning (AWS S3) &rarr; MLflow Experiment Tracking & Metric Logging &rarr; Hyperparameter Tuning (Random Forest / XGBoost) &rarr; Containerized FastAPI API &rarr; GitHub Actions CI/CD to AWS EC2</div>
          </div>

          <h4 class="font-bold text-white text-sm">Key Engineering Innovations:</h4>
          <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300">
            <li>Attained <strong class="text-purple-400">99% model recall</strong> to effectively eliminate false negatives in customer churn risk.</li>
            <li>Conducted deep feature importance analysis (SHAP / EDA) identifying critical retention triggers.</li>
            <li>Implemented immutable artifact pipelines with DVC and AWS S3 for zero-loss experiment reproducibility.</li>
          </ul>
        </div>
      `
    },
    medical: {
      title: "Agentic RAG-Powered Medical Assistant",
      subtitle: "Multi-Agent Clinical Retrieval & Grounded Reasoning",
      repo: "https://github.com/ka1817/Agentic-RAG-Powered-Medical-Assistant",
      body: `
        <div class="space-y-4">
          <p class="text-slate-300">Autonomous multi-agent biomedical assistant capable of parsing complex clinical queries, retrieving scientific literature, and citing authoritative sources.</p>

          <div class="bg-slate-950 p-4 rounded-xl border border-white/10 font-mono text-xs space-y-2">
            <div class="text-emerald-400 font-bold">Agent Flow:</div>
            <div class="text-slate-300">User Clinical Query &rarr; Query Router & Reformulator Agent &rarr; Hybrid Dense/Sparse Retrieval (Pinecone / FAISS) &rarr; Fact Verification Agent &rarr; Structured Medical Summary with Citations</div>
          </div>

          <h4 class="font-bold text-white text-sm">Key Engineering Innovations:</h4>
          <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300">
            <li>Employs LangChain and LangSmith for real-time trace inspection and latency profiling.</li>
            <li>Eliminates hallucination through self-correcting retrieval loops and token-level citation attribution.</li>
          </ul>
        </div>
      `
    }
  };

  const projectModal = document.getElementById("project-modal");
  const modalProjectTitle = document.getElementById("modal-project-title");
  const modalProjectSubtitle = document.getElementById("modal-project-subtitle");
  const modalProjectBody = document.getElementById("modal-project-body");
  const modalRepoLink = document.getElementById("modal-repo-link");
  const closeProjectModal = document.getElementById("close-project-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");

  function openProjectModal(key) {
    const data = projectDatabase[key];
    if (!data) return;

    modalProjectTitle.textContent = data.title;
    modalProjectSubtitle.textContent = data.subtitle;
    modalProjectBody.innerHTML = data.body;
    modalRepoLink.href = data.repo;

    projectModal.classList.remove("hidden");
    playClickSound();
  }

  function hideProjectModal() {
    if (projectModal) projectModal.classList.add("hidden");
    playClickSound();
  }

  document.querySelectorAll(".project-details-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pKey = btn.getAttribute("data-project");
      openProjectModal(pKey);
    });
  });

  if (closeProjectModal) closeProjectModal.addEventListener("click", hideProjectModal);
  if (modalCloseBtn) modalCloseBtn.addEventListener("click", hideProjectModal);
  if (projectModal) {
    projectModal.addEventListener("click", (e) => {
      if (e.target === projectModal) hideProjectModal();
    });
  }

  const resumeModal = document.getElementById("resume-modal");
  const openResumeBtn = document.getElementById("open-resume-btn");
  const mobileResumeBtn = document.getElementById("mobile-resume-btn");
  const closeResumeModal = document.getElementById("close-resume-modal");

  function openResume() {
    if (resumeModal) resumeModal.classList.remove("hidden");
    playClickSound();
  }

  function closeResume() {
    if (resumeModal) resumeModal.classList.add("hidden");
    playClickSound();
  }

  if (openResumeBtn) openResumeBtn.addEventListener("click", (e) => { e.preventDefault(); openResume(); });
  if (mobileResumeBtn) mobileResumeBtn.addEventListener("click", (e) => { e.preventDefault(); openResume(); });
  if (closeResumeModal) closeResumeModal.addEventListener("click", closeResume);
  if (resumeModal) {
    resumeModal.addEventListener("click", (e) => {
      if (e.target === resumeModal) closeResume();
    });
  }

  const termForm = document.getElementById("terminal-form");
  const termInput = document.getElementById("terminal-input");
  const termOutput = document.getElementById("terminal-output");
  const termClearBtn = document.getElementById("terminal-clear-btn");
  const termChips = document.querySelectorAll(".term-chip");

  async function executeTerminalCommand(cmd) {
    const raw = cmd.trim();
    if (!raw) return;

    // Append User query
    const userLine = document.createElement("div");
    userLine.innerHTML = `<span class="text-slate-400 font-mono">pranav@ai-portfolio:~$</span> <span class="term-cmd-user">${escapeHtml(raw)}</span>`;
    termOutput.appendChild(userLine);
    playClickSound();

    const clean = raw.toLowerCase().replace(/[^a-z0-9\s_-]/g, "");

    if (clean === "clear" || clean === "cls") {
      termOutput.innerHTML = "";
      return;
    }

    // Thinking indicator
    const thinkingEl = document.createElement("div");
    thinkingEl.className = "text-slate-400 text-xs font-mono flex items-center gap-2 py-1";
    thinkingEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin text-cyan-400"></i> <span>Querying Groq LLM Assistant...</span>';
    termOutput.appendChild(thinkingEl);
    termOutput.scrollTop = termOutput.scrollHeight;

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: raw })
      });

      thinkingEl.remove();

      if (response.ok) {
        const data = await response.json();
        const res = document.createElement("div");
        res.innerHTML = `<div class="term-res-card text-xs leading-relaxed text-slate-200">${formatMarkdown(data.reply)}</div>`;
        termOutput.appendChild(res);
        termOutput.scrollTop = termOutput.scrollHeight;
        playSuccessSound();
        return;
      }
    } catch (e) {
      thinkingEl.remove();
    }

    // Client fallback if server is offline
    const res = document.createElement("div");
    res.innerHTML = `
      <div class="term-res-card text-xs text-slate-300">
        <p><strong>Sai Pranav Reddy</strong> is an AI & Machine Learning Engineer specializing in Agentic RAG architectures, MLOps (MLflow, DVC, Docker, AWS), and production data science systems.</p>
        <p class="mt-1 text-slate-400">Set your <code>GROQ_API_KEY</code> in <code>.env</code> to activate live conversational answers from Llama-3.3-70B.</p>
      </div>
    `;
    termOutput.appendChild(res);
    termOutput.scrollTop = termOutput.scrollHeight;
  }

  function formatMarkdown(text) {
    if (!text) return "";
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code class='bg-slate-800 text-cyan-300 px-1 rounded'>$1</code>")
      .replace(/\n/g, "<br/>");
  }

  if (termForm && termInput) {
    termForm.addEventListener("submit", (e) => {
      e.preventDefault();
      executeTerminalCommand(termInput.value);
      termInput.value = "";
    });
  }

  if (termClearBtn) {
    termClearBtn.addEventListener("click", () => {
      termOutput.innerHTML = "";
      playClickSound();
    });
  }

  termChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const cmd = chip.getAttribute("data-cmd");
      executeTerminalCommand(cmd);
    });
  });

  // -----------------------------------------------------------
  // 10. Contact Form Submissions (PostgreSQL)
  // -----------------------------------------------------------
  const contactForm = document.getElementById("contact-form");
  const contactStatus = document.getElementById("contact-status");
  const contactSubmitBtn = document.getElementById("contact-submit-btn");

  if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      playClickSound();

      const name = document.getElementById("contact-name").value;
      const email = document.getElementById("contact-email").value;
      const subject = document.getElementById("contact-subject").value;
      const message = document.getElementById("contact-message").value;

      if (contactSubmitBtn) {
        contactSubmitBtn.disabled = true;
        contactSubmitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Saving to Database...</span>';
      }

      try {
        const res = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, subject, message })
        });

        if (res.ok) {
          const data = await res.json();
          showContactSuccess(data.message || "Message recorded successfully!");
          return;
        }
      } catch (err) {
        console.debug("Backend contact submission error:", err);
      }

      // Fallback
      showContactSuccess("Thank you! Your message has been prepared for Sai Pranav.");
      const mailtoUrl = `mailto:kattapranavreddy@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent("From: " + name + " (" + email + ")\n\n" + message)}`;
      window.open(mailtoUrl, "_blank");
    });
  }

  function showContactSuccess(msgText) {
    playSuccessSound();
    showToast("Message Dispatched & Saved!");
    if (contactStatus) {
      contactStatus.textContent = msgText;
      contactStatus.classList.remove("hidden");
    }
    if (contactSubmitBtn) {
      contactSubmitBtn.disabled = false;
      contactSubmitBtn.innerHTML = '<i class="fa-solid fa-circle-check text-emerald-400"></i> <span>Message Sent</span>';
    }
    if (contactForm) contactForm.reset();
  }

  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const textToCopy = btn.getAttribute("data-copy");
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          playSuccessSound();
          showToast(`Copied "${textToCopy}" to clipboard!`);
        });
      }
    });
  });

  function showToast(msg) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = "toast-msg";
    toast.innerHTML = `<i class="fa-solid fa-circle-check text-cyan-400"></i> <span>${escapeHtml(msg)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.4s ease";
      setTimeout(() => toast.remove(), 400);
    }, 2800);
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
