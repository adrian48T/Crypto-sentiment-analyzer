# Crypto Sentiment Analyzer (MVP) - Crypto-only
This is an MVP project that scrapes crypto news RSS feeds, scores sentiment, and serves a small React frontend.

## Quick start (local)
1. Create Python venv: `python -m venv venv && source venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Init DB: `python db_init.py`
4. Run backend: `python app.py`
5. In `frontend/` run: `npm install` and `npm start` (or use `npm run build` and serve the build folder)

## Deploy to Railway (one-click)
1. Push this repo to your GitHub account (create `crypto-sentiment-analyzer`).
2. On Railway, choose “Deploy from GitHub” and select this repo.
3. Set env vars if needed (none required for basic MVP).

## Notes
- Frontend contains placeholder ad blocks. Replace with AdSense or other ad code.
- HuggingFace model usage is optional; the app falls back to VADER for sentiment.
