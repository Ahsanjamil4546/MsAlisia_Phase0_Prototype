
# MsAlisia Phase 0 Prototype

A lean Phase 0 prototype for **MsAlisia**, focused on validating the core tutoring experience for **Grades 3-5 Math** with an easy-to-use interface for non-technical users.

The learning companion is presented as **Ms Alisia**. The experience avoids heavy “AI chatbot” branding and instead focuses on calm, guided, premium learning.

---

## 1. What This Prototype Includes

### Frontend
- React + TypeScript + Vite
- Responsive, parent-friendly interface
- Learner onboarding form
- Guided tutoring chat screen
- Parent learning summary panel
- Waitlist form
- Simple admin snapshot
- Light purple/lilac + gold visual direction

### Backend
- Python FastAPI
- Groq API integration through OpenAI-compatible Chat Completions
- Local SQLite storage for Phase 0 data
- Profile endpoint
- Chat endpoint
- Waitlist endpoint
- Session summary endpoint
- Admin snapshot endpoint

### AI/Tutoring Behavior
Ms Alisia is instructed to:
- Teach one concept at a time
- Use short explanations
- Ask one quick validation question
- Encourage the student
- Avoid long instructional articles
- Use hint-first support
- Keep the tone calm and child-friendly

---

## 2. Project Structure

```text
MsAlisia_Phase0_Prototype/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── groq_client.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── tutor_prompt.py
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdminSnapshot.tsx
│   │   │   ├── ChatPanel.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── OnboardingPanel.tsx
│   │   │   ├── ParentSummary.tsx
│   │   │   └── WaitlistPanel.tsx
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── types.ts
│   ├── .env.example
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/
│   └── FILE_GUIDE.md
├── docker-compose.yml
└── README.md
```

---

## 3. Required API Key

For real AI responses, the backend needs a Groq API key.

Create this file:

```bash
cp backend/.env.example backend/.env
```

Then update:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

If no Groq API key is provided, the backend will use a small demo fallback response so the UI can still be tested.

---

## 4. Run Locally Without Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 5. Run With Docker Compose

```bash
cp backend/.env.example backend/.env
# Add GROQ_API_KEY inside backend/.env

docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

---

## 6. Environment Variables

### Backend `.env`

| Variable | Purpose |
|---|---|
| `ENVIRONMENT` | Runtime environment name |
| `CORS_ORIGINS` | Allowed frontend URLs |
| `DATABASE_PATH` | SQLite database file path |
| `GROQ_API_KEY` | Server-side Groq API key |
| `GROQ_MODEL` | Groq model name |
| `GROQ_BASE_URL` | Groq OpenAI-compatible API base URL |
| `LLM_TEMPERATURE` | Controls response creativity |
| `LLM_MAX_TOKENS` | Maximum output length |

### Frontend `.env`

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Backend API URL |

---

## 7. Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Backend health check |
| `POST` | `/api/profiles` | Create parent/student learning profile |
| `GET` | `/api/profiles/{profile_id}` | Get saved profile |
| `POST` | `/api/chat` | Send a student message to Ms Alisia |
| `GET` | `/api/sessions/{session_id}/summary` | Get basic parent learning summary |
| `POST` | `/api/waitlist` | Save waitlist signup |
| `GET` | `/api/admin/snapshot` | View simple prototype metrics |

---

## 8. Phase 0 Scope

This prototype is intentionally lean. It is designed to validate:

- Core tutoring behavior
- Ease of use for parents and students
- Child-friendly conversation flow
- Basic personalization from onboarding
- Parent summary direction
- Simple admin visibility
- Waitlist capture direction
- Groq API integration
- Frontend/backend integration

---

## 9. What Is Not Included in Phase 0

The following should wait for later phases:

- Full production billing
- Stripe subscriptions
- Full parent dashboard
- Full admin dashboard
- Full referral system
- 7-day trial automation
- Production email automation
- Large-scale reporting
- Full ELA implementation
- Full homework image analysis
- GCP production deployment
- GKE/Cloud Run production infrastructure

---

## 10. Deployment Notes

### Recommended Phase 0 Deployment

- Frontend: Vercel
- Backend: Railway
- Database: local SQLite for prototype or Railway volume/storage
- LLM: Groq API

### Production Direction Later

For future MVP/production phases, the project can move toward:

- Cloud Run-first low-cost GCP deployment
- Cloud SQL PostgreSQL
- Cloud Storage
- Firebase Authentication
- Stripe Billing
- GKE Autopilot only when scale justifies it

---

## 11. Non-Technical User Interface Goals

The interface is designed to be simple enough for parents and non-technical users:

1. Set up learner profile
2. Ask a math question
3. Read the short tutor response
4. Refresh parent summary
5. Optionally join waitlist
6. Optionally view simple admin metrics

No technical setup is exposed inside the UI.

---

## 12. Security Notes

- Never place the Groq API key in the frontend.
- Keep `GROQ_API_KEY` only in the backend `.env` file or deployment environment variables.
- Do not commit `.env` files to GitHub.
- The included SQLite database is for Phase 0 only and should not be treated as production storage.
- For production, use role-based access control, secure secrets, backups, and stronger audit logging.

---

## 13. Suggested First Demo Flow

1. Open the frontend.
2. Review/edit the parent and student profile.
3. Save the learner profile.
4. Click a quick prompt such as “Can you help me with LCM of 4 and 6?”
5. Send the message.
6. Confirm Ms Alisia gives a short explanation and asks one quick validation question.
7. Refresh the parent learning summary.
8. Add a waitlist test entry.
9. Load the admin snapshot.

---

## 14. Future Improvements

- Supabase/PostgreSQL persistence
- Real auth
- Admin login protection
- Homework image support
- Session transcript export
- Parent dashboard
- More Grade 3-5 Math topics
- ELA tutoring mode
- Better analytics
- Cost tracking per session/student
- Safety escalation workflows
