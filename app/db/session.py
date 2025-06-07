from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Configuración de la conexión
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # Verifica que la conexión esté activa
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Funciona para abrir y cerrar sesiones de base de datos
def get_db():
    """Provee una sesión de base de datos para dependencias FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()