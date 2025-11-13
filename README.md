# VoiceBanker

**VoiceBanker** is an AI-powered voice assistant for financial operations, designed for the GHCI 25 (Grace Hopper Celebration India) hackathon. It enables users to perform secure banking tasks (balance inquiry, fund transfers, transaction history, loan inquiries, payment alerts) through natural voice conversations in Hindi, English, and Hinglish.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15

### Option 1: Local Development (Recommended)

1. **Clone and setup environment:**
   ```bash
   git clone <repo>
   cd VoiceBanker
   cp .env.example .env
   ```

2. **Create and activate Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run PostgreSQL locally** (or use Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=voicebanker postgres:15`)

5. **Start backend:**
   ```bash
   uvicorn backend.main:app --reload
   ```
   Backend runs at `http://localhost:8000`

6. **Start frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend runs at `http://localhost:3000`

### Option 2: Docker Compose (Full Stack)

```bash
docker-compose up --build
```

This starts:
- Backend at `http://localhost:8000`
- Frontend at `http://localhost:3000`
- PostgreSQL at `localhost:5432`

## Project Structure

```
voicebanker/
├── backend/
│   ├── asr/              # Vosk ASR wrapper and audio preprocessing
│   ├── nlu/              # Rasa models and dialogue management
│   ├── security/         # Voice biometric, OTP, authentication
│   ├── banking_api/      # Banking API adapter and mock endpoints
│   ├── tts/              # Text-to-speech (Coqui/eSpeak)
│   └── main.py           # FastAPI entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React UI components
│   │   ├── pages/        # Page components
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   └── package.json
├── tests/                # Unit and integration tests (pytest)
├── docs/                 # Technical documentation
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Container orchestration
├── .env                  # Environment variables (create from .env.example)
└── PROJECT_DOCS.md       # Extended architecture and planning docs
```

## Key Development Commands

### Backend
```bash
# Start development server with auto-reload
uvicorn backend.main:app --reload

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=backend tests/
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm build

# Run tests
npm test
```

### Rasa NLU
```bash
cd backend/nlu

# Train Rasa model
rasa train

# Run Rasa server
rasa run

# Run custom actions server (in another terminal)
rasa run actions
```

### Docker
```bash
# Build and start all services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Run tests in backend container
docker-compose exec backend pytest
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.11, FastAPI |
| **ASR** | Vosk (offline-first) |
| **NLP** | Rasa Open Source |
| **Voice Biometric** | pyannote.audio, resemblyzer |
| **TTS** | Coqui TTS, eSpeak |
| **Database** | PostgreSQL 15 |
| **Frontend** | React 18, Axios |
| **Infrastructure** | Docker, Docker Compose |
| **Testing** | pytest, React Testing Library |
| **CI/CD** | GitHub Actions |

## Architecture Overview

```
┌─────────────────┐
│   React UI      │ (localhost:3000)
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────────────────────┐
│    FastAPI Backend              │ (localhost:8000)
├─────────────────────────────────┤
│  Orchestration & Routing        │
├──────┬──────┬──────┬──────┬─────┤
│ ASR  │ NLU  │ TTS  │ SEC  │ API │
│ (Vosk)│(Rasa)│(Coqui)│(OTP) │(Adapter)
├─────────────────────────────────┤
│    PostgreSQL Database          │
└─────────────────────────────────┘
```

## Security & Privacy

- **Voice Biometric**: Hashed embeddings stored securely in `backend/security`
- **Offline First**: Vosk ASR runs locally; no raw audio sent to cloud
- **OTP Authentication**: Rate-limited (max 3 attempts, 10-min expiry)
- **Audit Logging**: All transactions logged to PostgreSQL
- **HTTPS Ready**: Configuration for production deployment

See `PROJECT_DOCS.md` for complete security checklist.

## Testing

### Run All Tests
```bash
pytest -v
```

### Test Coverage
```bash
pytest --cov=backend --cov-report=html
# Open htmlcov/index.html
```

### Test Specific Module
```bash
pytest tests/test_api.py -v
pytest tests/asr_*.py -v
```

## Environment Variables

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `API_SECRET_KEY`: JWT secret (change in production)
- `BACKEND_PORT`: FastAPI port (default 8000)
- `VOSK_SAMPLE_RATE`: Audio sample rate (default 16000)
- `BIOMETRIC_THRESHOLD`: Voice match confidence (0-1, default 0.75)

## API Endpoints

- **GET** `/` - Health check
- **GET** `/health` - Service status
- *(More endpoints coming as modules are developed)*

See `backend/main.py` for current endpoints.

## LLM Assistance & Prompts

This repo includes `prompts.md` with pre-written context and prompt templates for LLM-assisted development. Use these when asking an AI for code improvements:

- **Prompt 1**: Performance Optimization (latency targets)
- **Prompt 2**: Security Hardening (biometric, OTP, compliance)
- **Prompt 3**: NLP Dialogue Robustness (multi-intent handling)
- **Prompt 4**: Regional Adaptation (accents, code-switching)
- **Prompt 5**: Error Recovery Flows (graceful degradation)
- **Prompt 6**: Testing Strategy (coverage, edge cases)
- **Prompt 7**: Feature Prioritization & MVP
- **Prompt 8**: Code Quality & Refactoring
- **Prompt 9**: Deployment & Kubernetes
- **Prompt 10**: User Research & Iteration

See `.github/copilot-instructions.md` for AI agent guidelines.

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Reset database (⚠️ deletes data)
docker-compose down -v
docker-compose up postgres
```

### Import Errors
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Contributing

See `CONTRIBUTING.md` for detailed development guidelines, code style, and PR requirements.

## Documentation

- **`PROJECT_DOCS.md`** - Architecture, team structure, development phases, LLM prompt templates
- **`prompts.md`** - Ready-to-use system prompts for AI-assisted development
- **`.github/copilot-instructions.md`** - Guidelines for AI coding agents
- **`docs/`** - Technical documentation (APIs, deployment, troubleshooting)

## Performance Targets

- **ASR Accuracy**: 85%+ for diverse accents
- **NLP Intent Recognition**: 90%+
- **Voice Biometric FAR**: <1%, FRR <5%
- **Conversation Latency**: <2 seconds per turn
- **System Uptime**: 99.5%

## Team Roles

- **Backend/NLP Lead**: Rasa integration, banking API, dialogue flow
- **Speech/Security**: Vosk ASR, voice biometrics, OTP, authentication
- **Frontend/UX**: React UI, voice input/output, error messaging
- **DevOps/Integration**: Docker, CI/CD, testing, system integration

## License

[Add your license here]

## Contact & Support

- **Project Owner**: [Add contact info]
- **Team Slack**: [Channel]
- **Issue Tracker**: GitHub Issues
- **Docs**: See `PROJECT_DOCS.md`

---

**Last Updated**: November 2025
