import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io
from config import settings


def generate_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[-1].lower()
    return f"{uuid.uuid4().hex}{ext}"


async def save_upload_file(upload_file: UploadFile, subfolder: str = "") -> str:
    if upload_file.content_type not in settings.allowed_image_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {upload_file.content_type} not allowed. Use: {settings.ALLOWED_IMAGE_TYPES}",
        )

    contents = await upload_file.read()

    if len(contents) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # Validate it's a real image & resize if needed
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
        img = Image.open(io.BytesIO(contents))

        max_dim = 1200
        if img.width > max_dim or img.height > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output = io.BytesIO()
        img.save(output, format="JPEG", quality=85, optimize=True)
        contents = output.getvalue()
        ext = ".jpg"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file",
        )

    dest_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
    os.makedirs(dest_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(dest_dir, filename)

    async with aiofiles.open(filepath, "wb") as f:
        await f.write(contents)

    rel_path = f"/uploads/{subfolder}/{filename}" if subfolder else f"/uploads/{filename}"
    return rel_path


def delete_file(file_url: str):
    if not file_url:
        return
    rel = file_url.lstrip("/")
    if os.path.exists(rel):
        os.remove(rel)
