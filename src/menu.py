import pygame
import sys
from configuracion import Configuracion
from conexion import Conexion  # Importamos la clase Conexion

def mostrar_menu():
    config = Configuracion()
    pygame.init()
    pantalla = pygame.display.set_mode((config.ancho, config.largo))
    pygame.display.set_caption("Hunter_Bird - Menú")

    # Crear una instancia de Conexion y conectarse a la base de datos
    conexion = Conexion()
    conexion.conectar()

    # Cargar fondo
    try:
        fondo = pygame.image.load(config.ruta_logo_menu).convert()
        fondo = pygame.transform.scale(fondo, (config.ancho, config.largo))
    except Exception as e:
        print(f"❌ Error al cargar fondo: {e}")
        fondo = pygame.Surface((config.ancho, config.largo))
        fondo.fill(config.color_fondo)

    # Cargar imágenes de botones
    try:
        img_jugar = pygame.image.load("Imgs/jugar.png").convert_alpha()
        img_instrucciones = pygame.image.load("Imgs/instrucciones.png").convert_alpha()
        img_salir = pygame.image.load("Imgs/salir.png").convert_alpha()
        img_puntuaciones = pygame.image.load("Imgs/puntuaciones.png").convert_alpha()  # Nuevo botón
    except Exception as e:
        print(f"Error al cargar botones: {e}")
        pygame.quit()
        sys.exit()

    spacing = 90
    centro_x = config.ancho // 2
    inicio_y = config.largo // 2 - spacing

    rect_jugar = img_jugar.get_rect(center=(centro_x, inicio_y))
    rect_instrucciones = img_instrucciones.get_rect(center=(centro_x, inicio_y + spacing))
    rect_salir = img_salir.get_rect(center=(centro_x, inicio_y + 2 * spacing))
    rect_puntuaciones = img_puntuaciones.get_rect(center=(centro_x, inicio_y + 3 * spacing))  # Nuevo botón

    reloj = pygame.time.Clock()

    def pedir_nombre():
        nombre = ""
        fuente = pygame.font.SysFont(None, 40)
        input_rect = pygame.Rect(centro_x - 200, 300, 400, 50)
        activo = True

        while activo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN and nombre.strip():
                        activo = False
                    elif e.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    elif e.unicode.isprintable():
                        nombre += e.unicode

            pantalla.fill(config.color_fondo)
            texto = fuente.render(f"Ingresá tu nombre: {nombre}", True, (255, 255, 255))
            pantalla.blit(texto, (input_rect.x + 10, input_rect.y + 10))
            pygame.draw.rect(pantalla, (255, 0, 0), input_rect, 2)
            pygame.display.update()
            reloj.tick(60)

        return nombre.strip()

    def mostrar_instrucciones():
        pantalla.blit(fondo, (0, 0))
        instrucciones = [
            "El juego consiste en derribar los pájaros que cruzan la pantalla.",
            "Ganá puntos al hacer clic sobre ellos.",
            "¡Tenés 10 disparos por ronda!",
            "Presioná ENTER para volver."
        ]
        fuente = pygame.font.SysFont(None, 32)
        y = 150
        for linea in instrucciones:
            t = fuente.render(linea, True, config.color_texto)
            pantalla.blit(t, t.get_rect(center=(config.ancho // 2, y)))
            y += 45

        pygame.display.update()
        esperando = True
        while esperando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    esperando = False

    def mostrar_puntuaciones():
        pantalla.fill(config.color_fondo)
        puntuaciones = conexion.obtener_puntuaciones()

        fuente = pygame.font.SysFont(None, 40)
        y = 150

        for idx, puntuacion in enumerate(puntuaciones):
            texto = fuente.render(f"{idx+1}. {puntuacion[1]} - {puntuacion[2]} puntos", True, config.color_texto)
            pantalla.blit(texto, (config.ancho // 2 - texto.get_width() // 2, y))
            y += 40

        pygame.display.update()
        esperando = True
        while esperando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    esperando = False

    while True:
        pantalla.blit(fondo, (0, 0))

        # Detectar si el mouse está sobre un botón
        mouse_pos = pygame.mouse.get_pos()

        def dibujar_boton(img, rect):
            if rect.collidepoint(mouse_pos):
                resaltado = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                resaltado.fill((255, 255, 255, 40))
                pantalla.blit(img, rect)
                pantalla.blit(resaltado, rect)
            else:
                pantalla.blit(img, rect)

        dibujar_boton(img_jugar, rect_jugar)
        dibujar_boton(img_instrucciones, rect_instrucciones)
        dibujar_boton(img_salir, rect_salir)
        dibujar_boton(img_puntuaciones, rect_puntuaciones)  # Mostrar el nuevo botón

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_jugar.collidepoint(mouse_pos):
                    nombre = pedir_nombre()
                    return nombre
                elif rect_instrucciones.collidepoint(mouse_pos):
                    mostrar_instrucciones()
                elif rect_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif rect_puntuaciones.collidepoint(mouse_pos):  # Mostrar puntuaciones
                    mostrar_puntuaciones()

        pygame.display.update()
        reloj.tick(config.fps if hasattr(config, 'fps') else 60)
