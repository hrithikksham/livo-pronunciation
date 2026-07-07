# Pronunciation Scorer AI

AI-powered English pronunciation analysis built using FastAPI, Groq Whisper, Llama 3, and Next.js.

## Features

- Audio Upload
- Automatic Audio Normalization
- Whisper Speech-to-Text
- AI Pronunciation Evaluation
- Score Breakdown
- Word-level Mistakes
- Transcript Highlighting
- AI Feedback

## Tech Stack

### Frontend

- Next.js 15
- TypeScript
- TailwindCSS
- Framer Motion

### Backend

- FastAPI
- Pydantic
- Groq Whisper
- Llama 3.3 70B

## Architecture

(Add architecture image)

## Screenshots

(Add screenshots)

## Running Locally

### Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

## Environment Variables

Backend

```env
GROQ_API_KEY=
```

Frontend

```env
NEXT_PUBLIC_API_URL=
```

## License

MIT# livo-pronunciation
