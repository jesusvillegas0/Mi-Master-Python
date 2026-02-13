import requests

def similar_login(usuario, password):
    url = "https://reqres.in/api/login"

    credenciales = {
        "email": usuario,
        "password": password
    }

    try:
        print(f"Intentando conectar con las credenciales de : {usuario}")

        respuesta = requests.post(url, json=credenciales, timeout=10)

        if respuesta.status_code == 200:
            datos = respuesta.json()
            token = datos.get("token")
            print(f"Login exitoso! El servidor ns dio este token de acceso: {token}")
            return token
        elif respuesta.status_code == 400:
            error_msg = respuesta.json().get("error")
            print(f"Error 400 (Bad Request): {error_msg}")
        else:
            print(f"Algo salio mal. Codigo: {respuesta.status_code}")
    except Exception as e:
        print(f"Error de red: {e}")

token_recibido = similar_login("eve.holt@reqres.in", "cityslicka")

print("\n--- Segunda prueba (Error provocado) ---")
similar_login("jesus@devops.com", "12345")