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

    def leer_emails_no_leidos(self):
        """Lee correos no leídos de la bandeja de entrada"""
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.username, self.password)
        mail.select("inbox")

        _, data = mail.search(None, "UNSEEN")  # Buscar correos no leídos
        correos = []

        for num in data[0].split():
            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = BytesParser().parsebytes(msg_data[0][1])
            cuerpo = msg.get_payload(decode=True).decode(errors="ignore")
            correos.append({
                "de": msg.get("from"),
                "asunto": msg.get("subject"),
                "cuerpo": cuerpo
            })

        mail.logout()
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
