from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.yolo import detect_pencil
from app.core.security import create_token

router = APIRouter()

@router.post("/verify-pencil")
async def verify_pencil(image: UploadFile = File(...)):
    is_valid = await detect_pencil(image)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Pencil not found")
    token = create_token({"sub": "pencil-user"})
    return {"access": True, "token": token}
