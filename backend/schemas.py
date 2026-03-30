from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from models import BusinessCategory, BusinessTemplate, BookingStatus
import re


# ─── Auth Schemas ────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        return v.strip()


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# ─── Business Schemas ────────────────────────────────────────────────────────

class BusinessCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: BusinessCategory = BusinessCategory.service
    template: BusinessTemplate = BusinessTemplate.modern
    tagline: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    whatsapp: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Business name cannot be empty")
        return v.strip()


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[BusinessCategory] = None
    template: Optional[BusinessTemplate] = None
    tagline: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    whatsapp: Optional[str] = None


class ProductServiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Optional[float]
    currency: str
    image_url: Optional[str]
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackOut(BaseModel):
    id: int
    visitor_name: str
    rating: int
    comment: Optional[str]
    created_at: datetime
    is_hidden: bool

    model_config = {"from_attributes": True}


class BusinessOut(BaseModel):
    id: int
    owner_id: int
    name: str
    slug: str
    description: Optional[str]
    category: BusinessCategory
    template: BusinessTemplate
    tagline: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    cover_url: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    whatsapp: Optional[str]
    is_active: bool
    is_featured: bool
    view_count: int
    created_at: datetime
    updated_at: datetime
    owner: Optional[UserOut] = None
    products_services: List[ProductServiceOut] = []
    feedback: List[FeedbackOut] = []
    avg_rating: Optional[float] = None
    feedback_count: int = 0

    model_config = {"from_attributes": True}


class BusinessListOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    category: BusinessCategory
    template: BusinessTemplate
    tagline: Optional[str]
    city: Optional[str]
    logo_url: Optional[str]
    cover_url: Optional[str]
    is_featured: bool
    view_count: int
    avg_rating: Optional[float] = None
    feedback_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Feedback Schemas ────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    visitor_name: str
    visitor_email: Optional[EmailStr] = None
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

    @field_validator("visitor_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


# ─── Booking Schemas ────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    visitor_name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_date: Optional[str] = None
    message: Optional[str] = None

    @field_validator("visitor_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class BookingOut(BaseModel):
    id: int
    business_id: int
    visitor_name: str
    email: str
    phone: Optional[str]
    preferred_date: Optional[str]
    message: Optional[str]
    status: BookingStatus
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Product/Service Schemas ─────────────────────────────────────────────────

class ProductServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "RWF"
    is_available: bool = True


class ProductServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    is_available: Optional[bool] = None


# ─── Analytics Schemas ────────────────────────────────────────────────────────

class AnalyticsOut(BaseModel):
    total_views: int
    total_feedback: int
    total_bookings: int
    avg_rating: Optional[float]
    recent_bookings: List[BookingOut]
    recent_feedback: List[FeedbackOut]
    pending_bookings: int
    unread_bookings: int


# ─── Admin Schemas ────────────────────────────────────────────────────────────

class AdminStats(BaseModel):
    total_users: int
    total_businesses: int
    total_bookings: int
    total_feedback: int
    active_businesses: int


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    per_page: int
    pages: int
