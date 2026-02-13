import requests

def simular_login_con_headers(usuario, password):
    url = "https://reqres.in/api/login"

    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    credenciales = {
        "email": usuario,
        "password": password
    }

    try:

        respuesta = requests.post(url, json=credenciales, headers=cabeceras, timeout=10)

        if respuesta.status_code == 200:
            token = respuesta.json().get("token")
            print(f"Exito! Token: {token}")
        elif respuesta.status_code == 403:
            print("El servidor sigue bloqueando la peticion (403 Forbidden)")
        else:
            print(f"Codigo recibido: {respuesta.status_code} - {respuesta.text}")
    except Exception as e:
        print(f"Error de red: {e}")

simular_login_con_headers("eve.holt@reqres.in", "cityslicka")