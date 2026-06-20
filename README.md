# Vault — Your money. No excuses.

Vault is a personal finance tracker with a blunt AI persona named Frank, a raccoon who roasts your spending based on real numbers from your uploaded statements.

## What it does

- Upload a monthly spending statement (CSV/XLSX)
- Enter income, budget, and net savings for the month
- See a dashboard with spending breakdown charts and an AI-generated roast from Frank
- View historical months with verdict badges (Catastrophic / Survivable / Not Bad)

## Tech stack

- Python + Streamlit (multipage app)
- Supabase (auth + Postgres database)
- Pandas (CSV/Excel parsing)
- Plotly (charts)
- Groq API (Frank's AI roasts, llama-3.3-70b-versatile)
- Deployed on Streamlit Community Cloud

## How to run locally

1. Clone the repo
2. Install dependencies:
    pip install -r requirements.txt
3. Create a `.env` file in the root with: 
    SUPABASE_URL=your_supabase_url
    SUPABASE_ANON_KEY=your_supabase_anon_key
    GROQ_API_KEY=your_groq_api_key 
4. Run the app: 
    streamlit run app.py

## Project Structure 
vault/

├── app.py              # Landing page
├── requirements.txt
├── styles/
│   └── global.css      # Dark theme
├── utils/
│   └── init.py     # Shared helpers (auth, sidebar, Supabase client)
└── pages/
├── 1_Login.py
├── 2_Dashboard.py
├── 3_Upload.py
└── 4_History.py

# Expected upload file format
Columns: `Date` + any of `food, rent, transport, entertainment, other, subscriptions, groceries, medical`. Missing categories default to 0. Case-insensitive column matching.