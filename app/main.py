from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import verify_pencil, chat
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(verify_pencil.router, prefix="/api", tags=["Access verification"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])