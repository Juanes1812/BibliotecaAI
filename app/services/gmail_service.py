import smtplib
import imaplib
from email.parser import BytesParser
from email.mime.text import MIMEText
from app.core.config import settings

class GmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.imap_server = "imap.gmail.com"
        self.username = settings.smtp_username
        self.password = settings.app_password   

        print("USUARIO:", self.username)
        print("CONTRASEÑA:", self.password)



    def leer_emails_no_leidos(self):
        """Lee correos no leídos de la bandeja de entrada y muestra progreso"""
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.username, self.password)
        mail.select("inbox")

        _, data = mail.search(None, "UNSEEN")  # Buscar correos no leídos
        ids = data[0].split()
        print(f"🔍 Correos no leídos encontrados: {len(ids)}")

        correos = []

        for idx, num in enumerate(ids, start=1):
            print(f"📥 Leyendo correo {idx}/{len(ids)} con ID: {num.decode()}")

            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = BytesParser().parsebytes(msg_data[0][1])

            cuerpo = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        payload = part.get_payload(decode=True)
                        if payload:
                            cuerpo = payload.decode(errors="ignore")
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    cuerpo = payload.decode(errors="ignore")

            correo = {
                "de": msg.get("from"),
                "asunto": msg.get("subject"),
                "cuerpo": cuerpo
            }

            print(f"✅ Correo {idx} leído: De: {correo['de']}, Asunto: {correo['asunto']}")
            correos.append(correo)

        mail.logout()
        print(f"📬 Total de correos procesados: {len(correos)}")
        return correos

    def enviar_email(self, destinatario, asunto, cuerpo):
        """Envía un correo electrónico"""
        mensaje = MIMEText(cuerpo)
        mensaje["From"] = self.username
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(mensaje)
            server.quit()
