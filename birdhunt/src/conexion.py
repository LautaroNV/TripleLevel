import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hunter_bird"
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print(" Conectado a la base de datos.")
        except Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def guardar_puntaje(self, nombre, puntuacion):
        if self.conn is None or not self.conn.is_connected():
            print("No hay conexión con la base de datos.")
            return

        try:
            sql = "INSERT INTO puntuaciones (nombre, puntuacion) VALUES (%s, %s)"
            self.cursor.execute(sql, (nombre, puntuacion))
            self.conn.commit()
            print(f"Puntaje guardado: {nombre} - {puntuacion}")
        except Error as e:
            print(f"Error al guardar puntaje: {e}")

    def obtener_puntuaciones(self):
        try:
            if self.conn.is_connected():
                self.cursor.execute("SELECT id, nombre, puntuacion FROM puntuaciones ORDER BY puntuacion DESC LIMIT 10")
                return self.cursor.fetchall()
        except Error as e:
            print(f"Error al obtener puntuaciones: {e}")
        return []

    def cerrar(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexión cerrada.")
