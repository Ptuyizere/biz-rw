from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Business, ProductService, User
from schemas import ProductServiceCreate, ProductServiceUpdate, ProductServiceOut
from dependencies import get_current_user
from utils.file_upload import save_upload_file, delete_file

router = APIRouter(prefix="/api/businesses/{slug}/items", tags=["Products & Services"])


def get_owned_business(slug: str, current_user: User, db: Session) -> Business:
    b = db.query(Business).filter(Business.slug == slug).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    if b.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return b


@router.get("", response_model=List[ProductServiceOut])
def list_items(slug: str, db: Session = Depends(get_db)):
    b = db.query(Business).filter(Business.slug == slug, Business.is_active == True).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return b.products_services


@router.post("", response_model=ProductServiceOut, status_code=status.HTTP_201_CREATED)
def create_item(
    slug: str,
    data: ProductServiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = get_owned_business(slug, current_user, db)
    item = ProductService(business_id=b.id, **data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ProductServiceOut)
def update_item(
    slug: str,
    item_id: int,
    data: ProductServiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = get_owned_business(slug, current_user, db)
    item = db.query(ProductService).filter(ProductService.id == item_id, ProductService.business_id == b.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.post("/{item_id}/image", response_model=ProductServiceOut)
async def upload_item_image(
    slug: str,
    item_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = get_owned_business(slug, current_user, db)
    item = db.query(ProductService).filter(ProductService.id == item_id, ProductService.business_id == b.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.image_url:
        delete_file(item.image_url)
    url = await save_upload_file(file, subfolder="items")
    item.image_url = url
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    slug: str,
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    b = get_owned_business(slug, current_user, db)
    item = db.query(ProductService).filter(ProductService.id == item_id, ProductService.business_id == b.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.image_url:
        delete_file(item.image_url)
    db.delete(item)
    db.commit()
