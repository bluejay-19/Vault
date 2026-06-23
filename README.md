# 🔒 Vault — Your money. No excuses.

> A personal finance tracker with Frank — a blunt, witty raccoon who roasts your spending based on real numbers, not generic advice.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red) ![Supabase](https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-green) ![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-orange)

---

## What is Vault?

Vault lets you upload your monthly bank statement, enter your income and budget, and instantly get a brutally honest AI-generated breakdown of your spending from Frank — a raccoon persona powered by Groq's llama-3.3-70b-versatile model. Frank references your actual numbers, not boilerplate advice.

---

## Features

- **Upload** CSV or Excel monthly statements — adaptive category detection, no fixed format required
- **Dashboard** — 4 summary cards, budget vs actual progress bar, spending breakdown donut chart, savings trend line chart, and Frank's structured 4-part roast
- **Ask Frank** — ask a direct question about your spending and get a data-grounded answer
- **History** — month cards grid with verdict badges (Catastrophic / Survivable / Not Bad), Frank's overall verdict, regenerate on demand
- **Multi-currency** — AED, $, £, €, ZMW, R
- **Secure** — Supabase Row Level Security ensures users only access their own data

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (multipage) |
| Backend / Auth | Supabase (Postgres + RLS) |
| AI Persona | Groq API — llama-3.3-70b-versatile |
| Data Processing | Pandas |
| Charts | Plotly |
| Deployment | Streamlit Community Cloud |

---

## Project Structure
vault/

├── app.py                  # Landing page (entry point)

├── requirements.txt        # Pinned dependencies

├── .env                    # Local secrets (never committed)

├── .gitignore

├── .streamlit/

│   └── config.toml         # File upload size limit (10MB)

├── styles/

│   └── global.css          # Dark theme, typography, component styles

├── utils/

│   ├── init.py         # Shared helpers: load_css, check_auth, render_sidebar, get_supabase_client

│   └── logger.py           # File-based logging for Groq inputs/outputs

├── logs/

│   └── vault.log           # Runtime logs (gitignored)

└── pages/

├── 1_Login.py          # Email/password auth (login + signup)

├── 2_Dashboard.py      # Charts, summary cards, Frank's roast, Ask Frank

├── 3_Upload.py         # File upload, Pandas parsing, Supabase insert

└── 4_History.py        # Monthly history grid, verdict badges, overall verdict

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/bluejay-19/vault.git
cd vault
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file in the root**
SUPABASE_URL=your_supabase_project_url

SUPABASE_ANON_KEY=your_supabase_anon_key

GROQ_API_KEY=your_groq_api_key

**4. Run the app**
```bash
streamlit run app.py
```

---

## Upload File Format

Vault accepts CSV or Excel files with the following structure:

| Column | Required | Notes |
|---|---|---|
| Date | ✅ Yes | Any standard date format |
| food | Optional | |
| rent | Optional | |
| transport | Optional | |
| entertainment | Optional | |
| groceries | Optional | |
| subscriptions | Optional | |
| medical | Optional | |
| other | Optional | |

- Column names are **case-insensitive** — `Food`, `FOOD`, and `food` all work
- Missing categories default to `0` — no need to include all 8
- File size limit: **10MB**
- Supported formats: **CSV, XLSX**

---

## Supabase Schema

**Table: `uploads`**

| Column | Type | Notes |
|---|---|---|
| id | uuid | Auto-generated |
| user_id | uuid | Foreign key → auth.users |
| month | int2 | 1–12 |
| year | int2 | e.g. 2026 |
| income | float4 | |
| budget | float4 | |
| net_savings | float4 | Can be negative |
| total_spent | float4 | Computed by Pandas |
| category_breakdown | jsonb | `{"food": 461, "rent": 1200, ...}` |
| currency | text | Default: $ |
| created_at | timestamptz | Auto-generated |

RLS policies: users can only SELECT and INSERT their own rows.

---

## Security

- API keys stored in `.env` locally, Streamlit Secrets on deployment — never committed
- Supabase RLS enforces row-level data isolation per user
- Groq calls log metadata only (user_id, response length, latency) — no raw spending data in logs
- Input validation: income/budget capped at 1,000,000, net savings between -1,000,000 and 1,000,000
- File size capped at 10MB via `.streamlit/config.toml`
- Duplicate month uploads blocked at insert time

---

## Known Limitations

- Session lost on hard refresh (Streamlit limitation — re-login required)
- Forgot password flow not implemented in v1
- Multi-sheet Excel files read first sheet only
- Groq API rate limits not explicitly enforced (mitigated by single roast per page load)
- Korean language input responds in English (llama-3.3-70b behaviour)

---

## Built for

Decoding Data Science — 8-Day AI Application Building Challenge