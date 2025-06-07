import requests
import time

# URL de tu endpoint local
url = "http://localhost:8000/api/procesar-solicitud"

# Datos que normalmente vendrían desde un correo

# Enviar los datos al endpoint
data = {"solicitud": "Reservar el libro 'Hatchet'",
        "correo": "usuario11@example.com"}

start = time.time()
response = requests.post(url, json=data)
end = time.time()

# Mostrar el resultado
print(f"⏱️ Tiempo: {end - start:.2f} segundos")
print("📥 Respuesta del servidor:")
print(response.json())
