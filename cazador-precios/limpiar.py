from base_datos import BaseDatos

db = BaseDatos("backups_sistema.db")

def resetear_base_datos():
    orden_sql = "DROP TABLE IF EXISTS monitoreo_stock"
    db.cursor.execute(orden_sql)
    db.conexion.commit()

    db.cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoreo_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT,
    precio REAL,
    disponible INTEGER,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    db.conexion.commit()
    print("Base de datos reseteada. ¡Lista para datos reales!")

resetear_base_datos()