import os

class Configuracion:
    blanco = (255, 255, 255)

    def __init__(self):
        self.ancho = 800
        self.largo = 600

        self.color_fondo = (0, 0, 0)
        self.color_texto = (255, 255, 255)
        self.color_boton = (0, 0, 0)
        self.color_texto_boton = (255, 0, 0)

        self.fuente_default = ""
        self.fps = 60

        self.ruta_fondo_juego = os.path.join("birdhunt", "src", "Imgs", "fondo1.png")
        self.ruta_logo_menu = os.path.join("birdhunt", "src", "Imgs", "logo.png")
