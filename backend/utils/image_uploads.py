from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException

UPLOAD_DIR =  Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/jpeg": ".jpeg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_SIZE = 5 * 1024 * 1024

async def save_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Formato inválido. Envie JPG, PNG ou WEBP."
        )

    content = await file.read(MAX_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="O arquivo está vazio."
        )

    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="A imagem deve ter no máximo 5 MB."
        )

    extension = ALLOWED_TYPES[file.content_type]
    filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(content)

    return f"/uploads/{filename}"