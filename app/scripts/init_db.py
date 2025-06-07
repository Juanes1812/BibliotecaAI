import csv
import logging
from datetime import date, timedelta

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.libro import Libro, Reserva
from app.models.enums import EstadoLibro  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = "data/processed/books_clean.csv" 

def init_db():
    """Inicializa la base de datos con datos desde un CSV limpio."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        with open(CSV_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                libro = Libro(
                    titulo=row['title'][:300],
                    autor=row['authors'][:800],
                    isbn=row['isbn13'][:20],
                    estado=EstadoLibro.DISPONIBLE
                )
                db.add(libro)
            db.commit()
        
        # Crear una reserva de ejemplo
        libro_reservado = db.query(Libro).filter(Libro.titulo.ilike("%principito%")).first()
        if libro_reservado:
            reserva = Reserva(
                libro_id=libro_reservado.id,
                usuario_email="usuario@ejemplo.com",
                fecha_reserva=date.today(),
                fecha_vencimiento=date.today() + timedelta(days=7)
            )
            db.add(reserva)
            libro_reservado.estado = EstadoLibro.RESERVADO
            db.commit()

        logger.info("Base de datos inicializada con éxito desde el CSV limpio.")
    
    except Exception as e:
        logger.error(f"Error inicializando la base de datos: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
