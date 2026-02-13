import requests

def consultar_clima_pro():
    lat = 10.16
    lon = -68.00
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        temp = datos["current_weather"]["temperature"]
        viento = datos["current_weather"]["windspeed"]

        return temp, viento
    
    except Exception as e:
        print(f"Error tecnico: {e}")
        return None, None
    
temperatura, viento = consultar_clima_pro()
