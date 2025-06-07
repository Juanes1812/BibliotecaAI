import requests
import time

url = "http://localhost:8000/api/procesar-solicitud"
data = {"solicitud": "Reservar el libro 'V de Vendeta'"}

start = time.time()
response = requests.post(url, json=data)
end = time.time()

print(f"Tiempo: {end - start} segundos")
print(response.json())
