# Datanext Rootpanel Automation

Playwright Python + Pytest automation for the Datanext root panel.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

Create `.env` from `.env.example` and update the credentials if needed.

## Run

```bash
pytest tests/root/test_root_login.py
pytest tests/root/test_organizations.py
```

## Current Scope

- Root login
- Create organization through the 4-step wizard
- Edit root-side organization data through card menu modals

## Notes

- Organization head emails are generated from `hira.khalid+1@betacodespk.com` through `hira.khalid+99@betacodespk.com`
- If an email is already taken, the tests try the next available address
- Logo upload is intentionally skipped in this first version
