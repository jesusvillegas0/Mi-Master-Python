import sqlite3

class BaseDatos:
    def __init__(self, nombre_bd):
        self.conexion = sqlite3.connect(nombre_bd)
        self.cursor = self.conexion.cursor()
        self.crear_tablas()
    
    def crear_tablas(self):
        orden_sql = """
        CREATE TABLE IF NOT EXISTS servidores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        ruta TEXT NOT NULL,
        prefijo TEXT NOT NULL,
        formato_fecha TEXT NOT NULL)
        """
        self.cursor.execute(orden_sql)
        self.conexion.commit()
    
    def insertar_servidor(self, nombre, ruta, prefijo, formato_fecha):
        orden_sql = "INSERT INTO servidores (nombre, ruta, prefijo, formato_fecha) VALUES (?, ?, ?, ?)"
        self.cursor.execute(orden_sql, (nombre, ruta, prefijo, formato_fecha))
        self.conexion.commit()
        print(f"Servidor '{nombre}' guardado en la BD.")

    def consultar_servidores(self):
        orden_sql = "SELECT * FROM servidores"
        self.cursor.execute(orden_sql)
        
        servidores = self.cursor.fetchall()
        
        for fila in servidores:
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Ruta: {fila[2]} | Prefijo: {fila[3]} | formato: {fila[4]}")
        
        return servidores
    
    def eliminar_datos(self):
        orden_sql = "DELETE FROM servidores"
        self.cursor.execute(orden_sql)

        servidores = self.cursor.fetchall()

        print(servidores)

    def agregar_servidor_interativo(self):
        print("\n--- Agregar Nuevo servidor al Monitoreo ---")
        nombre = input("Nombre del servidor: ")
        ruta = input("Ruta de red (ej. \\\\192.168...): ")
        prefijo = input("Prefijo del archivo: ")
        formato = input("Formato de fecha (ej. %Y-%m-%d): ")

        try:
            self.insertar_servidor(nombre, ruta, prefijo, formato)
            print("Servidor agregado con exito.")
        except Exception as e:
            print(f"Error al agregar: {e}")

    def eliminar_servidor(self, id_servidor):
        orden_sql = "DELETE FROM servidores WHERE id = ?"
        self.cursor.execute(orden_sql, (id_servidor,))
        self.conexion.commit()

        print(f"\nServidor con el {id_servidor} borrado con exito!!")

    def actualizar_servidor(self, id_servidor, nombre, ruta, prefijo, formato):
        orden_sql = "UPDATE servidores SET nombre = ?, ruta = ?, prefijo = ?, formato_fecha = ? WHERE id = ?"
        self.cursor.execute(orden_sql, (nombre, ruta, prefijo, formato, id_servidor))
        self.conexion.commit()

        print(f"El servidor {nombre} fue actualizado con exito...")

    def crear_tabla_noticias(self):
        orden_sql = """
        CREATE TABLE IF NOT EXISTS noticias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titular TEXT UNIQUE,
        enlace TEXT,
        fecha_extracion DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        self.cursor.execute(orden_sql)
        self.conexion.commit()

    def guardar_noticia(self, titular, enlace):
        try:
            orden_sql = "INSERT INTO noticias (titular, enlace) VALUES (?, ?)"
            self.cursor.execute(orden_sql, (titular, enlace))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            pass
    
    def consultar_noticias(self):
        orden_sql = "SELECT * FROM noticias"
        self.cursor.execute(orden_sql)
        noticias = self.cursor.fetchall()

        for noticia in noticias:

            print(f"ID: {noticia[0]} | Titular: {noticia[1]} | Enlace: {noticia[2]} | Fecha: {noticia[3]}")

        return noticias

    def crear_tabla_precios(self):
        orden_sql = """
        CREATE TABLE IF NOT EXISTS historico_precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        precio REAL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )        
        """
        self.cursor.execute(orden_sql)
        self.conexion.commit()

    def registrar_precios(self, producto, precio):
        orden_sql = "INSERT INTO historico_precios (producto, precio) VALUES (?, ?)"
        self.cursor.execute(orden_sql, (producto, precio))
        self.conexion.commit()

    def consultar_precios(self):
        orden_sql = "SELECT * FROM historico_precios"
        self.cursor.execute(orden_sql)
        respuestas = self.cursor.fetchall()

        for res in respuestas:
            print(f"Producto: {res[1]} | Precio: {res[2]} | Fecha: {res[3]}")

            return respuestas
        
    def crear_tabla_stock(self):
        orden_sql = """
        CREATE TABLE IF NOT EXISTS monitoreo_stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        precio REAL,
        disponible INTEGER,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(orden_sql)
        self.conexion.commit()
    
    def registrar_monitoreo(self, producto, precio, disponible):
        orden_sql = "INSERT INTO monitoreo_stock (producto, precio, disponible) VALUES (?, ?, ?)"
        self.cursor.execute(orden_sql, (producto, precio, disponible))
        self.conexion.commit()

    def consultar_stock(self):
        orden_sql = "SELECT * FROM monitoreo_stock ORDER BY fecha DESC"
        self.cursor.execute(orden_sql)
        precios = self.cursor.fetchall()
        
        for precio in precios:
            print(f"ID:{precio[0]} | Producto: {precio[1]} | Precio: {precio[2]} | Disponible: {precio[3]} | Fecha: {precio[4]}")
        
        #print(precios)
    
        return precios
    
    def eliminar_stock(self):
        orden_sql = "DELETE FROM monitoreo_stock"
        self.cursor.execute(orden_sql)
        self.conexion.commit()

        self.consultar_stock()

    def obtener_ultimo_precio(self, nombre_producto):
        orden_sql = "SELECT precio FROM monitoreo_stock WHERE producto = ? ORDER BY fecha DESC LIMIT 1"
        self.cursor.execute(orden_sql, (nombre_producto,))
        ultimo_precio = self.cursor.fetchone()
        
        #print(ultimo_precio[0])
        if ultimo_precio is not None:
        
            return ultimo_precio[0]
        
        """
        for precio in ultimo_precio:
            price = precio[2]
        return price
        """
    
    def obtener_precio_minimo(self, nombre_producto):
        orden_sql = "SELECT MIN(precio) FROM monitoreo_stock WHERE producto = ?"
        self.cursor.execute(orden_sql, (nombre_producto,))
        resultado = self.cursor.fetchone()

        if resultado is not None:
            return resultado[0] 
        return None
    
    def crear_tabla_cripto(self):
        orden_sql = """
        CREATE TABLE IF NOT EXISTS cripto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP)
        """
        self.cursor.execute(orden_sql)
        self.conexion.commit()
    
    def registrar_precios_cripto(self, nombre, precio):
        orden_sql = "INSERT INTO cripto (nombre, precio) VALUES (?, ?)"
        self.cursor.execute(orden_sql,(nombre, precio))
        self.conexion.commit()

    def consultar_precio_cripto(self):
        orden_sql = "SELECT * FROM cripto"
        self.cursor.execute(orden_sql)
        respuesta = self.cursor.fetchall()

        for i in respuesta:
            print(f"ID:{i[0]} | Nombre:{i[1]} | Precio:{i[2]} | Fecha: {i[3]}")

        return respuesta

