import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import supabase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://marka_patentdy.vercel.app"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class QuizSubmit(BaseModel):
    isim_soyisim: str

@app.post("/submit")
def submit(data: QuizSubmit):
    result = supabase.table("anaveri").insert({
        "isim_soyisim": data.isim_soyisim
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Kayıt başarısız")

    return {"mesaj": "Kaydedildi", "id": result.data[0]["id"]}