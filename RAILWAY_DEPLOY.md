# Railway Deployment Guide

## 1) Create service
- Create a new Railway project and connect this repo.
- Deploy using the included `Dockerfile` (recommended for Selenium support).
- Start command is already defined by `Procfile` as `python main.py`.

## 2) Add persistent volume
- Add a volume and mount it at `/data`.
- Set `DATA_DIR=/data` in variables so tokens and CSV logs survive restarts.

## 3) Configure variables
Set these in Railway service variables:

- `KITE_API_KEY`
- `KITE_API_SECRET`

Use one of these token approaches:

- Preferred: set `KITE_ACCESS_TOKEN` manually each day (no Selenium dependency at runtime).
- Auto-login mode: also set `KITE_USER_ID`, `KITE_PASSWORD`, `KITE_TOTP_SECRET`.

Recommended runtime variables:

- `MARKET_TIMEZONE=Asia/Kolkata`
- `MARKET_START=09:30`
- `MARKET_END=15:15`
- `SIGNAL_INTERVAL_MINUTES=5`
- `DATA_DIR=/data`

## 4) Verify deployment
- Check logs for:
  - `Trading bot started`
  - `Downloading instrument dump...`
- Confirm CSV logs are being written under `/data/trade_history.csv`.

## 5) Paper vs live mode
- Current code is in paper mode for order placement.
- It tracks real prices and logs virtual exits to CSV without placing broker orders.
