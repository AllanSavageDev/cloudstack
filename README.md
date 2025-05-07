<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-090909?style=for-the-badge&logo=fastapi&logoColor=00FF84" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" />
</p>

---

[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/allansavage/cloudstack)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/allansavage/cloudstack/blob/main/LICENSE)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue)](https://github.com/allansavage/cloudstack#-full-docker-setup-production)
[![Made for Vibe Coders](https://img.shields.io/badge/vibe-ready-critical)](https://github.com/allansavage/cloudstack)

# 🚀 CloudStack

CloudStack is a modern full-stack boilerplate using:

- 🐍 **FastAPI** (Python backend with JWT auth & raw SQL)
- ⚡ **PostgreSQL** via Docker
- 🌐 **Next.js 15 + React 19**
- 🎨 **TailwindCSS**
- 🔐 Built-in login, user management, and full CRUD
- 🧪 Works with `npm run dev` or full Docker stack

> Rename this to **VibeStack** before going public if you want to ride the meme.

---

## ✅ Features

- User auth with JWT (no ORM bloat)
- Demo user auto-created (`demo@demo.com` / `password`)
- Create/read/update/delete items — all protected
- Frontend calls backend via `/api` rewrite (no config needed)
- Runs in dev or prod with Docker or native tools

---

## 🧱 Stack

| Layer     | Tech               |
|-----------|--------------------|
| Backend   | FastAPI + psycopg2 |
| DB        | PostgreSQL (Docker)|
| Frontend  | Next.js 15 + TS    |
| Styling   | Tailwind CSS       |
| Auth      | JWT (Python-Jose)  |

---

## 🚀 Get Started (Local Dev)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/cloudstack
cd cloudstack

# 2. Set up Python backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Start the local stack
./local.run.debug.sh
```

---

## 🐳 Full Docker Setup (Production)

```bash
docker compose up --build
```

Then visit:
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

---

## 🔑 Demo Credentials

- Email: `demo@demo.com`
- Password: `password`

---

## 🛠 What’s Included

```
backend/
  demo.py        ← Main FastAPI app
  requirements.txt
  Dockerfile

frontend/
  app/demo/demo.tsx  ← Full auth + CRUD UI
  tailwind.config.js
  postcss.config.mjs
  Dockerfile
  package.json

docker-compose.yml
local.run.debug.sh
```

---

## 📦 Coming Soon

- Redis support
- Email confirmation
- Real password hashing (already using argon2)
- Deployment recipes for Render/Fly/EC2
