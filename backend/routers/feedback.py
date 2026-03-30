from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import Business, Feedback
from schemas import FeedbackCreate, FeedbackOut
from dependencies import get_current_user, get_current_admin
from models import User
from utils.email import send_feedback_notification

router = APIRouter(prefix="/api/businesses/{slug}/feedback", tags=["Feedback"])


@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    slug: str,
    data: FeedbackCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug, Business.is_active == True).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")

    fb = Feedback(
        business_id=b.id,
        visitor_name=data.visitor_name,
        visitor_email=str(data.visitor_email) if data.visitor_email else None,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)

    if b.email:
        background_tasks.add_task(
            send_feedback_notification,
            b.name,
            b.email,
            {"visitor_name": fb.visitor_name, "rating": fb.rating, "comment": fb.comment},
        )

    return fb


@router.get("", response_model=list[FeedbackOut])
def get_feedback(slug: str, db: Session = Depends(get_db)):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return db.query(Feedback).filter(
        Feedback.business_id == b.id, Feedback.is_hidden == False
    ).order_by(Feedback.created_at.desc()).all()


@router.patch("/{feedback_id}/hide", response_model=FeedbackOut)
def toggle_hide_feedback(
    slug: str,
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    fb = db.query(Feedback).filter(Feedback.id == feedback_id, Feedback.business_id == b.id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    fb.is_hidden = not fb.is_hidden
    db.commit()
    db.refresh(fb)
    return fb
