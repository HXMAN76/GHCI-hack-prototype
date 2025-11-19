import os
import subprocess
import time
from dotenv import load_dotenv

# ============================================================
# LOAD .env AUTOMATICALLY
# ============================================================
print("\n🔧 Loading environment variables from .env ...")
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    print("❌ ERROR: GROQ_API_KEY not found in .env")
    exit(1)

print(f"✅ GROQ_API_KEY loaded: {groq_key[:10]}**********")

# ============================================================
# ACTIVATE VENV PATHS (cross-platform)
# ============================================================
VENV_PYTHON = None

if os.name == "nt":  # Windows
    VENV_PYTHON = ".venv\\Scripts\\python.exe"
else:  # macOS / Linux
    VENV_PYTHON = ".venv/bin/python"

if not os.path.exists(VENV_PYTHON):
    print("❌ ERROR: Virtual environment not found. Did you run:")
    print("   python -m venv .venv")
    exit(1)

print(f"✅ Using Python interpreter: {VENV_PYTHON}")

# ============================================================
# START ACTION SERVER
# ============================================================
def start_action_server():
    print("\n🚀 Starting Rasa Action Server on port 5055 ...")

    return subprocess.Popen(
        [VENV_PYTHON, "-m", "rasa_sdk.endpoint"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

# ============================================================
# START RASA MAIN SERVER
# ============================================================
def start_rasa_server():
    print("\n🚀 Starting Rasa Server on port 5005 ...")

    return subprocess.Popen(
        [VENV_PYTHON, "-m", "rasa", "run", "--enable-api", "--cors", "*", "--debug"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

# ============================================================
# PRINT LOGS CLEANLY
# ============================================================
def stream_output(process, name):
    for line in iter(process.stdout.readline, ''):
        print(f"[{name}] {line}", end='')

# ============================================================
# MAIN STARTUP PROCESS
# ============================================================
if __name__ == "__main__":
    print("\n=========================================")
    print("   🚀 Starting VoiceBanker (Rasa + Groq) ")
    print("=========================================\n")

    action_proc = start_action_server()
    time.sleep(3)

    rasa_proc = start_rasa_server()
    time.sleep(3)

    print("\n📡 Both services launched successfully!")
    print("👉 Action Server : http://localhost:5055/webhook")
    print("👉 Rasa Server   : http://localhost:5005\n")
    print("⚡ Press CTRL + C to stop all services.\n")

    try:
        # Continuously print logs
        while True:
            if action_proc.poll() is not None:
                print("❌ Action server stopped unexpectedly!")
                break
            if rasa_proc.poll() is not None:
                print("❌ Rasa server stopped unexpectedly!")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers ...")
        action_proc.terminate()
        rasa_proc.terminate()
        print("✔ All services stopped.")
