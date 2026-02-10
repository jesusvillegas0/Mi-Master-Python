from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from base_datos import BaseDatos

db = BaseDatos("backups_sistema.db")
db.crear_tabla_precios()


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Buscando ofertas de forma invisible")
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    driver.get(url)

    espera = WebDriverWait(driver, 10)
    titulo_elemento = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product_main h1")))
    nombre_producto = titulo_elemento.text

    print(f"Analiando el producto: {nombre_producto}")
    
    precio_elemento = driver.find_element(By.CLASS_NAME, "price_color")
    precio_texto = precio_elemento.text

    precio_final = float(precio_texto.replace('£', '').strip())

    db.registrar_precios(nombre_producto, precio_final)

    print(f"\nGuardado en DB: {nombre_producto} a {precio_final}€")

    print("\nProductos y sus precios:")
    db.consultar_precios()
    
    print(f"\nPrecio capturado con exito: {precio_final}")
    if precio_final < 60:
        print("Es una ganga!!")
except Exception as e:
    print(f"Ocurrio un error: {e}")
finally:
    driver.quit()
    print("Navegador cerrado.")