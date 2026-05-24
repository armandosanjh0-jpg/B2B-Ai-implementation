# Fulcrum AI — Website

Marketing site for Fulcrum AI, an AI workflow implementation agency for lean teams.
Static HTML/CSS — no build step, no dependencies.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home / positioning + services overview |
| `services.html` | Four service tiers + pricing |
| `how-it-works.html` | 6-step process |
| `use-cases.html` | Use cases by team type |
| `faq.html` | FAQ |
| `about.html` | About / philosophy |
| `book-a-call.html` | Lead form (Web3Forms) + Calendly booking |
| `confirmation.html` | Post-submit thank-you (noindex) |
| `contact.html` | Contact options |
| `privacy.html`, `terms.html` | Legal (Canada / PIPEDA) |
| `404.html` | Not-found page |

## ⚠️ Before you go live — required

The site is wired up but two values are placeholders. **Submissions will not be
delivered until you set the Web3Forms key.**

1. **Web3Forms access key** (lead capture → your inbox)
   - Go to <https://web3forms.com>, enter `dosa53@outlook.com`, and copy the
     access key emailed to you instantly (no account needed).
   - In `book-a-call.html`, replace `YOUR_WEB3FORMS_ACCESS_KEY` with that key.
   - Submit a test from the live page and confirm the email arrives.

2. **Calendly** — the widget points to `calendly.com/armandosanjh0` and is live.
   ⚠️ The live event is currently **"30 Minute Meeting"**, but the site copy says
   **"20-minute call"** throughout. Make them match: either create/rename a
   20-minute event in Calendly (recommended — lower commitment lifts bookings) or
   find-and-replace "20-minute"/"20 minutes" → "30" across the HTML.

## Recommended before launch

3. **Domain in metadata** — canonical tags, `sitemap.xml`, and `robots.txt`
   currently use `https://fulcrumai.com/`. Find-and-replace that with your real
   domain once chosen. If using the default GitHub Pages URL, it will be
   `https://armandosanjh0-jpg.github.io/B2B-Ai-implementation/`.

4. **Analytics** — each page has a marked comment in `<head>`:
   `<!-- Analytics: paste your Plausible/Umami/GA snippet here. -->`
   Paste your tracking snippet (e.g. [Plausible](https://plausible.io) — privacy-
   friendly, no cookie banner needed) into every page at that spot.

5. **Governing law** — `terms.html` has a `[your Province]` placeholder. Set it.

6. **Social share image** — add an `og:image` meta tag + a 1200×630 PNG once you
   have brand art, so links preview nicely.

## Deploy (GitHub Pages — free)

1. Push to the `main` branch.
2. Repo → **Settings → Pages**.
3. Source: **Deploy from a branch** → Branch: `main` → Folder: `/ (root)` → Save.
4. Wait ~1 min; your site is live at the URL shown there.
5. (Optional) Add a custom domain in that same Pages settings screen, then create
   a `CNAME` file in the repo root containing just your domain, and point your
   DNS to GitHub Pages.

`.nojekyll` is included so GitHub Pages serves the files as-is.

### Alternatives
- **Netlify / Vercel**: drag-and-drop the folder or connect the repo. Both detect
  it as a static site automatically — no config needed.

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Marketing

See [`MARKETING-PLAN.md`](MARKETING-PLAN.md) for the go-to-market plan, ICP,
channels, outreach templates, and 90-day playbook.
