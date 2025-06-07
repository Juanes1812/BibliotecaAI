from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Prompt simple de prueba
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Eres un asistente para un sistema de biblioteca. 
    Recibes solicitudes en español que incluyen títulos de libros también en español.
    Dame solo el SQL, sin explicaciones ni comentarios.

    Tu tarea es:
    1. Trael el título del libro para contruir la consulta SQL.
    2. Usar los nombres de tablas y columnas en español en la consulta SQL.
    4. Usar formato de fechas YYYY-MM-DD o CURRENT_DATE.
    5. Para reservas, la fecha de vencimiento será 7 días después de la fecha de reserva.

    Estructura de la base de datos:
    - libros(id, titulo, autor, isbn, estado)
    - reservas(id, libro_id, usuario_email, fecha_reserva, fecha_vencimiento)

    Ejemplos:
    - "Reservar el libro 'Cien años de soledad'" →
      INSERT INTO reservas (libro_id, usuario_email, fecha_reserva, fecha_vencimiento) SELECT id, 'juan@example.com', DATE('now'), DATE('now', '+7 days') FROM libros WHERE titulo = 'Cien años de soledad';

    - "Mostrar los libros reservados por 'juan@example.com'" →
      SELECT l.titulo, l.autor FROM libros l JOIN reservas r ON l.id = r.libro_id WHERE r.usuario_email = 'juan@example.com';
    """),
    ("human", "{user_request}")
])

# Crea el LLM de Ollama
chain = prompt | ChatOllama(model="phi", temperature=0)

# Ejecuta prueba
respuesta = chain.invoke({"user_request": "Reservar el libro 'La carpa roja'"})
print("Respuesta del modelo:\n", respuesta.content)
