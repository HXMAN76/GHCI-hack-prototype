## VoiceBanker — Copilot / AI agent instructions

Purpose: Give AI coding agents the minimal, actionable context to be productive in this repo.

1) Big-picture architecture (quick)
- Backend: Python FastAPI (entrypoint: `backend/main.py`), with modules: `backend/asr`, `backend/nlu`, `backend/security`, `backend/banking_api`, `backend/tts`.
- Frontend: React under `frontend/` (dev: `frontend/package.json`).
- Local infra: docker-compose for local dev; CI via `.github/workflows` (see `PROJECT_DOCS.md`).

2) Quick dev commands (discoverable patterns)
- Local containers: prefer `docker-compose up --build` if `docker-compose.yml` exists.
- Backend (python): `pip install -r requirements.txt` then `uvicorn backend.main:app --reload` from repo root.
- Rasa (NLU): look under `backend/nlu/` — train models with `rasa train` from that directory and run `rasa run` / `rasa run actions` for custom actions.
- Frontend: `cd frontend && npm install && npm start` if `frontend/package.json` is present.
- Tests: run `pytest -q` from repo root; add tests under `tests/` following existing test layout.

3) Project-specific conventions (do this when editing/generating code)
- Prefer small, focused changes: update a single component (ASR, NLU, TTS, security) and its tests in the same PR.
- Rasa custom actions -> keep logic lightweight: move complex business logic into `backend/banking_api` or a `services/` helper to keep actions readable.
- Voice biometric: embeddings are stored hashed/obfuscated in `backend/security` — never output raw embeddings or send raw audio to third‑party cloud in examples.
- Use the prompt templates in `prompts.md` for any LLM-assisted code: they contain concrete contexts and constraints (latency, memory, languages).

4) Integration points & external dependencies
- ASR: Vosk (offline-first). Changes to ASR preprocessing belong in `backend/asr/` and must keep offline constraint.
- NLP: Rasa models and training data live in `backend/nlu/` (intents, domain, stories, custom actions).
- Banking adapter: `backend/banking_api` contains the adapter and mock endpoints — use adapter pattern when adding real bank integrations.
- TTS: `backend/tts` — prefer Coqui/eSpeak wrappers; avoid cloud TTS without explicit approval.
- Auth: `backend/security` implements voice-biometric + OTP pattern. Respect rate-limits and audit logging rules described in `PROJECT_DOCS.md`.

5) What to generate and what to ask for permission on
- Safe to add: tests (pytest), small refactors that update imports, new utility modules under `backend/` that include tests.
- Ask a human before: introducing cloud-hosted ASR/TTS, changing authentication flow, adding external paid dependencies, or changing data retention/security behavior.

6) Examples to copy/modify
- When improving ASR: edit `backend/asr/*` and add tests in `tests/asr_*.py`. Keep changes offline-capable and include an example audio fixture.
- When changing NLU: update `backend/nlu/nlu.md` (or `nlu/` files), add training examples and a `tests/nlu_test.py` that asserts intent classification for representative utterances.

7) Security & privacy constraints (non-negotiable)
- Do not transmit raw audio or biometric embeddings to external services by default. If a change requires cloud audio, get explicit approval and document tradeoffs.
- Follow the checklist in `PROJECT_DOCS.md` (OTP rate-limiting, hashed biometric storage, HTTPS endpoints, audit logs).

8) Helpful files to inspect first
- `PROJECT_DOCS.md` — architecture, stacks, and prompts summary.
- `prompts.md` — ready-to-use LLM prompts and constraints; use these as system-context when asking for code or design help.

9) When uncertain, ask the human
- If a PR touches security/auth, PII handling, or adds an external integration, summarize proposed change and ask for owner sign-off.

If any section above is unclear or you want more examples (Rasa stories, ASR preprocessing snippets, CI steps), tell me which area to expand and I'll iterate.
