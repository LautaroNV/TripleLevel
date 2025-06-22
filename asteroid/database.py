import mysql.connector

def guardar_puntuacion(nombre, puntuacion):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",        
        password="", 
        database="asteroids"
    )
    cursor = conexion.cursor()
    sql = "INSERT INTO puntuaciones (nombre, puntuacion) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, puntuacion))
    conexion.commit()
    conexion.close()

def obtener_top5():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="asteroids"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, puntuacion FROM puntuaciones ORDER BY puntuacion DESC LIMIT 5")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados
