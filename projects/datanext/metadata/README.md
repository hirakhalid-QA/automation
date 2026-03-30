# Datanext Metadata API Automation

This script runs 3 APIs in sequence using Playwright Python request context:

1. Login (`/api/accounts/login/`)
2. Create Media-File (`/api/media-files/`)
3. Create Manual-Metadata (`/api/manual-metadata/`) using `media_file_id` from step 2

## Folder Structure

```text
metadata/
  main.py
  requirements.txt
  README.md
  media/
  modules/
    auth_api.py
    media_api.py
    manual_metadata_api.py
    config.py
    http.py
    utils.py
```

## Default Behavior

- Picks a random file from `metadata/media/` each run.
- Uses `folder_id = 4` for both media-file and manual-metadata APIs.
- Generates:
  - random `batch_id` (UUID)
  - random `batch_sequence`
- Creates title/about automatically based on selected file name.

## Configuration (Optional via environment variables)

- `DATANEXT_BASE_URL` (default: `https://backend-kifal.stg.datanext.co`)
- `DATANEXT_LOGIN_EMAIL` (default: `zulkifal@betacodespk.com`)
- `DATANEXT_LOGIN_PASSWORD` (default: `c9#%SkVwJ7Mb`)
- `DATANEXT_FOLDER_ID` (default: `4`)
- `DATANEXT_POST_TITLE` (default: `Post title`)
- `DATANEXT_IGNORE_HTTPS_ERRORS` (`true`/`false`, default: `false`)

## Run

From inside `projects/datanext/metadata`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
python main.py
```

## Notes

- If login does not persist, verify your backend auth mode (cookie/session/token).
- If your environment has SSL interception/proxy issues, set `DATANEXT_IGNORE_HTTPS_ERRORS=true`.
