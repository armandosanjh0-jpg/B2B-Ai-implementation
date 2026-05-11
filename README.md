# B2B-Ai-implementation

## Local preview

```bash
python3 -m http.server 4173
```

## Production checks

```bash
npm test
```

This runs `scripts/validate_site.py` to catch broken internal links and enforce booking form requirements.

## Booking flow

- `book-a-call.html` includes a production form (`POST`) configured for Netlify Forms.
- Successful submissions redirect to `confirmation.html`, where users can continue to a scheduling link.
- If submission fails, users are redirected to `booking-error.html` with retry instructions.
- A `404.html` page is included for better production fallback handling.

## Install Playwright

```bash
npm run install:playwright
```

If your environment blocks npm registry access, run this command in your CI/CD or local network where npm access is allowed.

## Screenshot capture (Chromium hardened)

```bash
python3 scripts/capture_screenshots.py --base-url http://127.0.0.1:4173
```

This script launches Chromium with extra stability flags (`--disable-dev-shm-usage`,
`--disable-gpu`, `--single-process`, `--no-sandbox`) and writes screenshots to `artifacts/`.


## Client access

- `login.html` provides client sign-in UI.
- `portal.html` provides the post-login workspace shell for onboarding/docs/support.
- Replace static login/portal wiring with your auth provider (Supabase/Auth0/Firebase) before handling real credentials in production.
