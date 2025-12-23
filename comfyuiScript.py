import sys
import subprocess
import torch

def check_python_version():
    major, minor = sys.version_info[:2]
    print(f"[INFO] Python version detected: {major}.{minor}")
    if major != 3 or minor < 10:
        raise SystemExit("[ERROR] Python 3.10+ is required for ComfyUI.")

def check_cuda():
    print("[INFO] Checking CUDA availability...")
    if torch.cuda.is_available():
        print(f"[INFO] CUDA is available: {torch.version.cuda}")
        print(f"[INFO] GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("[WARNING] CUDA is NOT available.")
        print("[WARNING] ComfyUI will run on CPU (slow).")
        print("[WARNING] Check that:")
        print(" - You installed the CUDA-enabled PyTorch wheel")
        print(" - You have compatible NVIDIA drivers installed")

def check_torch_version():
    print(f"[INFO] PyTorch version: {torch.__version__}")
    cuda = torch.version.cuda

    if cuda is None:
        print("[INFO] This is a CPU-only PyTorch build.")
        return

    major, minor = map(int, cuda.split('.'))
    print(f"[INFO] PyTorch was built with CUDA {major}.{minor}")

    # Example known compatible CUDA versions
    supported_cuda_versions = [(11, 8), (12, 1), (12, 4)]

    if (major, minor) not in supported_cuda_versions:
        print(f"[WARNING] CUDA {major}.{minor} is not a commonly tested build.")
        print("[WARNING] It may still work, but compatibility is not guaranteed.")
    else:
        print("[INFO] CUDA version is in a supported range.")

def run_system_checks():
    print("===============================================")
    print("           SYSTEM COMPATIBILITY CHECK          ")
    print("===============================================")

    try:
        check_python_version()
        check_torch_version()
        check_cuda()
        print("===============================================")
        print("[OK] System compatibility validated.")
        print("===============================================")
    except Exception as e:
        print("===============================================")
        print("[FAILED] Compatibility check failed.")
        print("===============================================")
        raise

# Call this at the top of your launcher
if __name__ == "__main__":
    run_system_checks()
