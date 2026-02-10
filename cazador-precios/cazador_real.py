import requests
from bs4 import BeautifulSoup

url = "https://www.coolmod.com/asustor-as1102t-v2-nas-2-bahias/"

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

try:
    session = requests.Session()
    respuesta = session.get(url, headers=cabeceras, timeout=10)
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    print(respuesta.status_code)
    precio_elemento = soup.find('span', {'id': 'pdp-price'})

    if precio_elemento:
        precio_texto = precio_elemento.text
        precio_limpio = precio_texto.replace('€', '').replace(',', '.').strip()
        precio_final = float(precio_limpio)

        print("Producto: Ryzen 7 5700x")
        print(f"Precio actual: {precio_elemento}€")

        if precio_final < 170:
            print("!!! CHOLLO DETECTADO !!!")
        else:
            print("No pude encontrar el precio. Puede ue hayan cambiado el diseño de la web")
except Exception as e:
    print(f"Error al conectar: {e}")