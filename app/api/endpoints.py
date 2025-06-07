from fastapi import APIRouter, Depends, Body  
from app.llm.query_generator import BilingualQueryProcessor
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import asyncio
import time

router = APIRouter()
processor = BilingualQueryProcessor()

@router.post("/procesar-solicitud")
async def procesar_solicitud(solicitud: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    start = time.time()

    try:
        # 1. Generar SQL desde lenguaje natural usando un hilo para no bloquear
        sql = await asyncio.to_thread(processor.generate_sql, solicitud)
        print(f"SQL generado: {sql}")

        # 2. Ejecutar la instrucción SQL (INSERT, UPDATE, DELETE, etc.)
        await db.execute(text(sql))
        await db.commit()  # Confirma los cambios

        # 3. Generar una respuesta en lenguaje natural (solo confirma éxito)
        respuesta = await asyncio.to_thread(processor.generate_response, "Operación completada correctamente.")

        print(f"⏱ Tiempo total: {time.time() - start:.2f}s")

        return {"respuesta": respuesta}

    except Exception as e:
        return {"error": f"Error procesando solicitud: {str(e)}"}