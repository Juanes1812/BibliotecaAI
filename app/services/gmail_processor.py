import requests
from app.services.gmail_service import GmailService

class GmailProcessor:
    def __init__(self, gmail_service: GmailService, api_url: str):
        self.gmail_service = gmail_service
        self.api_url = api_url

    def procesar_emails(self):
        correos = self.gmail_service.leer_emails_no_leidos()

        for correo in correos:
            remitente = self._extraer_direccion(correo["de"])
            mensaje = correo["cuerpo"].strip()
        
            print(f"📥 Procesando correo de {remitente}: {mensaje}")

            # Envía el prompt a la API y obtiene la respuesta
            try:
                response = requests.post(self.api_url, json={"solicitud": mensaje, "correo": remitente})
                if response.status_code == 200:
                    data = response.json()
                    mensaje_respuesta = data.get("respuesta", "No se pudo generar una respuesta.")
                else:
                    mensaje_respuesta = f"Error: {response.text}"

                self.gmail_service.enviar_email(
                    destinatario=remitente,
                    asunto="📚 Respuesta a tu solicitud de BibliotecaIA",
                    cuerpo=mensaje_respuesta
                )
                print(f"📤 Respuesta enviada a {remitente}")

            except Exception as e:
                print(f"❌ Error procesando correo de {remitente}: {e}")

    def _extraer_direccion(self, from_header):
        if "<" in from_header and ">" in from_header:
            return from_header.split("<")[1].split(">")[0]
        return from_header.strip()
