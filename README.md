# 🔒 Vault — Your money. No excuses.

> A personal finance tracker with Frank, a blunt, witty raccoon who roasts your spending based on real numbers, not generic advice.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-F55036?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

</div>

---

## What is Vault?

Vault lets you upload your monthly statement/excel sheeet , enter your income and budget, and instantly get a brutally honest AI-generated breakdown of your spending from **Frank**; a raccoon persona powered by Groq's llama-3.3-70b-versatile model.

Frank references your actual numbers. Not boilerplate advice. Not gentle suggestions. Your numbers, no excuses.

---

## Features

| Feature | Description |
|---|---|
| 📤 **Upload** | CSV or Excel monthly statements — adaptive category detection, no fixed format required |
| 📊 **Dashboard** | 4 summary cards, budget vs actual bar, spending donut chart, savings trend line chart, and Frank's structured roast |
| 💬 **Ask Frank (Quick Question)** | Ask a direct question about your spending and get a data-grounded answer |
| 🕐 **History** | Month cards grid with verdict badges, Frank's overall verdict, regenerate on demand |
| 💱 **Multi-currency** | AED, USD, GBP, EUR, ZMW, ZAR |
| 🔒 **Secure** | Supabase Row Level Security — users only ever access their own data |

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

```
vault/
├── app.py                      # Landing page (entry point)
├── requirements.txt            # Pinned dependencies
├── test.py                     # Local testing script
├── .env                        # Local secrets (never committed)
├── .gitignore
│
├── .streamlit/
│   └── config.toml             # File upload size limit (10MB)
│
├── docs/
│   ├── exam_set.md             # 20 test scenarios + pass/fail results
│   └── evaluation.md           # Evaluation approach and metrics
│
├── pages/
│   ├── 1_Login.py              # Email/password auth (login + signup)
│   ├── 2_Dashboard.py          # Charts, summary cards, Frank's roast
│   ├── 3_Upload.py             # File upload, Pandas parsing, Supabase insert
│   └── 4_History.py            # Monthly history grid, verdict badges
│
├── styles/
│   └── global.css              # Dark theme, typography, component styles
│
├── test_data/                  # Sample CSV files for testing
│   └── *.csv
│
└── utils/
    └── __init__.py             # Shared helpers: load_css, check_auth, render_sidebar
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/bluejay-19/vault.git
cd vault
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## Upload File Format

Vault accepts CSV or Excel files. Column names are **case-insensitive** — `Food`, `FOOD`, and `food` all work. Missing categories default to `0`.

| Column | Required | Notes |
|---|---|---|
| `Date` | ✅ Yes | Any standard date format |
| `food` | Optional | |
| `rent` | Optional | |
| `transport` | Optional | |
| `entertainment` | Optional | |
| `groceries` | Optional | |
| `subscriptions` | Optional | |
| `medical` | Optional | |
| `other` | Optional | |

> **File size limit:** 10MB — **Supported formats:** CSV, XLSX
> Sample test files are available in the test_data/ folder
---

## Supabase Schema

**Table: `uploads`**

| Column | Type | Notes |
|---|---|---|
| `id` | uuid | Auto-generated primary key |
| `user_id` | uuid | Foreign key → auth.users |
| `month` | int2 | 1–12 |
| `year` | int2 | e.g. 2026 |
| `income` | float4 | |
| `budget` | float4 | |
| `net_savings` | float4 | Can be negative |
| `total_spent` | float4 | Computed by Pandas on upload |
| `category_breakdown` | jsonb | `{"food": 461, "rent": 1200, ...}` |
| `currency` | text | Default: USD |
| `created_at` | timestamptz | Auto-generated |

> RLS policies enforced: users can only `SELECT` and `INSERT` their own rows. Duplicate month/year uploads per user are blocked at the database level.

---

## Security

- API keys stored in `.env` locally and Streamlit Secrets on deployment — never committed to version control
- Supabase RLS enforces row-level data isolation per user
- Input validation: income and budget capped at 1,000,000; net savings bounded between -1,000,000 and 1,000,000
- File uploads capped at 10MB via `.streamlit/config.toml`

---

## Known Limitations

- **Session lost on hard refresh** — Streamlit limitation, re-login required
- **Forgot password** not implemented in v1
- **Multi-sheet Excel files** — first sheet only is read
- **Groq rate limits** not explicitly enforced (mitigated by single roast per page load + 30-second cooldown on regenerate)

---

## Built for

**Decoding Data Science — 8-Day AI Application Building Challenge**