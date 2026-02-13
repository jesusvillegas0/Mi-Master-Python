import requests
import time

URL_DESTINO = "http://localhost:5000/reporte"

def enviar_reporte_sistema(btc_actual, temp_actual):
    reporte = {
        "bitcoin_price": btc_actual,
        "valencia_temp": temp_actual
    }

    try:
        respuesta = requests.post(URL_DESTINO, json=reporte, timeout=10)

        if respuesta.status_code == 200:
            print("Reporte enviado con exito")
        else:
            print(f"El servidor recibio la carta pero respondio con error: {respuesta.status_code}")
    except Exception as e:
        print(f"Error al intentar enviar el Post: {e}")

enviar_reporte_sistema(67400, 31.1)