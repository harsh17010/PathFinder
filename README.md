# 🧭 Pathfinder — AI-Powered Personalized Learning Path Recommender

**HackEarth Amplified · Round 2 Submission**

Pathfinder is a conversational learning assistant that turns a learner's natural-language goal into a structured, explainable, and adaptive learning roadmap. It uses semantic search, prerequisite graph algorithms, and retrieval-augmented generation to recommend the right courses in the right order — and explain why.

---

## ✨ Features

- **🗣️ Conversational Interface** — Describe your learning goal in natural language
- **👤 Learner Profiling** — Captures skills, interests, and parsed goals via LLM
- **🎯 Smart Recommendations** — Hybrid engine: semantic embeddings + prerequisite-aware filtering
- **🗺️ Learning Path Generator** — DAG-based topological sort guarantees correct course ordering
- **💡 Explainable AI** — Every recommendation grounded in real data (RAG-based)
- **📊 Progress Dashboard** — Skill radar chart, milestone tracker, adaptive feedback loop

## 🏗️ Architecture

```
Conversational Interface → Learner Profiling → Recommendation Engine
    → Learning Path Generator → Explainable AI → Progress Dashboard
                    ↺ Feedback loop closes back to profiling
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + TypeScript + TailwindCSS v3 + Recharts |
| Backend | FastAPI (Python, async) |
| Database | PostgreSQL 16 + pgvector (Docker) |
| LLM | Ollama (local) with LLM abstraction layer |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384-dim) |
| Graph Logic | networkx (topological sort on prerequisite DAG) |

## 📁 Project Structure

```
PathFinder/
├── frontend/                # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/      # UI components (Navbar, Layout)
│   │   ├── pages/           # HomePage, ChatPage, DashboardPage, PathPage
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript interfaces
│   └── ...
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # FastAPI route handlers
│   │   ├── core/              # Config, database, embeddings
│   │   ├── models/            # 13 SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── services/          # LLM abstraction (Ollama/Claude)
│   │   ├── main.py            # FastAPI app entry point
│   │   └── seed.py            # Database seeder with validation
│   └── data/
│       ├── skills.json        # 60 skills across 5 tracks
│       └── courses.json       # ~120 courses with prerequisite chains
├── docker-compose.yml         # PostgreSQL + pgvector
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Ollama** (installed locally — [ollama.com](https://ollama.com))

### 1. Clone & Setup

```bash
git clone https://github.com/harsh17010/PathFinder.git
cd PathFinder
```

### 2. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac

# Seed the database (validates data + generates embeddings)
python -m app.seed

# Start the API server
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 5. Start Ollama (separate terminal)

```bash
ollama pull llama3.1:8b
ollama serve
```

### 6. Access the App

- **Frontend**: http://localhost:5173
- **Backend API docs**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432

## 🤖 AI/ML Techniques

| Technique | Purpose |
|---|---|
| Sentence Embeddings + Cosine Similarity | Semantic course matching |
| Graph Algorithms (Topological Sort on DAG) | Prerequisite-respecting course ordering |
| LLM Function Calling / Tool Use | Structured goal extraction from conversation |
| Retrieval-Augmented Generation (RAG) | Grounded, explainable recommendations |
| Rule-based Adaptive Re-ranking | Feedback-driven path adjustment |
| KMeans Clustering *(optional)* | Peer-based recommendation signal |

## 📊 Dataset

- **60 skills** across 5 tracks: Data Science, Web Development, Cloud & DevOps, Cybersecurity, Mobile Development
- **~120 courses** with proper prerequisite chains forming a valid DAG
- **8 validation checks** run before seeding: duplicates, missing skills, invalid prereqs, self-prereqs, cycles, difficulty, rating, duration

## 📝 License

MIT
