"""Re-run the calling script under backend/.venv.

The test scripts need FastAPI and SQLModel, which only exist inside
backend/.venv. Rather than requiring every developer to register that
interpreter in their editor first, each script calls ensure_venv() and
re-launches itself under the right Python automatically.
"""

import os
import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent

# Set on the child process so it can never re-launch itself again.
_GUARD = "JT_VENV_BOOT"


def venv_python() -> Path | None:
    """Path to the virtualenv's Python, or None if it has not been created."""
    for candidate in (
        BACKEND_DIR / ".venv" / "Scripts" / "python.exe",  # Windows
        BACKEND_DIR / ".venv" / "bin" / "python",          # macOS / Linux
    ):
        if candidate.exists():
            return candidate
    return None


def ensure_venv() -> None:
    """Restart this script under backend/.venv unless already running there."""
    if os.environ.get(_GUARD) == "1":
        return  # this process IS the re-launched one

    python = venv_python()
    if python is None:
        # No virtualenv to switch to. Carry on and let the missing import
        # raise a normal, readable ImportError.
        return

    if Path(sys.executable).resolve() == python.resolve():
        return  # already the right interpreter

    env = {**os.environ, _GUARD: "1"}
    raise SystemExit(subprocess.call([str(python), *sys.argv], env=env))
