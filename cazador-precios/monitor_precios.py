import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

respuesta = requests.get(url, headers=cabeceras, timeout=15)
soup = BeautifulSoup(respuesta.text, 'html.parser')

nombre = soup.find('h1').text

precio_texto = soup.find('p', class_='price_color').text
precio_limpio = precio_texto.replace('Â£', '').strip()
precio_numero = float(precio_limpio)

#print(f"Producto: {nombre}")
#print(f"Precio encontrado: {precio_numero}")
#print(type(precio_numero))

print(f"DEBUG: El precio capturado es {precio_numero}")


if precio_numero < 40:
    print(f"¡OFERTA! El libro está a {precio_numero}. ¡Cómpralo ya!")
else:
    print(f" Sigue caro ({precio_numero}). Esperemos a que baje de 40")
