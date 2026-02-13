from flask import Flask, request, jsonify, render_template
from base_datos import BaseDatos
import clima_pro
import monitor_crypto

app = Flask(__name__)

db = BaseDatos("Monitoreo_proyectos.db")
db.crear_tabla_cripto()
db.crear_tabla_clima()



@app.route('/')
def inicio():
    return "<h1>Centro de Mando con Base de Datos Activo</h1>"

@app.route('/reporte', methods=['POST'])
def recibir_reporte():
    datos = request.json

    if not datos:
        return jsonify({"Error": "No se enviaron datos"}), 400

    btc = datos.get('bitcoin_price')
    temp = datos.get('valencia_temp')

    print(f"Procesando: BTC ${btc} | Clima {temp}°C")

    try:
        if btc:
            db.registrar_precios_cripto("Bitcoin", btc)
        if temp:
            db.registrar_clima_proyecto(temp)

        return jsonify({
            "status": "Exito",
            "mensaje": "Datos guardados en la base de datos correctamente."
        }), 200

    except Exception as e:
        print(f"Error al guardar en DB: {e}")
        return jsonify({"status": "Error", "mensaje": str(e)}), 500

@app.route('/ver-datos')
def ver_datos():
    criptos, clima = db.obtener_historial_completo()

    return render_template('index.html', lista_criptos=criptos, lista_clima=clima)

@app.route('/actualizar-ahora', methods=['POST'])
def actualizar_ahora():
    try:
        btc = monitor_crypto.consultar_precios()
        temp = clima_pro.consultar_clima_pro()

        db.registrar_precios_cripto("Bitcoin", btc[0])
        db.registrar_clima_proyecto(temp[1])

        return jsonify({"status": "ok", "btc": btc[0], "temp": temp[0]}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
