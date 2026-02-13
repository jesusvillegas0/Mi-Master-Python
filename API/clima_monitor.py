import requests

def consultar_clima(ciudad):
    url = f"https://wttr.in/{ciudad}?format=j1"

    try:
        respuesta = requests.get(url, timeout=10)
        datos = respuesta.json()

        temperatura = datos["current_condition"][0]["temp_C"]
        descripcion = datos["current_condition"][0]["lang_es"][0]["value"]

        return temperatura, descripcion

    except Exception as e:
        print(f"Error al consultar: {e}")
        return None, None
"""
ciudad_usuario = "Valencia, Venezuela"
temp, desc = consultar_clima(ciudad_usuario)

if temp:
    print(f"Reporte para {ciudad_usuario}:")
    print(f"Temperatura: {temp}°C")
    print(f"Estado: {desc}")
"""
resultado = consultar_clima("Valencia,Venezuela")

if resultado[0] is not None:
    temp, desc = resultado
    print(f"Clima: {temp}°C, {desc}")
else:
    print("Problemas de red")