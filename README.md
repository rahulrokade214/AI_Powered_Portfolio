# Rahul Rokade — Portfolio + AI Chatbot

Two parts, two separate GitHub repos, two separate deployments:

```
frontend/   → your portfolio site (GitHub Pages)
backend/    → Flask + Groq chatbot API (Render)
```

## 1. Frontend (`frontend/index.html`)

- This is your existing portfolio site, unchanged except for one line:
  the chat widget now calls `CHAT_API_URL` (a constant near the bottom
  `<script>` block) instead of a relative `/api/chat` path — needed because
  GitHub Pages and Render are different domains.
- Push this to: `Personal-Portfolio-Website-of-Rahul-Rokade` repo.
- **After deploying the backend**, edit this line in `index.html`:
  ```js
  const CHAT_API_URL = "https://your-app-name.onrender.com/api/chat";
  ```
  Replace with your real Render URL, commit, push.

## 2. Backend (`backend/`)

- Flask API that calls Groq's LLaMA 3.3 model, with your details baked
  into the system prompt so it answers questions about you specifically.
- Push this to: `portfolio-chatbot-backend` repo.

### Local setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # then edit .env, add your real GROQ_API_KEY
python app.py
```

Visit `http://localhost:5000` — you should see "Chatbot backend is running."

### Deploy to Render

1. New Web Service → connect `portfolio-chatbot-backend` repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `python app.py`
4. Environment tab → add `GROQ_API_KEY` (your real key) — never commit it
5. Deploy, then copy the live URL (e.g. `https://xxxx.onrender.com`)
6. Paste that URL + `/api/chat` into `CHAT_API_URL` in `frontend/index.html`,
   commit, push

## Security note

`.env` is git-ignored in `backend/`. If a Groq key has ever been pushed to
GitHub in any past commit, treat it as compromised and rotate it in the
Groq console, even after deleting the file — old commits keep it in history.
