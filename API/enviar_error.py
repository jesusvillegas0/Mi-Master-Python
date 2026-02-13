import requests
import time

def enviar_log_error(servicio, nivel_error, descripcion):
    url = "https://jsonplaceholder.typicode.com/posts"

    log = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "servicio": servicio,
        "level": nivel_error,
        "details": descripcion,
        "node": "Valencia-Srv-01"
    }

    try:

        respuesta = requests.post(url, json=log, timeout=10)

        if respuesta.status_code == 201:
            print(f"Log enviado: {nivel_error} en {servicio}")
            print(f"ID del reporte en el servidor: {respuesta.json()['id']}")
        else:
            print(f"Error al enviar reporte: {respuesta.status_code}")
    except Exception as e:
        print(f"Fallo total de la conexion: {e}")

enviar_log_error("Base_de_Datos", "Critial", "La conexion se perdio por falta de RAM")
time.sleep(2)
enviar_log_error("API_Crypto", "WARNING", "El internet esta lento, reintentand...")