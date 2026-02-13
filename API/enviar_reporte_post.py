import requests
import time

URL_DESTINO = "	https://webhook.site/bf54b15f-d4a0-430f-b9a0-517ade43ca68"

def enviar_reporte_sistema(btc_actual, temp_actual):
    reporte = {
        "estatus": "Sistema_OK",
        "usuario": "jesus_DevOps",
        "datos": {
            "bitcoin_price": btc_actual,
            "valencia_temp": temp_actual
        },
        "mensaje": "Reporte generado automaticamente desde el Sistema Maestro"
    }

    try:
        respuesta = requests.post(URL_DESTINO, json=reporte, timeout=10)

        if respuesta.status_code == 200:
            print("Reporte enviado con exito")
        else:
            print(f"El servidor recibio la carta pero respondio con error: {respuesta.status_code}")
    except Exception as e:
        print(f"Error al intentar enviar el Post: {e}")

enviar_reporte_sistema(67500, 28.4)