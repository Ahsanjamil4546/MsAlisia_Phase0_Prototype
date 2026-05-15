# Production Deployment

This repository is a monorepo with:

- Frontend: Vite React in `frontend/`
- Backend: FastAPI Python in `backend/`

The frontend deploys to Vercel. The backend deploys to Railway.

## 1. Deploy Backend on Railway

Create a new Railway project from the GitHub repository.

Railway settings:

- Root Directory: `/` or `backend`
- Builder: Dockerfile
- Dockerfile Path: `Dockerfile`
- Start Command: `sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"`
- Healthcheck Path: `/health`

The root `Dockerfile` and `railway.json` deploy the backend from the monorepo root. The `backend/Dockerfile` and `backend/railway.json` are also available if you set Railway's Root Directory to `backend`.

Railway automatically provides `PORT`. Do not set `PORT` manually.

Add these Railway environment variables:

```env
ENVIRONMENT=production
CORS_ORIGINS=https://your-vercel-frontend.vercel.app
CORS_ORIGIN_REGEX=https://.*\.vercel\.app
DATABASE_PATH=/app/data/msalisia_phase0.db
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
GROQ_BASE_URL=https://api.groq.com/openai/v1
LLM_TEMPERATURE=0.35
LLM_MAX_TOKENS=420
```

After deployment, open Railway networking and generate a public domain. The backend should respond at:

```text
https://your-railway-backend.up.railway.app/health
```

## 2. Deploy Frontend on Vercel

Create a new Vercel project from the same GitHub repository.

Vercel settings:

- Root Directory: `frontend`
- Framework Preset: `Vite`
- Install Command: `npm ci`
- Build Command: `npm run build`
- Output Directory: `dist`

Add this Vercel environment variable:

```env
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app
```

Redeploy the frontend after adding or changing this variable.

## 3. Connect Frontend and Backend

1. Deploy the Railway backend first.
2. Copy the Railway public backend URL.
3. Add that URL to Vercel as `VITE_API_BASE_URL`.
4. Copy the Vercel frontend URL.
5. Add that URL to Railway as `CORS_ORIGINS`.
6. Redeploy both services.

For Vercel preview deployments, keep:

```env
CORS_ORIGIN_REGEX=https://.*\.vercel\.app
```

For stricter production-only CORS, remove `CORS_ORIGIN_REGEX` and set only the exact production frontend URL in `CORS_ORIGINS`.

## 4. Local Development

Backend:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```powershell
cd frontend
npm run dev
```

Local URLs:

- Frontend: `http://localhost:5173`
- Backend: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`
