from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True) 
chrome_options.add_argument("--remote-allow-origins=*")

try: 
    print("Paso 1: Buscando el driver compatible...") # Esta es la línea mágica que descarga el driver correcto ruta = ChromeDriverManager().install() service = Service(ruta)

except Exception as e: print("Error:", e)