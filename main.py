"""Juice Tech — main entry point.

This is the only file you need to run. Python serves the whole site:

    Website      http://localhost:8000
    API docs     http://localhost:8000/docs

In PyCharm: pick "Juice Tech" from the run dropdown and press the green arrow.
From a terminal:  python main.py

The original React/TypeScript site still exists in src/ but is no longer
needed — the site is now plain HTML, CSS and JavaScript served by Python.
To run it anyway (it needs Bun installed):

    python main.py --with-react     ->  http://localhost:8080

Press Ctrl+C once to stop everything.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"

API_PORT = 8000
WEB_PORT = 8080


def find_backend_python() -> Path:
    """The Python inside backend/.venv, which has FastAPI installed."""
    candidate = BACKEND / ".venv" / "Scripts" / "python.exe"  # Windows
    if candidate.exists():
        return candidate

    candidate = BACKEND / ".venv" / "bin" / "python"  # macOS / Linux
    if candidate.exists():
        return candidate

    sys.exit(
        "Could not find backend/.venv.\n"
        "Create it once with:\n"
        f"    python -m venv {BACKEND / '.venv'}\n"
        f"    {BACKEND / '.venv' / 'Scripts' / 'python.exe'} -m pip install -r "
        f"{BACKEND / 'requirements.txt'}"
    )


def find_bun() -> Path | None:
    """Bun runs the legacy React site. Returns None if it is not installed."""
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    winget = (
        local
        / "Microsoft"
        / "WinGet"
        / "Packages"
        / "Oven-sh.Bun_Microsoft.Winget.Source_8wekyb3d8bbwe"
        / "bun-windows-x64"
        / "bun.exe"
    )
    if winget.exists():
        return winget

    from shutil import which

    found = which("bun")
    return Path(found) if found else None


def clear_stale_vite_temp() -> None:
    """Remove a leftover node_modules/.vite-temp folder.

    Vite writes this while it loads vite.config.ts and normally deletes it on
    exit. If the process is killed (or OneDrive still has a handle on it) the
    folder survives, and the next start dies with "EEXIST: mkdir .vite-temp".
    """
    stale = ROOT / "node_modules" / ".vite-temp"
    if not stale.exists():
        return

    import shutil

    try:
        shutil.rmtree(stale)
    except OSError as exc:
        print(f"  Warning: could not remove {stale}: {exc}")


def main() -> int:
    with_react = "--with-react" in sys.argv
    python = find_backend_python()

    processes: list[tuple[str, subprocess.Popen]] = []

    print("\n" + "=" * 58)
    print("  JUICE TECH — starting up")
    print("=" * 58)

    # --- The site + API, both served by Python ----------------------------
    api = subprocess.Popen(
        [str(python), "-m", "uvicorn", "app.main:app", "--reload", "--port", str(API_PORT)],
        cwd=BACKEND,
    )
    processes.append(("Website", api))
    print(f"  Website  http://localhost:{API_PORT}")
    print(f"  API docs http://localhost:{API_PORT}/docs")

    # --- Legacy React site, only on request -------------------------------
    if with_react:
        bun = find_bun()
        if bun is None:
            print("  React    SKIPPED — bun is not installed.")
            print("           Install it with:  winget install Oven-sh.Bun")
        else:
            clear_stale_vite_temp()
            web = subprocess.Popen([str(bun), "dev"], cwd=ROOT)
            processes.append(("React site", web))
            print(f"  React    http://localhost:{WEB_PORT}  (legacy)")

    print("=" * 58)
    print("  Press Ctrl+C to stop.\n")

    # --- Wait, and shut everything down together --------------------------
    try:
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n{name} stopped (exit code {proc.returncode}). Shutting down.")
                    raise KeyboardInterrupt
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping...")
        for name, proc in processes:
            if proc.poll() is None:
                proc.terminate()
        for name, proc in processes:
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()  # did not exit politely
        print("Stopped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
