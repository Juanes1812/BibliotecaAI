import time
from app.services.gmail_service import GmailService
from app.services.gmail_processor import GmailProcessor

if __name__ == "__main__":
    gmail = GmailService()
    api_url = "http://localhost:8000/api/procesar-solicitud"
    processor = GmailProcessor(gmail_service=gmail, api_url=api_url)

    while True:
        print("🔄 Revisando nuevos correos...")
        processor.procesar_emails()
        print("✅ Revisión completa. Esperando 60 segundos...\n")
        time.sleep(60) 

