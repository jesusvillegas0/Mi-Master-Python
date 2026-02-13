import requests
import time
import os
from dotenv import load_dotenv
from base_datos import BaseDatos

load_dotenv()

db = BaseDatos("Monitoreo_cripto.db")
db.crear_tabla_cripto()

def consultar_precios():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    try:

        respuesta = requests.get(url, timeout=10)

        datos = respuesta.json()

        btc = datos["bitcoin"]["usd"]
        eth = datos["ethereum"]["usd"]
            
        return btc, eth
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None, None
    