"""Cache-busting for the CSS and JavaScript.

Browsers hold on to a stylesheet they have already seen, so a change can go
live and the person looking at the page still sees the old one. Appending a
version that changes whenever a file changes makes the URL itself new, which
is the only thing a browser reliably treats as a different asset.

The version is the newest modification time across static/css and static/js,
recomputed per request in development so an edit shows up on the next reload.
"""

from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

_WATCHED = ("css", "js")


def version() -> str:
    """Short token that changes whenever any stylesheet or script changes."""
    newest = 0.0

    for folder in _WATCHED:
        directory = STATIC_DIR / folder
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.is_file():
                newest = max(newest, path.stat().st_mtime)

    # Whole seconds are plenty: two edits inside one second still land
    # together, and the string stays short enough to read in devtools.
    return str(int(newest))
