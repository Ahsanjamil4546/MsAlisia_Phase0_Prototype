# MsAlisia Phase 0 File Guide

This document explains every important file in the Phase 0 prototype.

---

## Root Files

### `README.md`
Main setup and usage guide. Includes installation steps, environment variables, API endpoints, scope, and deployment notes.

### `docker-compose.yml`
Runs the frontend and backend together using Docker. Useful for local testing when Docker is installed.

---

## Backend Files

### `backend/requirements.txt`
Python dependencies for the FastAPI backend.

Main packages:
- `fastapi` for the API server
- `uvicorn` for running the server
- `httpx` for calling Groq
- `pydantic` and `pydantic-settings` for validation and settings
- `email-validator` for validating parent/waitlist emails

### `backend/.env.example`
Template for backend environment variables. Copy this to `.env` and add the real Groq API key.

### `backend/Dockerfile`
Builds the backend container for Docker-based deployment.

### `backend/app/config.py`
Loads backend configuration from environment variables.

Important settings:
- `GROQ_API_KEY`
- `GROQ_MODEL`
- `GROQ_BASE_URL`
- `DATABASE_PATH`
- `CORS_ORIGINS`

### `backend/app/schemas.py`
Defines request and response data models using Pydantic.

Main models:
- `ParentProfile`
- `StudentProfile`
- `ProfileRequest`
- `ChatRequest`
- `ChatResponse`
- `WaitlistRequest`
- `SummaryResponse`
- `AdminSnapshot`

### `backend/app/tutor_prompt.py`
Contains the Ms Alisia tutoring instructions.

This file controls the tutoring style:
- one concept at a time
- short explanation
- quick validation question
- encouragement
- hint-first learning
- child-friendly tone

### `backend/app/groq_client.py`
Handles communication with the Groq API.

It sends requests to Groq’s OpenAI-compatible chat completions endpoint. If no Groq API key is present, it returns a small demo fallback response.

### `backend/app/db.py`
Local SQLite persistence layer for Phase 0.

Stores:
- parent/student profiles
- waitlist submissions
- chat messages
- basic summary/admin counts

This is intentionally simple for prototype use.

### `backend/app/main.py`
Main FastAPI application.

Defines these endpoints:
- `GET /health`
- `POST /api/profiles`
- `GET /api/profiles/{profile_id}`
- `POST /api/chat`
- `GET /api/sessions/{session_id}/summary`
- `POST /api/waitlist`
- `GET /api/admin/snapshot`

---

## Frontend Files

### `frontend/package.json`
Defines frontend scripts and dependencies.

Main scripts:
- `npm run dev`
- `npm run build`
- `npm run preview`

### `frontend/.env.example`
Template for frontend environment variables.

Main variable:
- `VITE_API_BASE_URL`

### `frontend/Dockerfile`
Builds the frontend container and serves it through Nginx.

### `frontend/index.html`
HTML entry point used by Vite.

### `frontend/vite.config.ts`
Vite configuration for the React frontend.

### `frontend/tsconfig.json`
TypeScript configuration.

### `frontend/src/main.tsx`
React entry point. Mounts the app into the page.

### `frontend/src/App.tsx`
Main frontend application state and layout.

Handles:
- parent/student profile state
- saved profile ID
- chat messages
- session ID
- parent summary
- API errors

### `frontend/src/api.ts`
Frontend API client.

Functions:
- `createProfile`
- `sendChatMessage`
- `joinWaitlist`
- `getSessionSummary`
- `getAdminSnapshot`

### `frontend/src/types.ts`
Shared TypeScript types for frontend data.

Includes:
- parent profile
- student profile
- chat message
- summary
- admin snapshot

### `frontend/src/styles.css`
Global styles for the interface.

Design direction:
- lilac/light purple
- gold accents
- calm cards
- large rounded panels
- readable fields and buttons
- responsive layout for desktop/tablet/mobile

---

## Frontend Components

### `frontend/src/components/Header.tsx`
Top hero/brand section for the prototype.

### `frontend/src/components/OnboardingPanel.tsx`
Parent/student setup form.

Collects:
- parent name
- parent email
- child name
- grade
- confidence level
- learning pace
- support preference
- optional learning notes

### `frontend/src/components/ChatPanel.tsx`
Student tutoring chat interface.

Includes:
- quick example prompts
- chat window
- message input
- provider/model indicator

### `frontend/src/components/ParentSummary.tsx`
Simple parent-facing summary panel.

Displays:
- total student turns
- latest focus
- strengths
- support needs
- next step

### `frontend/src/components/WaitlistPanel.tsx`
Optional waitlist form for Phase 0 interest capture.

### `frontend/src/components/AdminSnapshot.tsx`
Simple internal metrics panel.

Displays:
- number of profiles
- waitlist signups
- sessions
- messages

---

## Notes for Developers

- Keep the Groq API key server-side only.
- Frontend calls the backend only; it never calls Groq directly.
- The tutor prompt should be edited carefully because it controls the learning behavior.
- SQLite is only for Phase 0. Replace it with Supabase/PostgreSQL or Cloud SQL in later phases.
- Admin snapshot is not protected in Phase 0. Add authentication before any public deployment.
