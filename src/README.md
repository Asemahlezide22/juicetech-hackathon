# This folder is not the website any more

**Nothing you change in `src/` will appear on the Juice Tech site.**

This is the original React + TypeScript build. It has been replaced by a
Python site that serves every page, and it is kept only as a fallback.

## Edit these instead

| To change | Go to |
|---|---|
| A page's content or markup | `backend/templates/` |
| Styles | `backend/static/css/styles.css` |
| The kiosk demo's styles | `backend/static/css/kiosk.css` |
| Wording, prices, nav links | `backend/app/content.py` and `backend/app/config.py` |
| What the AI assistant says | `backend/app/policies/juice_tech_policies.md` |

## Run it

```bash
python main.py
```

Then open **http://localhost:8000**. Not `npm run dev` — that starts this old
build on a different port, and it is not what anyone is looking at.

First run creates `backend/.venv` and installs dependencies by itself. On
Ubuntu use `python3 main.py`, and install the venv module once with
`sudo apt install python3-venv`.

## Check your change worked

```bash
cd backend && python test_pages.py
```

There are four suites — `test_pages.py`, `test_kiosk.py`, `smoke_test.py` and
`test_late_fees.py`. Run them before pushing.

See `backend/README.md` for the full layout, and `PITCH.md` for the demo script.
