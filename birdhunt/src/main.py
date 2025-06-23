import pygame
import sys
import os

# Ajustar el path para importar desde birdhunt
sys.path.append(os.path.join(os.path.dirname(__file__), 'birdhunt', 'src'))

from configuracion import Configuracion
from Bird import Bird
from menu import mostrar_menu
from nivel import Nivel
from conexion import Conexion  # Clase para manejar base de datos

def main():
    pygame.init()
    pygame.mixer.init()

    config = Configuracion()
    pantalla = pygame.display.set_mode((config.ancho, config.largo))
    pygame.display.set_caption("Hunter_Bird")

    # Música de fondo (loop)
    try:
        ruta_musica = os.path.join("birdhunt", "src", "Sonido", "tema.mp3")
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error al cargar música de fondo: {e}")

    # Conectarse a la base de datos
    conexion = Conexion()
    conexion.conectar()

    while True:
        nombre_jugador = mostrar_menu()

        fuente = pygame.font.SysFont(config.fuente_default, 40)
        reloj = pygame.time.Clock()

        # Fondo
        try:
            fondo = pygame.image.load(config.ruta_fondo_juego).convert()
            fondo = pygame.transform.scale(fondo, (config.ancho, config.largo))
        except Exception as e:
            print(f"Error al cargar fondo: {e}")
            fondo = pygame.Surface((config.ancho, config.largo))
            fondo.fill(config.color_fondo)

        # Sonido
        try:
            ruta_disparo = os.path.join("birdhunt", "src", "Sonido", "doom-shotgun.mp3")
            disparo_sonido = pygame.mixer.Sound(ruta_disparo)
            disparo_sonido.set_volume(0.4)
        except Exception as e:
            print(f"Error al cargar sonido de disparo: {e}")
            disparo_sonido = None

        # Armas
        try:
            arma_idle = pygame.image.load(os.path.join("birdhunt", "src", "Imgs", "arma0.png")).convert_alpha()
            arma_disparo = pygame.image.load(os.path.join("birdhunt", "src", "Imgs", "arma2.png")).convert_alpha()
            arma_retroceso = pygame.image.load(os.path.join("birdhunt", "src", "Imgs", "arma3.png")).convert_alpha()
        except Exception as e:
            print(f"Error al cargar imágenes de arma: {e}")
            pygame.quit()
            sys.exit()

        # Pájaros
        pajaros = [Bird() for _ in range(7)]

        # Ejecutar modo tiempo (sin selección de nivel)
        nivel = Nivel(pantalla, fuente, reloj, config)
        resultado = nivel.ejecutar_modo_tiempo(
            pajaros=pajaros,
            sonido_disparo=disparo_sonido,
            imagen_fondo=fondo,
            arma_esperando=arma_idle,
            arma_disparo=arma_disparo,
            arma_retroceso=arma_retroceso,
            puntuacion_inicial=0
        )

        if isinstance(resultado, int):
            print(f"{nombre_jugador} obtuvo una puntuación final de: {resultado}")
            conexion.guardar_puntaje(nombre_jugador, resultado)
        continue  # volver al menú para jugar de nuevo

if __name__ == "__main__":
    main()
