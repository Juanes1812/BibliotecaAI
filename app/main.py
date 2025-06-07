from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.api.endpoints import router as api_router  # Importa tu router

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Biblioteca IA API",
    description="API para procesar solicitudes en español con base de datos en inglés",
    version="1.0.0"
)

# Configuración CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye tu router con prefijo opcional
app.include_router(
    api_router,
    prefix="/api",  
    tags=["Solicitudes"]
)

@app.get("/", include_in_schema=False)
async def health_check():
    return {"status": "API operativa"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)