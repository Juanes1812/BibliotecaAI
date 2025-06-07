from app.services.gmail_service import GmailService

# Instanciar el servicio
gmail = GmailService()

# Cambia esto al correo de destino
destinatario = "juan.monsalve39@correo.tdea.edu.co"
asunto = "📚 Prueba desde el sistema de biblioteca"
cuerpo = "Hola, este es un correo de prueba enviado por el sistema."

# Enviar
gmail.enviar_email(destinatario, asunto, cuerpo)
print("Correo enviado ✅")
