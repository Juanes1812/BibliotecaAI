# Biblioteca IA - Sistema de Gestión de Libros por Email

## Descripción
Sistema que permite gestionar reservas de libros mediante solicitudes por correo electrónico, utilizando inteligencia artificial para interpretar los mensajes y ejecutar las acciones correspondientes.

## Requisitos
- Python 3.8+
- Cuenta de Azure para Graph API
- Cuenta de OpenAI o proveedor de LLM

## Instalación
1. Clonar repositorio:
   ```bash
   git clone https://github.com/Juanes1812/BibliotecaAI.git
   cd BibliotecaAI

2. Configurar entorno virtual:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows

3. Instalar dependencias
    pip install -r requirements.txt

4. Configurar variables de entorno:
        
    copy .env.example .env  # Windows
    cp .env.example .env    # Linux/Mac

5. Ejecutar el programa:
    uvicorn app.main:app --reload

6. Configuración (.env):
    # Base de datos
    DATABASE_URL=sqlite:///./biblioteca.db


    # Configuracion con Mailtrap
    SMTP_SERVER=sandbox.smtp.mailtrap.io
    SMTP_PORT=puerto_de_tu_eleccion
    SMTP_USERNAME=tu_username_id
    SMTP_PASSWORD=tu_password

    # LLM
    LLM_API_KEY=tu_api_key

7. Para cargar la base de datos:
    python -m app.scripts.init_db


7. Uso:
    Accede a la API: http://localhost:8000

    Documentación Swagger: http://localhost:8000/docs

    Envía correos con comandos como:
    "Reservar El Principito"
    "Listar libros disponibles"

8. Despliegue en Azure:
    docker build -t biblioteca-ia .
    az acr build --registry <nombre-registro> --image biblioteca-ia .

9. Endpoints principales:
    POST /procesar-email: Procesa nuevos correos

    GET /libros: Lista todos los libros

    POST /reservas: Crea nueva reserva

