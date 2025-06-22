class Configuracion:
    # Parámetros del juego
    blanco = (255, 255, 255)

    def __init__(self):
        # Definir los parámetros básicos del juego
        self.ancho = 800
        self.largo = 600

        # Colores
        self.color_fondo = (0, 0, 0)  # Fondo negro
        self.color_texto = (255, 255, 255)  # Blanco
        self.color_boton = (0, 0, 0)  # Color del botón
        self.color_texto_boton = (255, 0, 0)  # Color del texto del botón

        # Fuente y FPS
        self.fuente_default = ""
        self.fps = 60

        # Rutas
        self.ruta_fondo_juego = "Imgs/fondo1.png"  # Cambia esto con la ruta de tu fondo
        self.ruta_logo_menu = "Imgs/logo.png"  # Cambia esto con la ruta del logo
