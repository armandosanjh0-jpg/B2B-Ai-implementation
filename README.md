# Novelle — Website

Marketing site for Novelle, an AI workflow implementation agency for lean teams.
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
   The site copy and the Calendly event now both say **30 minutes** — matched.
   Just confirm the event is published and titled clearly (e.g. "Discovery Call").

## Recommended before launch

3. **Domain in metadata** — canonical tags, `sitemap.xml`, and `robots.txt`
   currently use `https://NOVELLE-DOMAIN-TBD/`. Find-and-replace that with your real
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

## Outreach sales agent (Claude-powered)

Use `sales_agent.py` to generate personalized cold email + LinkedIn outreach for leads using your existing `OUTREACH-STRATEGY.md`.

### 1) Install dependencies

```sh
python3 -m pip install -r requirements-agent.txt
```

### 2) Set your Claude API key

```sh
export ANTHROPIC_API_KEY="{{ANTHROPIC_API_KEY}}"
```

### 3) Run the agent

```sh
python3 sales_agent.py --leads leads.sample.csv --output outreach_results.json
```

If you want every generated outreach record sent to your Zapier flow (e.g., to create/send Outlook drafts), set a Zapier Catch Hook URL:

```sh
export ZAPIER_WEBHOOK_URL="{{ZAPIER_WEBHOOK_URL}}"
python3 sales_agent.py --leads leads.sample.csv --output outreach_results.json
```

Or pass it directly:

```sh
python3 sales_agent.py --leads leads.sample.csv --output outreach_results.json --zapier-webhook-url "{{ZAPIER_WEBHOOK_URL}}"
```

### 4) Input/output

- Input CSV headers:
  `name, role, company, company_size, industry, notes`
- Output:
  `outreach_results.json` with lead score, fit tier, outreach angle, email draft, LinkedIn messages, and follow-ups.
  If Zapier is configured, each lead record is also POSTed as JSON to your webhook.

### Zapier payload fields

Each webhook request includes:
- Event fields:
  - `source`
  - `created_at`
  - `zapier_event`
  - `zapier_version`
- Lead fields:
  - `lead_name`
  - `lead_email`
  - `lead_role`
  - `lead_company`
  - `lead_company_size`
  - `lead_industry`
  - `lead_notes`
- Qualification fields:
  - `lead_score`
  - `fit_tier`
  - `outreach_angle`
- Outlook step input fields:
  - `outlook_to_email`
  - `outlook_to_name`
  - `outlook_subject`
  - `outlook_body`
- LinkedIn fields:
  - `linkedin_connect_note`
  - `linkedin_first_dm`
- Follow-up step input fields:
  - `followup_1_day_offset`
  - `followup_1_scheduled_at`
  - `followup_1_subject`
  - `followup_1_body`
  - `followup_2_day_offset`
  - `followup_2_scheduled_at`
  - `followup_2_subject`
  - `followup_2_body`

Compatibility fields are also included:
- `lead` (original lead object)
- `outreach` (raw Claude output)
- `outlook_draft` (nested object)
- `follow_up_plan` (nested array)
