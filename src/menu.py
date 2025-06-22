import pygame
import sys
import os
from configuracion import Configuracion
from conexion import Conexion

def mostrar_menu():
    pygame.init()

    config = Configuracion()
    pantalla = pygame.display.set_mode((config.ancho, config.largo))
    pygame.display.set_caption("Hunter_Bird - Menú")

    conexion = Conexion()
    conexion.conectar()

    # Cargar imagen de fondo/logo a pantalla completa
    try:
        ruta_logo = os.path.join("Imgs", "logo.png")  # imagen completa de fondo
        fondo = pygame.image.load(ruta_logo).convert()
        fondo = pygame.transform.scale(fondo, (config.ancho, config.largo))
    except Exception as e:
        print(f"No se pudo cargar el fondo: {e}")
        fondo = pygame.Surface((config.ancho, config.largo))
        fondo.fill(config.color_fondo)

    # Fuente personalizada
    try:
        ruta_fuente = os.path.join("fuentes", "Minecraft.ttf")
        fuente = pygame.font.Font(ruta_fuente, 30)
    except:
        print("No se pudo cargar la fuente Minecraft.ttf")
        fuente = pygame.font.SysFont(None, 40)

    # Botones del menú
    botones = ["JUGAR", "INSTRUCCIONES", "SALIR", "PUNTUACIONES"]
    acciones = ["jugar", "instrucciones", "salir", "puntuaciones"]
    rects = []
    spacing = 60
    centro_x = config.ancho // 2
    inicio_y = config.largo // 2 + 20  # posición más abajo para dar aire al fondo

    for i, texto in enumerate(botones):
        t = fuente.render(texto, True, config.color_texto)
        rect = t.get_rect(center=(centro_x, inicio_y + i * spacing))
        rects.append((texto, rect, acciones[i]))

    reloj = pygame.time.Clock()

    def pedir_nombre():
        nombre = ""
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

            pantalla.blit(fondo, (0, 0))
            texto = fuente.render(f"Ingresa tu nombre: {nombre}", True, (255, 255, 255))
            pantalla.blit(texto, (input_rect.x + 10, input_rect.y + 10))
            pygame.draw.rect(pantalla, (255, 0, 0), input_rect, 2)
            pygame.display.update()
            reloj.tick(60)

        return nombre.strip()

    def mostrar_instrucciones():
        # Cargar fondo alternativo fondo2.png
        try:
            ruta_fondo2 = os.path.join("Imgs", "instrucciones.png")
            fondo_instrucciones = pygame.image.load(ruta_fondo2).convert()
            fondo_instrucciones = pygame.transform.scale(fondo_instrucciones, (config.ancho, config.largo))
        except Exception as e:
            print(f"No se pudo cargar fondo2.png: {e}")
            fondo_instrucciones = fondo  # Usa el fondo original si falla

        pantalla.blit(fondo_instrucciones, (0, 0))
        instrucciones = [
            "Dispara pajaros.",
            "Gana puntos al acertar con clic.",
            "¡Recarga con la tecla E!",
            "Presiona ENTER para volver."
        ]
        y = 250
        for linea in instrucciones:
            t = fuente.render(linea, True, config.color_texto)
            pantalla.blit(t, t.get_rect(center=(centro_x, y)))
            y += 50

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
        pantalla.blit(fondo, (0, 0))
        puntuaciones = conexion.obtener_puntuaciones()
        y = 150
        for idx, puntuacion in enumerate(puntuaciones):
            texto = fuente.render(f"{idx+1}. {puntuacion[1]} - {puntuacion[2]} puntos", True, config.color_texto)
            pantalla.blit(texto, (centro_x - texto.get_width() // 2, y))
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

    # Bucle principal
    while True:
        pantalla.blit(fondo, (0, 0))

        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        for texto, rect, accion in rects:
            color = (255, 255, 255) if rect.collidepoint(mouse_pos) else config.color_texto
            t = fuente.render(texto, True, color)
            pantalla.blit(t, t.get_rect(center=rect.center))

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for texto, rect, accion in rects:
                    if rect.collidepoint(mouse_pos):
                        if accion == "jugar":
                            return pedir_nombre()
                        elif accion == "instrucciones":
                            mostrar_instrucciones()
                        elif accion == "salir":
                            pygame.quit()
                            sys.exit()
                        elif accion == "puntuaciones":
                            mostrar_puntuaciones()

        pygame.display.update()
        reloj.tick(config.fps if hasattr(config, 'fps') else 60)
