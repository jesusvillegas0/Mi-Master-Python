from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from base_datos import BaseDatos
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

db = BaseDatos("backups_sistema.db")
db.crear_tabla_stock()


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

productos = [
    {"nombre": "A Light in the Attic", "url": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"},
    {"nombre": "Tipping the Velvet", "url": "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"},
    #{"nombre": "Soumission", "url": "http://books.toscrape.com/catalogue/soumission_998/index.html"}
]

def enviar_telegram(mensaje):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"

    try:
        requests.get(url, timeout=20)
        print("Eureka")
    except Exception as e:
        print("No se pudo")



    """
    intentos = 3

    for i in range(intentos):        
        try:
            requests.get(url, timeout=20)
            print(f"Notificacion enviada (Intento {i+1})")
            return
        except Exception as e:
            print(f"Intento {i+1} fallo... reintentando en 2 segundos.")
            time.sleep(2)
    print("No se pudo enviar a Telegram tras 3 intentos.")
    """

try:
    for p in productos:
        print(f"\nMonitoreando: {p['nombre']}...")
        driver.get(p['url'])

        espera = WebDriverWait(driver, 30)

        precio_elem = espera.until(EC.presence_of_element_located((By.CLASS_NAME, "price_color")))
        precio_num = float(precio_elem.text.replace('£', '').strip())


        stock_elem = driver.find_element(By.CLASS_NAME, "instock")
        texto_stock = stock_elem.text

        esta_disponible = 1 if "In stock" in texto_stock else 0

        precio_anterior = db.obtener_ultimo_precio(p["nombre"])

        precio_num = 19.0

        if precio_anterior is None:
            db.registrar_monitoreo(p['nombre'], precio_num, esta_disponible)
            print(f"{p['nombre']}: Primer registro guardado ({precio_num}£)")

        elif precio_num < precio_anterior:
            ahorro = precio_anterior - precio_num
            db.registrar_monitoreo(p["nombre"], precio_num, esta_disponible)
            print("Alerta oferta")
            print(f"\n{p['nombre']} ha bajado {round(ahorro, 2)}£. Precio actual: {precio_num}£)")

            texo_alerta = f"Oferta detectada \nProducto: {p['nombre']}\nBajo: {round(ahorro, 2)}£\nPrecio actual: {precio_num}£"

            enviar_telegram(texo_alerta)
            time.sleep(5)
            #print("Notificacion enviada a Telegram")


        elif precio_num > precio_anterior:
            db.registrar_monitoreo(p["nombre"], precio_num, esta_disponible)
            print(f"Subida de precio: {p['nombre']} ahora cuesta {precio_num}£ (Antes: {precio_anterior}£)")
        else:
            print("Precio es igual al registrado!!!")  
       
        
        """
        precio_actual = db.obtener_ultimo_precio(p["nombre"])
        if precio_actual is None or precio_num != precio_actual:
            db.registrar_monitoreo(p['nombre'], precio_num, esta_disponible) 
         
           print(f"\nGuardado: {p['nombre']} a {precio_num}£")
        """
            
        time.sleep(2)
    db.consultar_stock()
except Exception as e:
    print(f"Error critico: {e}")