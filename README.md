# Biblioteca IA - Sistema de Gestión de Libros por Email

## Descripción
Sistema que permite gestionar reservas de libros mediante solicitudes por correo electrónico, utilizando inteligencia artificial para interpretar los mensajes y ejecutar las acciones correspondientes.

## Requisitos
- Python 3.8+
- Descargar el modelo LLM de Ollama llamado 'phi'

## Instalación
1. Clonar repositorio:
   ```bash
   git clone https://github.com/Juanes1812/BibliotecaAI.git
   cd BibliotecaAI

2. Configurar entorno virtual:

    python -m venv venv

    source venv/bin/activate  # Linux/Mac

    .\venv\Scripts\activate   # Windows

3. Instalar dependencias:

    pip install -r requirements.txt

4. Configurar variables de entorno:
        
    copy .env.example .env  # Windows

    cp .env.example .env    # Linux/Mac

5. Configuración (.env):

    smtp_username=tu_correo@gmail.com       # Tu dirección de Gmail

    app_password=tu_clave_de_aplicacion     # Contraseña de aplicación (generada en Google)

    
    DATABASE_URL=sqlite+aiosqlite:///./nombre_base_datos.db # Configuracion para la base de datos

6. Para cargar la base de datos(si no se tiene aún):

    python -m app.scripts.init_db

7. Activar la carga de correos:

    python -m app.scripts.gmail_complete_process

8. Ejecutar el programa:

    uvicorn app.main:app --reload

9. Uso:

    Acceso de la API: http://localhost:8000/api

    Documentación Swagger: http://localhost:8000/docs
    
10. Envía correos con comandos como:
    - "Reservar el libro 'El alquimista'"
    - "Cancelar una reserva 'La granja de animales'"
    - "Renovar una reserva 'Cien años de soledad'"
    - "Mostrar libros disponibles"
    - "Mostrar mis libros reservados"
    - "Agregar un libro '1984', 'George Orwell', '1234567890', 'disponible'"
    - "Eliminar el libro 'El principito'"

11. Endpoints principales:

    POST /procesar-solicitud: Procesa solicitudes (requiere un correo y mensaje para funcionar)

## Uso

Una vez hechos todos los pasos, mandar un coreo con alguno de los comandos del punto 10.
Si has enviado exitosamente la información, verá como se le envia un correo con una respuesta del comando enviado.

