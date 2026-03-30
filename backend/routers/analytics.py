from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from database import get_db
from models import Business, Feedback, Booking, ProfileView, User
from schemas import AnalyticsOut, BookingOut, FeedbackOut
from dependencies import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/{slug}", response_model=AnalyticsOut)
def get_analytics(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    visible_fb = db.query(Feedback).filter(
        Feedback.business_id == b.id, Feedback.is_hidden == False
    ).all()

    ratings = [f.rating for f in visible_fb]
    avg = round(sum(ratings) / len(ratings), 2) if ratings else None

    recent_bookings = (
        db.query(Booking)
        .filter(Booking.business_id == b.id)
        .order_by(Booking.created_at.desc())
        .limit(10)
        .all()
    )

    recent_feedback = (
        db.query(Feedback)
        .filter(Feedback.business_id == b.id, Feedback.is_hidden == False)
        .order_by(Feedback.created_at.desc())
        .limit(10)
        .all()
    )

    total_bookings = db.query(Booking).filter(Booking.business_id == b.id).count()
    pending_bookings = db.query(Booking).filter(Booking.business_id == b.id, Booking.status == "pending").count()
    unread_bookings = db.query(Booking).filter(Booking.business_id == b.id, Booking.is_read == False).count()

    return AnalyticsOut(
        total_views=b.view_count,
        total_feedback=len(visible_fb),
        total_bookings=total_bookings,
        avg_rating=avg,
        recent_bookings=[BookingOut.model_validate(bk) for bk in recent_bookings],
        recent_feedback=[FeedbackOut.model_validate(f) for f in recent_feedback],
        pending_bookings=pending_bookings,
        unread_bookings=unread_bookings,
    )
