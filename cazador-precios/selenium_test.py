from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opciones = Options()
# opciones.add_argument("--start-maximized") # Si quieres que abra en pantalla completa

try:
    print("Iniciando Chrome...")
    driver = webdriver.Chrome(options=opciones)

    driver.get("https://www.google.com")
    print(f"Titulo de la pagina: {driver.title}")

    time.sleep(5)
    driver.quit()
    print("Navegador cerrado correctamente.")
except Exception as e:
    print(f"Ocurrio un error: {e}")