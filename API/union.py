import requests
import time
import os 
from dotenv import load_dotenv
from base_datos import BaseDatos

load_dotenv()

db = BaseDatos("Monitoreo_proyectos.db")
db.crear_tabla_clima()

def obtener_datos_completos():
    url_crypto = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    url_clima = "https://api.open-meteo.com/v1/forecast?latitude=10.16&longitude=-68.00&current_weather=true"

    try:
        res_crypto = requests.get(url_crypto, timeout=10)
        res_clima =  requests.get(url_clima, timeout=10)

        res_crypto.raise_for_status()
        res_clima.raise_for_status()

        datos_crypto = res_crypto.json()
        datos_clima = res_clima.json()

        btc = datos_crypto["bitcoin"]["usd"]
        eth = datos_crypto["ethereum"]["usd"]
        temp = datos_clima["current_weather"]["temperature"]

        return btc, eth, temp
    except Exception as e:
        print(f"Error al cargar: {e}")
        return None, None, None

print("Sistema Maestro iniciado...Guardando cada 5 minutos")

try:
    while True:
        btc, eth, temp = obtener_datos_completos()

        if btc is not None:
            hora = time.strftime("%d-%m-%Y %H:%M:%S")
            print(f"[{hora}] BTC:{btc} | ETH:{eth} | Clima Valencia: {temp}°C")
            db.registrar_precios_cripto("Bitcoin", btc)
            db.registrar_precios_cripto("Ethereum", eth)
            db.registrar_clima_proyecto(temp)
        time.sleep(300)

except KeyboardInterrupt:
    print("Sistema Apagado...")
