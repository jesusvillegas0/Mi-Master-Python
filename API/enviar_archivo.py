import requests

def subir_archivo_al_servidor(ruta_archivo):
    url = "https://httpbin.org/post"

    try: 

        with open (ruta_archivo, 'rb') as archivo_binario:
            paquete_archivo = {'file': archivo_binario}

            print(f"Subiendo {ruta_archivo}...")
            respuesta = requests.post(url, files=paquete_archivo, timeout=10)

            if respuesta.status_code == 200:
                print("Archivo recibido por el servidor")
                datos_recibidos = respuesta.json()
                print(f"El servidor guardo un archivo de tamaño: {len(datos_recibidos['files']['file'])}bytes")
            else:
                print(f" Fallo: {respuesta.status_code}")

    except FileNotFoundError:
        print("Error: No encontre el archivo. Verifica el nombre")
    except Exception as e:
        print(f"Error de red: {e}")

subir_archivo_al_servidor("imagen.jpg")