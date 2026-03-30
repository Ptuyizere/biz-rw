from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from config import settings
from database import init_db
from routers import auth, businesses, feedback, bookings, products, analytics, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting biz.rw API...")
    init_db()
    _seed_admin()
    logger.info("Database initialised.")
    yield
    logger.info("Shutting down biz.rw API.")


def _seed_admin():
    from database import SessionLocal
    from models import User
    from auth import hash_password

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not existing:
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                full_name="Platform Admin",
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                is_admin=True,
            )
            db.add(admin_user)
            db.commit()
            logger.info("Admin user seeded: %s", settings.ADMIN_EMAIL)
    finally:
        db.close()


app = FastAPI(
    title="biz.rw API",
    description="Empowering Rwandan SMEs with an online presence",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(businesses.router)
app.include_router(feedback.router)
app.include_router(bookings.router)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
