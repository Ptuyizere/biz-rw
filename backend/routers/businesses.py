from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List
import re
from database import get_db
from models import Business, User, Feedback, ProfileView
from schemas import (
    BusinessCreate, BusinessUpdate, BusinessOut, BusinessListOut
)
from dependencies import get_current_user, get_optional_user
from utils.file_upload import save_upload_file, delete_file

router = APIRouter(prefix="/api/businesses", tags=["Businesses"])


def make_slug(name: str, db: Session, exclude_id: int = None) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    slug = base
    i = 1
    while True:
        query = db.query(Business).filter(Business.slug == slug)
        if exclude_id:
            query = query.filter(Business.id != exclude_id)
        if not query.first():
            break
        slug = f"{base}-{i}"
        i += 1
    return slug


def enrich_business(b: Business) -> dict:
    visible_fb = [f for f in b.feedback if not f.is_hidden]
    avg = round(sum(f.rating for f in visible_fb) / len(visible_fb), 1) if visible_fb else None
    data = BusinessOut.model_validate(b).model_dump()
    data["avg_rating"] = avg
    data["feedback_count"] = len(visible_fb)
    data["feedback"] = [f for f in data["feedback"] if not f["is_hidden"]]
    return data


@router.get("", response_model=List[BusinessListOut])
def list_businesses(
    search: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Business)
        .options(joinedload(Business.feedback))
        .filter(Business.is_active == True)
    )
    if search:
        term = f"%{search}%"
        query = query.filter(
            Business.name.ilike(term) | Business.description.ilike(term) | Business.city.ilike(term)
        )
    if category:
        query = query.filter(Business.category == category)
    if city:
        query = query.filter(Business.city.ilike(f"%{city}%"))

    query = query.order_by(Business.is_featured.desc(), Business.created_at.desc())
    businesses = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for b in businesses:
        visible_fb = [f for f in b.feedback if not f.is_hidden]
        avg = round(sum(f.rating for f in visible_fb) / len(visible_fb), 1) if visible_fb else None
        item = BusinessListOut.model_validate(b)
        item.avg_rating = avg
        item.feedback_count = len(visible_fb)
        result.append(item)
    return result


@router.post("", response_model=BusinessOut, status_code=status.HTTP_201_CREATED)
def create_business(
    data: BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have a business profile")

    slug = make_slug(data.name, db)
    business = Business(
        owner_id=current_user.id,
        slug=slug,
        **data.model_dump(),
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    return enrich_business(business)


@router.get("/my", response_model=BusinessOut)
def get_my_business(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = (
        db.query(Business)
        .options(
            joinedload(Business.feedback),
            joinedload(Business.products_services),
            joinedload(Business.bookings),
        )
        .filter(Business.owner_id == current_user.id)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="No business profile found")
    return enrich_business(b)


@router.get("/{slug}", response_model=BusinessOut)
def get_business(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    b = (
        db.query(Business)
        .options(
            joinedload(Business.feedback),
            joinedload(Business.products_services),
            joinedload(Business.owner),
        )
        .filter(Business.slug == slug, Business.is_active == True)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")

    # Track view
    ip = request.client.host if request.client else None
    b.view_count += 1
    view = ProfileView(business_id=b.id, ip_address=ip)
    db.add(view)
    db.commit()
    db.refresh(b)

    return enrich_business(b)


@router.put("/{slug}", response_model=BusinessOut)
def update_business(
    slug: str,
    data: BusinessUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        update_data["slug"] = make_slug(update_data["name"], db, exclude_id=b.id)

    for k, v in update_data.items():
        setattr(b, k, v)

    db.commit()
    db.refresh(b)
    return enrich_business(b)


@router.post("/{slug}/logo", response_model=BusinessOut)
async def upload_logo(
    slug: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    if b.logo_url:
        delete_file(b.logo_url)

    url = await save_upload_file(file, subfolder="logos")
    b.logo_url = url
    db.commit()
    db.refresh(b)
    return enrich_business(b)


@router.post("/{slug}/cover", response_model=BusinessOut)
async def upload_cover(
    slug: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    if b.cover_url:
        delete_file(b.cover_url)

    url = await save_upload_file(file, subfolder="covers")
    b.cover_url = url
    db.commit()
    db.refresh(b)
    return enrich_business(b)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(b)
    db.commit()
