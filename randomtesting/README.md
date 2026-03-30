# Random Testing - Reset Password (Isolated)

This folder is standalone and not linked with other project folders.

## What this runner does

Headed Playwright Python flow for reset-password testing:

1. Sign-in page load
2. Navigate to forgot-password
3. Empty email negative check
4. Invalid email negative check
5. Valid forgot-password submit
6. Reset link open (you paste link from email)
7. Mismatch password negative check
8. Successful password reset (you paste second link)
9. Login with old password should fail
10. Login with new password should pass
11. Reuse of used reset link should fail

## Setup

```bash
cd randomtesting
pip install -r requirements.txt
playwright install
```

## Run (headed)

```bash
python main.py \
  --email "your-email@domain.com" \
  --current-password "your-current-password"
```

The runner will ask for two fresh reset links during execution:
- link 1 for mismatch validation
- link 2 for successful reset

You can also pass them as arguments for non-interactive run:

```bash
python main.py \
  --email "your-email@domain.com" \
  --current-password "your-current-password" \
  --reset-link-1 "https://root.fordata.ai/reset-password?token=..." \
  --reset-link-2 "https://root.fordata.ai/reset-password?token=..."
```

## Proof Artifacts

Each run writes evidence in:

`randomtesting/artifacts/<timestamp>/`

- Screenshot per step (pass/fail)
- `api_calls.jsonl` with request/response status snapshots for forgot/reset calls
