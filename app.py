#!/usr/bin/env python
"""
Spin up both the Flask API (port 5000) and React-Vite dev server (port 3000)
with a single command:

    python app.py
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "FlaskBackend"
FRONTEND_DIR = ROOT / "ReactFrontEnd"
VENV_DIR = ROOT / "venv"          # top-level venv (optional)

# --------------------------------------------------------------------------- #
# Helper: pick the Python binary inside venv if it exists
# --------------------------------------------------------------------------- #
def python_from_venv(venv: Path) -> str | None:
    for rel in ("bin/python", "Scripts/python.exe"):   # mac/linux / windows
        candidate = venv / rel
        if candidate.exists():
            return str(candidate)
    return None


def main() -> None:
    python_exe = sys.executable  # Use system Python instead of venv

    backend_cmd = [python_exe, "run.py"]
    frontend_cmd = ["npm", "run", "dev", "--prefix", str(FRONTEND_DIR)]

    print("🚀  Launching SalesForecaster dev stack")
    print("  • BACKEND :", ' '.join(backend_cmd))
    print("  • FRONTEND:", ' '.join(frontend_cmd))
    print("  (Press Ctrl-C once to stop both)\n")

    processes: list[subprocess.Popen] = []

    try:
        # Start Flask
        processes.append(
            subprocess.Popen(
                backend_cmd,
                cwd=BACKEND_DIR,
                env={**os.environ, "PYTHONPATH": str(ROOT)},  # ensure App/ is importable
            )
        )

        # Start Vite
        processes.append(
            subprocess.Popen(
                frontend_cmd,
                cwd=ROOT,    # npm --prefix handles path
            )
        )

        # Wait for Ctrl-C or for either process to exit
        while True:
            for p in processes:
                if p.poll() is not None:            # one process exited
                    raise RuntimeError(
                        f"Process {p.args[0]} terminated with code {p.returncode}"
                    )
            signal.pause()                          # idle until signal
    except (KeyboardInterrupt, RuntimeError):
        print("\n🛑  Shutting down…")
        for p in processes:
            if p.poll() is None:                    # still running
                p.send_signal(signal.SIGINT)
        for p in processes:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
    finally:
        print("✅  Dev stack stopped.")


if __name__ == "__main__":
    main()