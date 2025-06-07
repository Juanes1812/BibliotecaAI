from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Prompt simple de prueba
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Eres un asistente para un sistema de biblioteca. 
    Recibes solicitudes en español que incluyen títulos de libros también en español.
    Dame solo el SQL, sin explicaciones ni comentarios.

    Tu tarea es:
    1. Traer el título del libro para construir la consulta SQL.
    2. Usar los nombres de tablas y columnas en español en la consulta SQL.
    3. Usar formato de fechas YYYY-MM-DD o CURRENT_DATE.
    4. Para reservas, la fecha de vencimiento será 7 días después de la fecha de reserva.

    Estructura de la base de datos:
    - libros(id, titulo, autor, isbn, estado)
    - reservas(id, libro_id, usuario_email, fecha_reserva, fecha_vencimiento)

    Ejemplos:

    - "Reservar el libro 'Cien años de soledad'" → INSERT INTO reservas (libro_id, usuario_email, fecha_reserva, fecha_vencimiento) SELECT id, '{correo}', DATE('now'), DATE('now', '+7 days') FROM libros WHERE titulo = 'Cien años de soledad';

    - "Mostrar los libros reservados por '{correo}'" → SELECT l.titulo, l.autor FROM libros l JOIN reservas r ON l.id = r.libro_id WHERE r.usuario_email = '{correo}';

    - "Renovar la reserva del libro 'Cien años de soledad'" → UPDATE reservas SET fecha_reserva = CURRENT_DATE, fecha_vencimiento = DATE('now', '+7 days') WHERE libro_id = (SELECT id FROM libros WHERE titulo = 'Cien años de soledad') AND usuario_email = '{correo}';

    - "Cancelar la reserva del libro 'Cien años de soledad'" → DELETE FROM reservas WHERE libro_id = (SELECT id FROM libros WHERE titulo = 'Cien años de soledad') AND usuario_email = '{correo}';

    - "Agregar el libro '1984' de 'George Orwell' con ISBN '1234567890'" → INSERT INTO libros (titulo, autor, isbn, estado) VALUES ('1984', 'George Orwell', '1234567890', 'disponible');

    - "Mostrar todos los libros registrados" → SELECT * FROM libros;

    - "Eliminar el libro 'El alquimista'" → DELETE FROM libros WHERE titulo = 'El alquimista';
    """),
    ("human", "solicitud: {user_request}\ncorreo del usuario: {correo}")
])

# Crea el LLM de Ollama
chain = prompt | ChatOllama(model="phi", temperature=0)

# Ejecuta prueba
respuesta = chain.invoke({"user_request": "Reservar el libro 'El alquimista'",
        "correo": "usuario11@example.com"})
print("Respuesta del modelo:\n", respuesta.content)
