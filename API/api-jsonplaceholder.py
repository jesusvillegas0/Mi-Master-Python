import requests

url = "https://jsonplaceholder.typicode.com/posts"

mi_post = {
    "title": "Reporte DevOps",
    "body": "Todo funciona fino",
    "userId": 1
}

res = requests.post(url, json=mi_post, timeout=10)
print(f"Codigo: {res.status_code}")
print(f"Respuesta del servidor: {res.json()}")
