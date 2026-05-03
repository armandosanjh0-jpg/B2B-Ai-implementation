# B2B-Ai-implementation

## Local preview

```bash
python3 -m http.server 4173
```

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
