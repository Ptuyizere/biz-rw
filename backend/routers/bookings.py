from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Business, Booking, User
from schemas import BookingCreate, BookingOut
from dependencies import get_current_user
from utils.email import send_booking_notification

router = APIRouter(prefix="/api/businesses/{slug}/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    slug: str,
    data: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug, Business.is_active == True).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")

    booking = Booking(
        business_id=b.id,
        visitor_name=data.visitor_name,
        email=str(data.email),
        phone=data.phone,
        preferred_date=data.preferred_date,
        message=data.message,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    if b.email:
        background_tasks.add_task(
            send_booking_notification,
            b.name,
            b.email,
            {
                "visitor_name": booking.visitor_name,
                "email": booking.email,
                "phone": booking.phone,
                "preferred_date": booking.preferred_date,
                "message": booking.message,
            },
        )

    return booking


@router.get("", response_model=List[BookingOut])
def get_bookings(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return (
        db.query(Booking)
        .filter(Booking.business_id == b.id)
        .order_by(Booking.created_at.desc())
        .all()
    )


@router.patch("/{booking_id}/status")
def update_booking_status(
    slug: str,
    booking_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.business_id == b.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    valid = ["pending", "confirmed", "cancelled"]
    if new_status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")

    booking.status = new_status
    booking.is_read = True
    db.commit()
    db.refresh(booking)
    return booking
