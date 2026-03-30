# biz.rw — Rwanda's Business Platform

Empowering Rwandan SMEs with a beautiful, affordable online presence.

---

## Tech Stack

| Layer     | Technology                                   |
|-----------|----------------------------------------------|
| Backend   | Python 3.11+ · FastAPI · SQLAlchemy · SQLite  |
| Frontend  | Vue 3 · Vite · Tailwind CSS · Pinia           |
| Auth      | JWT access tokens · bcrypt password hashing  |
| Email     | aiosmtplib (SMTP — Gmail/SendGrid/etc.)       |
| Images    | Server filesystem (easy swap to S3)           |

---

## Quick Start (Development)

### 1. Backend

```bash
cd biz-rw/backend

# Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env        # Windows
cp .env.example .env          # macOS/Linux
# Edit .env with your settings (see below)

# ⚠️  IMPORTANT: run uvicorn from INSIDE the backend/ folder
uvicorn main:app --reload
```

API available at: **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

### 2. Frontend

```bash
# In a separate terminal
cd biz-rw/frontend

npm install
npm run dev
```

App available at: **http://localhost:5173**

---

## Environment Variables

Edit `backend/.env`:

```env
# App
SECRET_KEY=your-super-secret-key-change-this   # min 32 random chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database (SQLite default, change for Postgres in production)
DATABASE_URL=sqlite:///./bizrw.db

# File uploads
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_MB=5

# Email notifications (optional — bookings/reviews won't email if blank)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your-app-password    # Gmail: use an App Password
SMTP_FROM=noreply@biz.rw
SMTP_TLS=true

# Admin account (seeded automatically on first run)
ADMIN_EMAIL=admin@biz.rw
ADMIN_PASSWORD=changeme123        # ← change this!

# CORS — set to your frontend URL
FRONTEND_URL=http://localhost:5173
```

---

## Default Credentials

| Role  | Email            | Password    |
|-------|------------------|-------------|
| Admin | admin@biz.rw     | admin123    |
| Demo  | amina@example.com| password123 |
| Demo  | john@example.com | password123 |

> **Change the admin password before deploying to production.**

---

## Project Structure

```
biz-rw/
├── backend/               ← Run uvicorn from HERE
│   ├── main.py            FastAPI app entry point
│   ├── config.py          Settings (reads .env)
│   ├── database.py        SQLAlchemy engine & session
│   ├── models.py          ORM models (User, Business, Feedback…)
│   ├── schemas.py         Pydantic request/response schemas
│   ├── auth.py            JWT + bcrypt utilities
│   ├── dependencies.py    FastAPI dependency injection
│   ├── seed_demo.py       Optional demo data seeder
│   ├── requirements.txt
│   ├── .env.example
│   ├── routers/
│   │   ├── auth.py        POST /api/auth/register, /login, GET /me
│   │   ├── businesses.py  CRUD + image upload
│   │   ├── feedback.py    Star ratings & comments
│   │   ├── bookings.py    Inquiry / booking requests
│   │   ├── products.py    Products & services catalogue
│   │   ├── analytics.py   Dashboard stats
│   │   └── admin.py       Admin moderation endpoints
│   └── utils/
│       ├── email.py       Async email notifications
│       └── file_upload.py Image validation & storage
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── HomeView.vue          Landing page
│   │   │   ├── ExploreView.vue       Business directory + search
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── DashboardView.vue     Owner home
│   │   │   ├── BusinessSetupView.vue Create profile wizard
│   │   │   ├── BusinessEditView.vue  Edit + manage items
│   │   │   ├── AnalyticsView.vue     Stats & recent activity
│   │   │   ├── BookingsView.vue      Manage booking requests
│   │   │   ├── BusinessPublicView.vue 3 templates: Modern/Classic/Bold
│   │   │   └── admin/               Admin panel (users/businesses/feedback)
│   │   ├── components/
│   │   ├── stores/         Pinia (auth, toast)
│   │   ├── api/            Axios + all API calls
│   │   ├── router/         Vue Router with auth guards
│   │   └── composables/
│   ├── public/favicon.svg
│   ├── package.json
│   ├── vite.config.js      Dev proxy → backend:8000
│   ├── tailwind.config.js
│   └── nginx.conf          Production nginx config
│
├── Dockerfile.backend
├── frontend/Dockerfile.frontend
├── docker-compose.yml
├── run.py                  ← Alternative: run from project root
└── README.md
```

---

## Page Templates

Each business picks one of three stunning templates:

| Template | Style          | Best For                              |
|----------|----------------|---------------------------------------|
| Modern   | Green & white, clean cards | Tech, professional services |
| Classic  | Dark navy + gold, serif typography | Established businesses, consulting |
| Bold     | Full-black, massive typography, gold accents | Retail, food, creative brands |

---

## Business URLs

Every business page lives at:
```
http://localhost:5173/b/{business-slug}
```

Example: `http://localhost:5173/b/kigali-fresh-bakery`

---

## Production with Docker

```bash
cd biz-rw

# Copy and edit backend env
cp backend/.env.example backend/.env

# Build and run everything
docker-compose up --build -d

# App on port 80, API proxied automatically
```

---

## Production without Docker (VPS)

```bash
# Backend — run with gunicorn
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend — build and serve with nginx
cd frontend
npm run build

```

© 2024 biz.rw · MIT License
