# Bitcoin Signal Hub

A Streamlit-based signal platform for Bitcoin: on-chain analytics, merchant adoption, daily briefs, and structured learning paths. Designed for clarity and signal over noise.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run src/app.py
```

## Task Runner

This repo includes both `Taskfile.yml` (go-task default) and `task.yml`:

```bash
task setup
task run
```

## Features

- **Signal Desk**: Bitcoin primer, asset comparisons, on-chain signals, merchant adoption map, daily brief
- **Learning Platform**: Beginner → Intermediate → Advanced modules
- **Alerts (Coming Soon)**: BTC price alerts (pipeline scaffolded, disabled until infra is configured)

## Merchant Adoption Data

Merchant data is sourced from OpenStreetMap tags commonly used by BTC Map:

- `currency:XBT=yes`
- `payment:onchain=yes`
- `payment:lightning=yes`
- `payment:lightning_contactless=yes`

Large countries can be slow to query; using a state/province improves performance.

## Price Alerts (Production-Style)

Pipeline:
- UI: Streamlit Alerts tab
- DB: Supabase (free tier)
- Worker: GitHub Actions cron (hourly)
- Email: Gmail SMTP (App Password)

### Supabase Setup

Run `supabase.sql` in Supabase to create the `alerts` table.

### Local Environment Variables (optional)

```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail_address
SMTP_PASSWORD=your_gmail_app_password
FROM_EMAIL=your_gmail_address
```

### GitHub Actions Secrets

Set these in repo settings:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `FROM_EMAIL`

## Project Structure

```
BitcoinCommunity/
├── .github/
│   └── workflows/
│       └── alert_worker.yml
├── scripts/
│   └── alert_worker.py
├── src/
│   ├── alerts.py
│   ├── app.py
│   ├── utils.py
│   └── modules/
│       ├── alerts.py
│       ├── advanced.py
│       ├── beginner.py
│       ├── intermediate.py
│       └── signal_desk.py
├── requirements.txt
├── Taskfile.yml
├── task.yml
└── supabase.sql
```

## Notes

- The Daily Brief RSS parser has a built-in fallback that works even if `feedparser` isn’t installed.
- For large on-chain numbers, values are shown in compact format (K/M/B/T).

## License

MIT
