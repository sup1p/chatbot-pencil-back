from fastapi import APIRouter, HTTPException, Request, Header
from app.core.security import verify_token
import httpx
import os

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
@router.get("/chat")
async def chat(request: Request, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    data = await request.json()
    user_message = data("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=401, detail="Empty message")

    payload = {
        "contents": [
            {
                "role": "system",
                "parts": [
                    {"text": "Ты эксперт в области кибербезопасности. Отвечай только на вопросы по этой теме. "
                             "Если вопрос не относится к кибербезопасности, скажи: 'Извините, я могу отвечать только на вопросы, касающиеся кибербезопасности.'"}
                ]
            },
            {
                "role": "user",
                "parts": [{"text": user_message}]
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            json=payload,
            timeout=15
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="GEMINI API error")
        result = response.json()
        try:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            reply = "Извините, я не смог обработать ваш запрос."
    return {"response": reply}