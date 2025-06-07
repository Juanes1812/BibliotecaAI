import csv
import logging
import asyncio
from datetime import date, timedelta
from sqlalchemy import select
from app.db.session import async_session, engine
from app.db.base import Base
from app.models.libro import Libro, Reserva
from app.models.enums import EstadoLibro  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = "data/processed/books_clean.csv"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    libros = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            libros.append(
                Libro(
                    titulo=row['title'][:300],
                    autor=row['authors'][:800],
                    isbn=row['isbn13'][:20],
                    estado=EstadoLibro.DISPONIBLE
                )
            )
    
    async with async_session() as session:
        try:
            session.add_all(libros)
            await session.commit()

            # Consultar libro async
            result = await session.execute(
                select(Libro).where(Libro.titulo.like("%El alquimista%"))
                )
            
            libro_reservado = result.scalars().first()

            if libro_reservado:
                reserva = Reserva(
                    libro_id=libro_reservado.id,
                    usuario_email="usuario@ejemplo.com",
                    fecha_reserva=date.today(),
                    fecha_vencimiento=date.today() + timedelta(days=7)
                )
                session.add(reserva)
                libro_reservado.estado = EstadoLibro.RESERVADO

                await session.commit()

            logger.info("Base de datos inicializada con éxito desde el CSV limpio.")

        except Exception as e:
            logger.error(f"Error inicializando la base de datos: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(init_db())
