"""Juice Tech — main entry point.

This is the only file you need to run. Python serves the whole site:

    Website      http://localhost:8000
    API docs     http://localhost:8000/docs

In PyCharm: pick "Juice Tech" from the run dropdown and press the green arrow.
From a terminal:  python main.py     (python3 main.py on Ubuntu and macOS)

The original React/TypeScript site still exists in src/ but is no longer
needed — the site is now plain HTML, CSS and JavaScript served by Python.
To run it anyway (it needs Bun installed):

    python main.py --with-react     ->  http://localhost:8080

Press Ctrl+C once to stop everything.
"""

# Keeps the "Path | None" annotations below parseable on Python 3.7-3.9, so
# this file reaches the version check instead of dying with a SyntaxError.
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit(
        f"Juice Tech needs Python 3.10 or newer. This is {sys.version.split()[0]}.\n\n"
        "  Ubuntu:  sudo apt install python3.12 python3.12-venv\n"
        "           then start it with:  python3.12 main.py\n"
        "  macOS:   brew install python@3.12\n"
        "  Windows: https://www.python.org/downloads/"
    )

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
        stderr = result.stderr.strip()

        # Debian and Ubuntu ship venv separately from Python itself, so
        # `python3 -m venv` fails out of the box with an ensurepip error.
        # That message does not say "install a package", so spell it out.
        if "ensurepip" in stderr or "python3-venv" in stderr:
            version = f"{sys.version_info.major}.{sys.version_info.minor}"
            sys.exit(
                "Could not create backend/.venv — the venv module is not installed.\n\n"
                f"{stderr}\n\n"
                "On Ubuntu or Debian, install it and run this again:\n"
                f"    sudo apt install python{version}-venv\n"
            )

        sys.exit(
            "Could not create backend/.venv.\n"
            f"{stderr}\n\n"            "Check that Python 3.10+ is installed and on your PATH."
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


def port_in_use(port: int) -> bool:
    """True if something is already listening on this port.

    Without this check, uvicorn dies with "WinError 10013: An attempt was made
    to access a socket in a way forbidden by its access permissions" — which
    sounds like a permissions problem and is really just a second copy of the
    server still running.
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def lan_address() -> str | None:
    """This machine's address on the local network, or None if offline.

    Opening a UDP socket to a public address makes the OS pick the interface
    it would actually route through — which is the one a phone on the same
    wifi can reach. Nothing is sent; UDP needs no handshake.
    """
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.4)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


def main() -> int:
    with_react = "--with-react" in sys.argv
    python = find_backend_python()

    if port_in_use(API_PORT):
        sys.exit(
            f"\nPort {API_PORT} is already in use — Juice Tech is probably\n"
            "already running in another window or terminal.\n\n"
            f"  Just open it:  http://localhost:{API_PORT}\n\n"
            "Or stop the other copy first. To find and stop it on Windows:\n"
            f"    netstat -ano | findstr :{API_PORT}\n"
            "    taskkill /F /PID <the number in the last column>\n"
        )

    processes: list[tuple[str, subprocess.Popen]] = []

    print("\n" + "=" * 58)
    print("  JUICE TECH — starting up")
    print("=" * 58)

    # --- The site + API, both served by Python ----------------------------
    # Bound to 0.0.0.0, not localhost, so a phone on the same wifi can open
    # the site and the station QR codes actually scan. That does mean anyone
    # on this network can reach it — which is the point at a demo, and not
    # something to leave running on a café connection.
    api = subprocess.Popen(
        # --proxy-headers lets the station QR encode the right address when the
        # site is reached through a tunnel: without it every URL the server
        # builds says "http", so a code scanned from an https link points at a
        # scheme the tunnel does not serve. A tunnel connects from 127.0.0.1,
        # which uvicorn trusts by default — so no --forwarded-allow-ips, whose
        # "*" Windows expands into a directory listing before uvicorn sees it.
        [str(python), "-m", "uvicorn", "app.main:app", "--reload",
         "--host", "0.0.0.0", "--port", str(API_PORT), "--proxy-headers"],
        cwd=BACKEND,
    )
    processes.append(("Website", api))
    print(f"  Website  http://localhost:{API_PORT}")
    print(f"  API docs http://localhost:{API_PORT}/docs")

    lan = lan_address()
    if lan:
        print()
        print(f"  On your phone (same wifi):  http://{lan}:{API_PORT}")
        print(f"  Scan the station QR from:   http://{lan}:{API_PORT}/how-it-works")
        print("  Open the site at that address first — the QR encodes")
        print("  whatever host you loaded the page from.")

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
