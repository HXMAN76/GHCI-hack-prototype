# VoiceBanker Project Documentation

## 1. Project Overview

### 1.1 Project Description
VoiceBanker is an AI-powered voice assistant for financial operations, designed for the GHCI 25 (Grace Hopper Celebration India) hackathon Theme 4. It enables users to perform secure banking tasks (balance inquiry, fund transfers, transaction history, loan inquiries, payment alerts) through natural voice conversations in Hindi, English, and Hinglish.

### 1.2 Problem Statement
*   **Target:** Non-English speakers, elderly users, digitally illiterate Indians (60%+ of population).
*   **Challenge:** Traditional mobile banking apps are complex, click-heavy, and exclusionary.
*   **Solution:** Voice-first interface making banking as natural as conversation.
*   **Requirements:** Secure authentication, contextual NLP, graceful error handling, multilingual support, compliance with banking standards.

## 2. Technical Architecture

### 2.1 Technology Stack
*   **Speech Recognition:** Vosk (offline, lightweight, supports Hindi/English/Hinglish)
*   **NLP Engine:** Rasa Open Source (context-aware dialogue management, intent recognition)
*   **Authentication:** Voice biometric (speaker embedding via resemblyzer/pyannote) + Voice OTP (Twilio)
*   **Banking Integration:** Mock APIs (MockBank.io, Open Bank Project) for development; real banking APIs for production
*   **Text-to-Speech:** Coqui TTS or eSpeak (open-source, multilingual)
*   **Backend:** Python FastAPI or Flask, PostgreSQL for user/transaction logs
*   **Frontend:** React web interface for testing and demo
*   **Infrastructure:** Docker/Docker Compose for local development, CI/CD via GitHub Actions
*   **Deployment:** Cloud-ready (AWS/GCP free tier or self-hosted)

### 2.2 Project Structure
```
voicebanker/  
├── backend/  
│ ├── asr/ # Vosk wrapper, audio preprocessing  
│ ├── nlu/ # Rasa models, custom actions  
│ ├── security/ # Voice biometric, OTP, authentication  
│ ├── banking_api/ # Banking API adapter, mock endpoints  
│ ├── tts/ # Text-to-speech wrapper  
│ └── main.py # FastAPI server  
├── frontend/  
│ ├── src/  
│ │ ├── components/ # Voice input, conversation display  
│ │ ├── pages/ # Dashboard, settings  
│ │ └── App.js  
│ └── package.json  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
├── .github/  
│ └── workflows/ # CI/CD pipelines  
├── docs/ # Technical documentation  
└── tests/ # Unit & integration tests
```

## 3. Development Guidelines & Checklists

### 3.1 Team Structure (4 Developers)
*   **Developer 1 (Backend/NLP Lead):** Rasa integration, banking API, custom actions, dialogue flow
*   **Developer 2 (Speech/Security):** Vosk ASR, voice biometrics, OTP, authentication flows
*   **Developer 3 (Frontend/UX):** Web UI, voice input/output handling, error messaging, user experience
*   **Developer 4 (DevOps/Integration):** Architecture, Docker, CI/CD, testing, deployment

### 3.2 Performance Optimization Priorities
1.  **ASR latency:** Optimize Vosk audio buffer size, preprocessing pipeline.
2.  **NLP latency:** Use lightweight Rasa model, cache intent weights.
3.  **API latency:** Connection pooling, response caching, async/await.
4.  **End-to-end latency:** Parallel processing where possible (fetch user data while generating TTS).
5.  **Memory footprint:** Efficient voice biometric storage, compress Rasa model.

### 3.3 Security & Compliance Checklist
*   ✅ Voice biometric secure storage (hashed embeddings)
*   ✅ OTP rate limiting (max 3 attempts)
*   ✅ Transaction audit logging
*   ✅ Session token expiration
*   ✅ HTTPS for all APIs
*   ✅ Input validation (amount, recipient, account number)
*   ✅ Fraud pattern detection (unusual amounts, rapid transfers)
*   ✅ RBI compliance for voice-based banking
*   ✅ Data privacy: on-device ASR (no cloud transmission)
*   ✅ GDPR-ready: user data export, deletion capabilities

### 3.4 Testing Coverage Requirements
*   **Unit tests:** 70%+ code coverage
*   **Integration tests:** All end-to-end flows
*   **Security tests:** Biometric bypass attempts, OTP brute-force, SQL injection
*   **Performance tests:** 100+ concurrent users, latency under load
*   **UAT:** 10+ diverse users (different ages, accents, technical literacy)

### 3.5 Deployment Checklist
*   [ ] Docker images built and tagged
*   [ ] CI/CD pipelines passing all tests
*   [ ] Environment variables documented
*   [ ] Database migrations tested
*   [ ] Load balancer configured (if multi-instance)
*   [ ] Logging and monitoring set up
*   [ ] Backup and disaster recovery procedures
*   [ ] Security scanning completed
*   [ ] Performance benchmarks documented
*   [ ] Demo environment accessible to judges

## 4. LLM Assistance Prompts (for Developers)

### 4.1 How to Use This Context for LLM Assistance
When asking an LLM for help, specify:
1.  **What you're working on:** "I'm working on Vosk ASR audio preprocessing for the VoiceBanker project"
2.  **Current issue:** "Audio noise is degrading transcription accuracy"
3.  **What you need:** "Give me Python code to implement spectral gating..."

### 4.2 Strategic Improvement Prompts for LLM

#### Prompt 1: Performance Optimization
**CURRENT ISSUE:** End-to-end conversation latency is 3.5 seconds per turn. Target: <2 seconds.
**Breakdown:**
*   Vosk ASR: 800ms
*   Rasa NLP inference: 600ms
*   Banking API call: 700ms
*   TTS generation: 400ms
**IMPROVEMENT REQUEST:** Identify bottlenecks and suggest optimization strategies with code examples. Prioritize parallelization and caching opportunities.
**Constraints:**
*   Cannot reduce ASR accuracy
*   API call time is network-dependent
*   Memory footprint must stay under 500MB

#### Prompt 2: Security Hardening
**SECURITY FOCUS AREAS:**
1.  Voice biometric spoofing (deepfakes, recorded voices)
2.  OTP interception or brute-force
3.  Replay attacks on transactions
4.  Unauthorized access to user data
**IMPROVEMENT REQUEST:** Design defense mechanisms for each threat. Suggest code implementations, testing strategies, and compliance measures (RBI/GDPR).
**Current defenses:** Voice biometric + OTP dual auth. What are the gaps?

#### Prompt 3: NLP Dialogue Robustness
**CURRENT CHALLENGE:** Users often ask vague or multi-intent queries like:
*   "I want to send money to Raj and check my balance"
*   "Can you tell me about my loan and set a reminder?"
*   "Transfer 5000 but first show me my last transaction with Priya"
**IMPROVEMENT REQUEST:** Design Rasa dialogue flows to handle:
1.  Multi-intent requests (sequential processing)
2.  Partial information (slot-filling across turns)
3.  Intent disambiguation (clarification questions)
Provide updated Rasa domain.yml, stories, and NLU training examples.

#### Prompt 4: Regional Adaptation
**CHALLENGE:** Vosk struggles with:
*   South Indian Tamil/Telugu accent mixing with Hindi
*   Northeast Indian English accent
*   Bengali-Hindi code-switching
*   Vernacular banking terms (lakh, crore, niyamit jama, etc.)
**IMPROVEMENT REQUEST:** Develop strategy for:
1.  Accent-specific Vosk model training
2.  Regional terminology mapping
3.  Banking term translation dictionaries
4.  Dialect-aware NLU training
Provide implementation roadmap and resource requirements.

#### Prompt 5: Error Recovery Flows
**CURRENT FLOWS:** When ASR confidence < 70%, system re-prompts: "Sorry, didn't catch that. Could you repeat?"
**PROBLEM:** Users get frustrated after 2-3 re-prompts. Needs graceful degradation.
**IMPROVEMENT REQUEST:** Design multi-level fallback strategies:
1.  Level 1: Re-prompt with hint ("Say account balance, transfer, or history")
2.  Level 2: Switch to clarification menu (numbered options read aloud)
3.  Level 3: Offer text input fallback
4.  Level 4: Transfer to human agent
Provide Rasa story examples and dialogue flow diagrams for each level.

#### Prompt 6: Testing Strategy Expansion
**COVERAGE GAPS:**
*   Concurrent multi-user conversations (not tested)
*   Transaction failures mid-flow (network timeout, API error)
*   Voice biometric with similar voices (twins, family members)
*   Rapid transaction sequences (potential fraud triggers)
**IMPROVEMENT REQUEST:** Design comprehensive test suites:
1.  Load testing scenario (50 concurrent users, 100 transactions/min)
2.  Chaos engineering: simulate API failures, network delays, ASR unavailability
3.  Biometric spoofing attempts with similar voices
4.  Edge cases: ₹0 balance, negative balance, account locked
Provide pytest/unittest code for automated testing.

#### Prompt 7: Feature Prioritization & MVP
**PROPOSED FEATURES (beyond MVP):**
*   Transaction prediction (ML model suggesting likely next action)
*   Voice pattern analytics (detect anomalies, fraud)
*   Scheduled transactions (voice command for recurring payments)
*   Investment inquiries (mutual fund balance, returns)
*   Credit score voice explanation
*   Multilingual automatic detection
**IMPROVEMENT REQUEST:**
1.  Prioritize features for MVP (hackathon submission)
2.  Identify quick wins (high impact, low effort)
3.  Design phased rollout for post-MVP
4.  Estimate effort for top-5 features
Provide feature vs. effort matrix with implementation suggestions.

#### Prompt 8: Code Quality & Maintainability
**CODEBASE CHALLENGES:**
*   Rasa custom actions becoming complex (200+ lines)
*   ASR preprocessing pipeline has duplicated logic
*   No consistent error handling pattern across modules
*   Insufficient logging for debugging production issues
**IMPROVEMENT REQUEST:**
1.  Refactor Rasa custom actions into modular service layer
2.  Extract ASR preprocessing into reusable utility class
3.  Design unified error handling middleware
4.  Implement structured logging (JSON format, severity levels)
Provide refactored code examples with before/after comparison.

#### Prompt 9: Deployment & Scalability
**CURRENT:** Docker Compose local setup works. Need to scale to production.
**SCALING CHALLENGES:**
*   Single Rasa server bottleneck
*   Voice biometric model loading (50MB) on every request
*   Database connection pooling not configured
*   No horizontal pod autoscaling
**IMPROVEMENT REQUEST:** Design Kubernetes deployment with:
1.  Rasa server scaling (3+ replicas with load balancing)
2.  In-memory caching layer for biometric models
3.  Database connection pooling (pgBouncer)
4.  Horizontal Pod Autoscaler (HPA) based on CPU/memory
5.  Service mesh observability (Prometheus, Grafana)
Provide Kubernetes manifests (Deployment, Service, HPA, ConfigMap).

#### Prompt 10: User Research & Iteration
**AFTER PHASE 4 UAT:** Received feedback from 10 users:
*   40% struggled with initial voice biometric enrollment (didn't know how to speak)
*   30% didn't trust the system (wanted additional confirmation)
*   20% wanted faster responses (latency > 2 seconds felt slow)
*   50% wanted Hindi-first interface (English seen as secondary)
*   1 user with speech impediment couldn't use voice input
**IMPROVEMENT REQUEST:**
1.  Redesign enrollment UX with on-screen guidance
2.  Add explicit transaction confirmation step with replay
3.  Optimize latency (see Prompt 1)
4.  Reverse UI language defaults (Hindi primary)
5.  Implement text input as parallel path for accessibility
Provide updated UI mockups, dialogue flows, and implementation checklist.

### 4.3 Quick Reference: Common Development Questions
*   **Q: "How do I improve Vosk accuracy for regional accents?"** → Use Prompt 4 (Regional Adaptation)
*   **Q: "Our transaction latency is too high."** → Use Prompt 1 (Performance Optimization)
*   **Q: "How do we handle voice spoofing attacks?"** → Use Prompt 2 (Security Hardening)
*   **Q: "Users get confused in multi-turn transactions."** → Use Prompt 3 (NLP Dialogue Robustness)
*   **Q: "Testing coverage feels incomplete."** → Use Prompt 6 (Testing Strategy Expansion)
*   **Q: "How do we decide what features to cut for MVP?"** → Use Prompt 7 (Feature Prioritization)
*   **Q: "Code is getting messy, what's best practice?"** → Use Prompt 8 (Code Quality)
*   **Q: "Need to scale beyond hackathon setup."** → Use Prompt 9 (Deployment & Scalability)
*   **Q: "UAT feedback is contradictory, how to prioritize?"** → Use Prompt 10 (User Research & Iteration)

## 5. Sharing & Integration

### 5.1 How to Share This with Your Team
1.  **Save as document:** Create a shared Google Doc/Notion page with this entire context.
2.  **LLM integration:** Use this as a system prompt in Claude Projects, OpenAI Assistants, or LangChain.
3.  **Quick snippets:** Share individual prompts via Slack/Discord when specific help is needed.
4.  **Weekly sync:** Review improvements suggested by LLM during team standups.
5.  **Git integration:** Add as `CONTEXT.md` in your repository for contributor onboarding.

This comprehensive context enables any LLM to provide highly relevant, project-aware assistance throughout development without repeating background information.
