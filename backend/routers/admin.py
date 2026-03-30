from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Business, Feedback, Booking
from schemas import UserOut, BusinessListOut, AdminStats, BookingOut, FeedbackOut
from dependencies import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStats)
def admin_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return AdminStats(
        total_users=db.query(User).count(),
        total_businesses=db.query(Business).count(),
        active_businesses=db.query(Business).filter(Business.is_active == True).count(),
        total_bookings=db.query(Booking).count(),
        total_feedback=db.query(Feedback).count(),
    )


@router.get("/users", response_model=List[UserOut])
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )


@router.patch("/users/{user_id}/toggle-active", response_model=UserOut)
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/make-admin", response_model=UserOut)
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = not user.is_admin
    db.commit()
    db.refresh(user)
    return user


@router.get("/businesses", response_model=List[BusinessListOut])
def list_all_businesses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    businesses = (
        db.query(Business)
        .order_by(Business.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    result = []
    for b in businesses:
        visible_fb = [f for f in b.feedback if not f.is_hidden]
        avg = round(sum(f.rating for f in visible_fb) / len(visible_fb), 1) if visible_fb else None
        item = BusinessListOut.model_validate(b)
        item.avg_rating = avg
        item.feedback_count = len(visible_fb)
        result.append(item)
    return result


@router.patch("/businesses/{slug}/toggle-active")
def toggle_business_active(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    b.is_active = not b.is_active
    db.commit()
    return {"slug": b.slug, "is_active": b.is_active}


@router.patch("/businesses/{slug}/toggle-featured")
def toggle_business_featured(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    b.is_featured = not b.is_featured
    db.commit()
    return {"slug": b.slug, "is_featured": b.is_featured}


@router.get("/feedback", response_model=List[FeedbackOut])
def list_all_feedback(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )


@router.patch("/feedback/{feedback_id}/toggle-hide", response_model=FeedbackOut)
def admin_toggle_hide_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    fb.is_hidden = not fb.is_hidden
    db.commit()
    db.refresh(fb)
    return fb
