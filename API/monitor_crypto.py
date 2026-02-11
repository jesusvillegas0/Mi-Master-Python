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
    
print("Iniciando monitoreo... (Presiona Ctrl + C para detener)")

def enviar_mensaje_telegram(mensaje):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"

    try:
        requests.get(url, timeout=15)
        print("Eureka")
    except Exception:
        print("Telegram fuera de servicio temporalmente (Timeout)")

aviso_enviado = False

try:
    while True:
        precio_btc, precio_eth = consultar_precios()

        if precio_btc and precio_eth:
            hora_actual = time.strftime("%d-%m-%Y %H:%M:%S")
            print(f"[{hora_actual}] BTC: ${precio_btc} | ETH: ${precio_eth}")
            db.registrar_precios_cripto("Bitcoin",precio_btc)
            db.registrar_precios_cripto("Ethereum", precio_eth)
            if precio_btc >= 67100 and not aviso_enviado:
                msg = f"El precio del BTC ha subido a {precio_btc}"
                print("El BTC subio....")
                enviar_mensaje_telegram(msg)
                aviso_enviado = True
            elif precio_btc < 67100:
                aviso_enviado = False
        time.sleep(60)
        #db.consultar_precio_cripto()

except KeyboardInterrupt:
    print("Monitoreo detenido por el usuario. Hasta luego!")

