# Contributing to VoiceBanker

Thank you for contributing to VoiceBanker! This guide helps ensure consistent, high-quality contributions.

## Getting Started

1. **Fork and clone** the repository
   ```bash
   git clone <your-fork>
   cd VoiceBanker
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Code Style

**Python:**
- Follow **PEP 8** style guide
- Use `black` for formatting (line length 88)
- Use `flake8` for linting
- Use `isort` for import sorting

```bash
# Auto-format code
black backend/ tests/

# Check linting
flake8 backend/ tests/

# Sort imports
isort backend/ tests/
```

**JavaScript/React:**
- Follow **Airbnb JavaScript Style Guide**
- Use `prettier` for formatting
- Use `ESLint` for linting

```bash
cd frontend
npx prettier --write src/
npx eslint src/ --fix
```

### 2. Commit Messages

Use **conventional commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
```bash
git commit -m "feat(asr): add noise filtering to Vosk preprocessing"
git commit -m "fix(security): improve OTP rate limiting logic"
git commit -m "docs(api): update endpoint documentation"
```

### 3. Testing Requirements

**All contributions must include tests:**

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_api.py -v

# Check coverage (target: 70%+)
pytest --cov=backend tests/ --cov-report=html
```

**Test file naming:**
- `tests/test_api.py` - API endpoints
- `tests/asr_test.py` - ASR module tests
- `tests/nlu_test.py` - NLU module tests
- `tests/security_test.py` - Authentication tests
- `tests/banking_api_test.py` - Banking API tests

### 4. Code Review Checklist

Before submitting a PR, verify:

- [ ] Code follows PEP 8 / Airbnb style guide
- [ ] All tests pass (`pytest -v`)
- [ ] Test coverage maintained (70%+)
- [ ] Imports are sorted (`isort`)
- [ ] Code is formatted (`black`, `prettier`)
- [ ] No linting errors (`flake8`, `eslint`)
- [ ] Docstrings added for new functions/classes
- [ ] Commit messages follow conventional format
- [ ] No hardcoded secrets (use `.env` variables)
- [ ] No large binary files committed

## Component Guidelines

### Backend Modules

#### ASR (`backend/asr/`)
- Changes to ASR preprocessing must **keep offline constraint** (no cloud dependencies)
- Include example audio fixtures for testing
- Maintain compatibility with Vosk API
- Document sample rate assumptions

#### NLU (`backend/nlu/`)
- Update `nlu.md` (or appropriate `.yml` files) with training examples
- Train models with `rasa train` before committing
- Include representative test utterances in `tests/nlu_test.py`
- Verify intent classification accuracy (90%+)

#### Security (`backend/security/`)
- Never commit raw biometric embeddings or audio
- All embeddings must be hashed/obfuscated
- Follow OTP rate-limiting rules (max 3 attempts, 10-min expiry)
- Update security checklist in `PROJECT_DOCS.md` if adding new auth features

#### Banking API (`backend/banking_api/`)
- Use **adapter pattern** for adding new bank integrations
- Keep mock endpoints separate from real implementations
- Document API contracts with docstrings
- Include integration tests

#### TTS (`backend/tts/`)
- Prefer **Coqui/eSpeak wrappers** (offline, no cloud dependencies)
- Avoid cloud TTS without explicit approval
- Support multilingual output

### Frontend

- Keep components focused and reusable
- Use React hooks (no class components)
- Handle loading/error states explicitly
- Document props with PropTypes or TypeScript
- Test user interactions in `src/__tests__/`

## Security & Privacy Requirements

**Non-negotiable:**
1. Do NOT transmit raw audio to external services
2. Do NOT log biometric embeddings
3. Use hashed/obfuscated storage for voice data
4. Implement OTP rate limiting (max 3 attempts)
5. Follow audit logging requirements

See `PROJECT_DOCS.md` Security Checklist (§3.3) for complete guidelines.

## Documentation

### Code Documentation
- Add docstrings to all functions/classes (PEP 257 format)
- Include type hints for function arguments
- Document exceptions raised
- Provide usage examples for complex functions

**Example:**
```python
def transcribe_audio(audio_path: str, confidence_threshold: float = 0.7) -> dict:
    """
    Transcribe audio using Vosk ASR.
    
    Args:
        audio_path: Path to audio file (16-bit WAV, 16kHz sample rate)
        confidence_threshold: Minimum confidence score (0-1)
        
    Returns:
        dict with keys:
            - 'text': Transcribed text
            - 'confidence': Confidence score (0-1)
            - 'language': Detected language
            
    Raises:
        FileNotFoundError: If audio file not found
        ValueError: If audio format unsupported
        
    Example:
        >>> result = transcribe_audio('sample.wav')
        >>> print(result['text'])
    """
```

### PR Description
Include in PR body:
- **What**: Brief description of changes
- **Why**: Problem being solved
- **How**: Implementation approach
- **Testing**: How to verify changes
- **Breaking Changes**: Any API/behavior changes

## Performance Considerations

- **Backend latency**: Target <600ms per request
- **ASR latency**: Target <800ms for transcription
- **NLP latency**: Target <600ms for intent recognition
- **Memory footprint**: Keep below 500MB

Profile code before and after optimization:
```bash
# Generate profile (Python)
python -m cProfile -o profile.stats backend/main.py

# View results
python -m pstats profile.stats
```

## Branching Strategy

Use **feature branches** from `master`:

```bash
# Feature branch
git checkout -b feature/new-banking-intent

# Bugfix branch
git checkout -b fix/otp-rate-limiting

# Documentation branch
git checkout -b docs/deployment-guide
```

## Pull Request Process

1. **Push your branch**
   ```bash
   git push origin feature/your-feature
   ```

2. **Open PR on GitHub**
   - Provide clear PR title: `feat(asr): implement noise filtering`
   - Link related issues: `Closes #42`
   - Add description from template
   - Add `@username` for code reviewers

3. **Address review feedback**
   ```bash
   # Make changes
   git add .
   git commit -m "fix: address review feedback on PR #50"
   git push
   ```

4. **Merge to master**
   - Squash commits if multiple: `git rebase -i`
   - Delete branch after merge

## Reporting Issues

Use GitHub Issues with template:

```markdown
**Describe the bug**
Brief description of the issue

**Steps to reproduce**
1. ...
2. ...

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- Python version: 3.11
- OS: Ubuntu 22.04
- Branch: master

**Logs/Screenshots**
Include relevant logs or screenshots
```

## Getting Help

- **Questions**: Post in project Slack or GitHub Discussions
- **Documentation**: See `PROJECT_DOCS.md` and `README.md`
- **LLM Assistance**: Use prompts in `prompts.md` for code help
- **Architecture Questions**: Refer to `.github/copilot-instructions.md`

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others grow and learn
- Report harmful behavior to project maintainers

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` (maintained per team preference)
- GitHub contributor graph
- Release notes for major features

---

**Thank you for making VoiceBanker better! 🎉**
