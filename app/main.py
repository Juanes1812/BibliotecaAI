from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Biblioteca IA API",
    description="API para gestionar libros mediante emails",
    version="0.1.0"
)

# Configurar CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheck(BaseModel):
    status: str

@app.get("/", response_model=HealthCheck, tags=["Health Check"])
async def root():
    return {"status": "API funcionando"}

@app.get("/test-email", tags=["Development"])
async def test_email_config():
    """Endpoint para verificar la configuración de email"""
    email_account = os.getenv("EMAIL_ACCOUNT")
    return {
        "message": "Configuración de email cargada",
        "email_account": email_account
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)