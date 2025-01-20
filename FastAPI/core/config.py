from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings

app = FastAPI()

class Settings(BaseSettings):
    mongo_uri: str
    frontend_url: str

    class Config:
        env_file = ".env"

settings = Settings()

# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(query: str):
    # Aquí iría la lógica para buscar en MongoDB
    return {"message": f"Buscaste: {query}"}
