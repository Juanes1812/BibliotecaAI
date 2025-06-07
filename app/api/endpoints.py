from fastapi import APIRouter, Depends, Body  
from app.llm.query_generator import BilingualQueryProcessor
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import asyncio, time, logging

router = APIRouter()
processor = BilingualQueryProcessor()
logger = logging.getLogger("uvicorn.error")

@router.post("/procesar-solicitud")
async def procesar_solicitud(payload: dict = Body(...), db: AsyncSession = Depends(get_db)):
    start = time.time()

    try:
        correo_usuario = payload.get("correo")
        mensaje_usuario = payload.get("solicitud")

        if not mensaje_usuario or not correo_usuario:
            raise ValueError("No se pudo extraer la solicitud del mensaje.")

        print(f"Correo: {correo_usuario}")
        print(f"Solicitud: {mensaje_usuario}")

        # 1. Generar SQL desde lenguaje natural usando un hilo para no bloquear
        sql = await asyncio.to_thread(processor.generate_sql, mensaje_usuario, correo_usuario)
        print(f"SQL generado: {sql}")
# 3. Ejecutar SQL
        try:
            result = await db.execute(text(sql))
            await db.commit()
            logger.info(f"✅ SQL ejecutado, filas afectadas: {result.rowcount}")
        except Exception as sql_err:
            logger.error(f"❌ Error ejecutando SQL: {sql_err}")
            raise

        # 4. Si es SELECT, formatear los datos para el usuario
        if sql.strip().lower().startswith("select"):
            rows = result.fetchall()
            data = [dict(row._mapping) for row in rows]
            respuesta = {
                "resultado": data,
                "tipo": "consulta",
                "correo_usuario": correo_usuario
            }
        else:
            # Si fue INSERT/UPDATE/DELETE, genera respuesta natural
            mensaje_respuesta = await asyncio.to_thread(
                processor.generate_response,
                sql
            )
            respuesta = {
                "respuesta": mensaje_respuesta,
                "tipo": "accion",
                "correo_usuario": correo_usuario
            }

        logger.info(f"⏱ Tiempo total: {time.time() - start:.2f}s")
        return respuesta

    except Exception as e:
        return {"error": f"Error procesando solicitud: {str(e)}"}
