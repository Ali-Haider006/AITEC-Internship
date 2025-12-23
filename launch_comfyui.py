import os
import sys
import subprocess
import time
import webbrowser
import venv

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
REPO_URL = "https://github.com/comfyanonymous/ComfyUI.git"
COMFY_DIR = "ComfyUI"
VENV_DIR = "comfy_venv"

# -------------------------------------------------------------------
# UTILITY: run commands safely
# -------------------------------------------------------------------
def run(cmd, cwd=None):
    subprocess.check_call(cmd, shell=True, cwd=cwd)

# -------------------------------------------------------------------
# VENV HELPERS
# -------------------------------------------------------------------
def create_virtual_env():
    if not os.path.exists(VENV_DIR):
        print("[INFO] Creating virtual environment...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    else:
        print("[INFO] Virtual environment already exists.")

def venv_python():
    """Return python path inside the venv."""
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

# -------------------------------------------------------------------
# SYSTEM COMPATIBILITY CHECKS
# -------------------------------------------------------------------
def check_python_version():
    major, minor = sys.version_info[:2]
    print(f"[INFO] Python version: {major}.{minor}")
    if major != 3 or minor < 10:
        raise SystemExit("[ERROR] Python 3.10+ is required.")

def check_pytorch_and_cuda(venv_python):
    print("[INFO] Checking PyTorch & CUDA inside the venv...")
    try:
        cmd = (
            f'"{venv_python}" -c "import torch; '
            'print(torch.__version__); '
            'print(torch.version.cuda); '
            'print(torch.cuda.is_available())"'
        )
        output = subprocess.check_output(cmd, shell=True, text=True).splitlines()

        torch_version = output[0]
        cuda_version = output[1]
        cuda_available = output[2] == "True"

        print(f"[INFO] PyTorch version: {torch_version}")
        print(f"[INFO] CUDA built-in version: {cuda_version}")
        print(f"[INFO] CUDA available: {cuda_available}")

        if cuda_version == "None":
            print("[WARNING] This is a CPU-only PyTorch build. ComfyUI will run slowly on CPU.")
        else:
            print("[INFO] GPU acceleration is available.")

    except Exception as e:
        print("[WARNING] Could not import torch inside the venv yet.")
        print(f"[WARNING] Exception: {e}")
        print("[WARNING] This is normal BEFORE first install.")

# -------------------------------------------------------------------
# INSTALLATION: clone & install deps
# -------------------------------------------------------------------
def clone_comfyui():
    if not os.path.exists(COMFY_DIR):
        print("[INFO] Cloning ComfyUI repository...")
        run(f"git clone {REPO_URL}")
    else:
        print("[INFO] ComfyUI folder already exists. Skipping clone.")

def install_requirements():
    print("[INFO] Upgrading pip...")
    run(f"{venv_python()} -m pip install --upgrade pip")

    print("[INFO] Installing ComfyUI dependencies...")
    req_path = os.path.join(COMFY_DIR, "requirements.txt")
    run(f"{venv_python()} -m pip install -r {req_path}")

    print("[INFO] Dependencies installed.")

# -------------------------------------------------------------------
# LAUNCH COMFYUI
# -------------------------------------------------------------------
def launch_comfyui():
    print("[INFO] Starting ComfyUI server...")

    subprocess.Popen(
        [venv_python(), "main.py", "--listen", "127.0.0.1", "--port", "8188"],
        cwd=COMFY_DIR
    )

    print("[INFO] Waiting for ComfyUI to boot...")
    time.sleep(5)

    print("[INFO] Opening browser...")
    webbrowser.open("http://127.0.0.1:8188")

    print("\n====================================================")
    print(" ComfyUI is now running at:  http://127.0.0.1:8188")
    print("====================================================")

# -------------------------------------------------------------------
# MAIN EXECUTION FLOW
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("====================================================")
    print("       COMFYUI ONE-CLICK INSTALL & LAUNCHER         ")
    print("====================================================\n")

    check_python_version()
    create_virtual_env()
    clone_comfyui()
    install_requirements()
    check_pytorch_and_cuda(venv_python())
    launch_comfyui()
