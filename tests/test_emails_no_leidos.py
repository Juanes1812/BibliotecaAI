from app.services.gmail_service import GmailService

gmail = GmailService()

correos = gmail.leer_emails_no_leidos()

for correo in correos:
    print("📩 Nuevo mensaje:")
    print("De:", correo["de"])
    print("Asunto:", correo["asunto"])
    print("Cuerpo:", correo["cuerpo"])
