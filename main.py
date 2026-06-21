import os
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.ticket import TicketResponse
from services.gemini import analyze_ticket

load_dotenv()

app = FastAPI(title="Cestia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "app": "Cestia API"}

@app.post("/analyze-ticket", response_model=TicketResponse)
async def analyze_ticket_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    image_bytes = await file.read()
    return await analyze_ticket(image_bytes)