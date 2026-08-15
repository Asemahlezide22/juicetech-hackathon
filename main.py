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


def venv_python() -> Path | None:
    """The Python inside backend/.venv, or None if it does not exist yet."""
    for candidate in (
        BACKEND / ".venv" / "Scripts" / "python.exe",  # Windows
        BACKEND / ".venv" / "bin" / "python",          # macOS / Linux
    ):
        if candidate.exists():
            return candidate
    return None


def find_backend_python() -> Path:
    """The backend interpreter, creating it on first run.

    backend/.venv is deliberately not in git, so a fresh clone has no
    virtualenv and no dependencies. Rather than making somebody read the
    README before anything works, build it here — this runs once, then
    every later start finds it already there.
    """
    existing = venv_python()
    if existing is not None:
        return existing

    print("  First run: setting up backend/.venv (this takes a minute)…")

    result = subprocess.run(
        [sys.executable, "-m", "venv", str(BACKEND / ".venv")],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(
            "Could not create backend/.venv.\n"
            f"{result.stderr.strip()}\n\n"
            "Check that Python 3.10+ is installed and on your PATH."
        )

    python = venv_python()
    if python is None:
        sys.exit("backend/.venv was created but no interpreter was found inside it.")

    print("  Installing dependencies…")
    result = subprocess.run(
        [str(python), "-m", "pip", "install", "-q", "-r", str(BACKEND / "requirements.txt")],
    )
    if result.returncode != 0:
        # Leave the half-built venv in place; deleting it would also throw away
        # whatever did install, making the retry slower.
        sys.exit(
            "Dependency install failed. Fix the error above, then run:\n"
            f"    {python} -m pip install -r {BACKEND / 'requirements.txt'}"
        )

    print("  Setup complete.\n")
    return python


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
