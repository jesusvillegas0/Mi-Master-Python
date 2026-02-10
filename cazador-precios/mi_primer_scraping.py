import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from base_datos import BaseDatos

#url = "https://es.wikipedia.org/wiki/Python"
url = "https://www.genbeta.com"

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

}

datos_noticias = []


respuesta = requests.get(url, headers=cabeceras, timeout=15)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    titulo = soup.find('h2').text
    print(f" Conexion exitosa. El titulo es: {titulo}")
else:
    print(f"No pudimos entrar. Codigo de error: {respuesta.status_code}")

soup = BeautifulSoup(respuesta.text, 'html.parser')
parrafos = soup.find_all('p')

if len(parrafos) > 1:
    print("\n--- Resumen del primer parrafo ---")
    print(parrafos[1].text)

print("\n--- Primero 5 enlaces de la pagina ---")
enlaces = soup.find_all('a', limit=5)

for enlace in enlaces:
    texto = enlace.text
    url_destino = enlace.get('href')
    print(f"Texto: {texto} | Link: {url_destino}")

#base_url = "https://es.wikipedia.org"
base_url = "https://www.genbeta.com"


print("\n--- Enlaces Funcionales ---")
for enlace in enlaces:
    texto = enlace.text.strip()
    ruta = enlace.get('href')

    link_completo = urljoin(base_url, ruta)

    if texto:
        print(f" {texto} -> {link_completo}")

print("\n--- Ultimos Titulares de genbeta ---")
titulares = soup.find_all('h2')

"""
for titular in titulares:
    texto_limpio = titular.text.strip()

    etiqueta_a = titular.find('a')

    if etiqueta_a:
        link_noticia = etiqueta_a.get('href')
        link_final = urljoin(base_url, link_noticia)
        datos_noticias.append([texto_limpio, link_final])
    if len(texto_limpio) > 10:
        print(f"\n {texto_limpio}")
        print(f"Link: {link_final}")

nombre_archivo = "noticias_genbeta.csv"

with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
    archivo.write("sep=;\n")
    escritor = csv.writer(archivo, delimiter=';')
    escritor.writerow(["Titular", "Enlace"])
    escritor.writerows(datos_noticias)

print(f"\n ¡Éxito! Se han guardado {len(datos_noticias)} noticias en {nombre_archivo}")
"""
db_noticias = BaseDatos("backups_sistema.db")
db_noticias.crear_tabla_noticias()

print("\n--- Guardando en Base de Datos ---")
contador = 0

for titular in titulares:
    texto_limpio = titular.text.strip()
    etiqueta_a = titular.find('a')

    if etiqueta_a and len(texto_limpio) > 10:
        link_final = urljoin(base_url, etiqueta_a.get('href'))

        db_noticias.guardar_noticia(texto_limpio, link_final)
        contador += 1
print(f"\n Proceso terminado. Se intentaron procesar {contador} noticias.")
print("\n--- Mostrando las noticias ---")
db_noticias.consultar_noticias()
