from fastapi import APIRouter, HTTPException, Request, Header
from app.core.security import verify_token
import httpx
import os
from pydantic import BaseModel

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest,authorization: str = Header(None)):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")
    print("GEMINI_API_KEY:", GEMINI_API_KEY)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message")

    gemini_payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Ты эксперт в области кибербезопасности. "
                            "Отвечай только на вопросы по этой теме. "
                            "Если вопрос не относится к кибербезопасности, скажи: "
                            "'Извините, я могу отвечать только на вопросы, касающиеся кибербезопасности.'\n\n"
                            f"{user_message}"
                        )
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json=gemini_payload,
            timeout=15
        )

    if response.status_code != 200:
        print("Gemini API responded with status:", response.status_code)
        print("Gemini response body:",
              response.text)
        raise HTTPException(status_code=500, detail="GEMINI API error")

    result = response.json()

    try:
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        reply = "Извините, я не смог обработать ваш запрос."

    return {"response": reply}