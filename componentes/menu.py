import pygame
import pygame.mixer
import sqlite3

musica_activada = True

def cargar_fuente(tamano):
    return pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", tamano)

def reproducir_musica_menu():
    pygame.mixer.music.load("canciones/cancionmenu.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def detener_musica_menu():
    pygame.mixer.music.stop()

def dibujar_boton_musica(pantalla, musica_activada, boton_rect):
    icono = pygame.image.load("imgs/on.png" if musica_activada else "imgs/off.png").convert_alpha()
    icono = pygame.transform.scale(icono, (40, 40))
    pantalla.blit(icono, boton_rect.topleft)
    return boton_rect

def menu_principal(pantalla):
    global musica_activada
    fondo = pygame.image.load("imgs/background.png").convert()
    fondo = pygame.transform.scale(fondo, pantalla.get_size())

    fuente = cargar_fuente(40)
    opciones = ["Elegir Nivel", "Instrucciones", "Puntuaciones", "Salir"]
    rects_opciones = []

    boton_musica_rect = pygame.Rect(pantalla.get_width() - 50, 10, 40, 40)

    if musica_activada and not pygame.mixer.music.get_busy():
        reproducir_musica_menu()

    while True:
        pantalla.blit(fondo, (0, 0))
        rects_opciones.clear()

        for i, texto in enumerate(opciones):
            render = fuente.render(texto, True, (0, 0, 0))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 350 + i * 70))
            pantalla.blit(render, rect)
            rects_opciones.append((rect, texto))

        dibujar_boton_musica(pantalla, musica_activada, boton_musica_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_musica_rect.collidepoint(evento.pos):
                    musica_activada = not musica_activada
                    if musica_activada:
                        reproducir_musica_menu()
                    else:
                        detener_musica_menu()
                for rect, texto in rects_opciones:
                    if rect.collidepoint(evento.pos):
                        if texto == "Elegir Nivel":
                            return "elegir_nivel"
                        elif texto == "Instrucciones":
                            return "instrucciones"
                        elif texto == "Puntuaciones":
                            return "puntuaciones"
                        elif texto == "Salir":
                            pygame.quit()
                            exit()

        pygame.display.flip()

def mostrar_instrucciones(pantalla):
    fondo = pygame.image.load("imgs/background2.png").convert()
    fondo = pygame.transform.scale(fondo, pantalla.get_size())

    fuente = cargar_fuente(28)
    texto1 = fuente.render("Presiona cuando las notas lleguen a la línea", True, (0, 0, 0))
    texto2 = fuente.render("Las notas largas deben mantenerse presionadas", True, (0, 0, 0))

    teclas = ['A', 'S', 'J', 'K', 'L']
    sprites = {}
    for tecla in teclas:
        frame1 = pygame.image.load(f"imgs/{tecla}1.png").convert_alpha()
        frame2 = pygame.image.load(f"imgs/{tecla}2.png").convert_alpha()
        frame1 = pygame.transform.scale(frame1, (70, 70))
        frame2 = pygame.transform.scale(frame2, (70, 70))
        sprites[tecla] = [frame1, frame2]

    frame_actual = 0
    frame_timer = 0
    frame_interval = 400
    clock = pygame.time.Clock()

    while True:
        tiempo_pasado = clock.tick(60)
        frame_timer += tiempo_pasado

        if frame_timer >= frame_interval:
            frame_actual = (frame_actual + 1) % 2
            frame_timer = 0

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(texto1, (pantalla.get_width() // 2 - texto1.get_width() // 2, 300))
        pantalla.blit(texto2, (pantalla.get_width() // 2 - texto2.get_width() // 2, 340))

        spacing = 85
        start_x = pantalla.get_width() // 2 - (len(teclas) * spacing) // 2
        y_pos = 450
        for i, tecla in enumerate(teclas):
            sprite = sprites[tecla][frame_actual]
            pantalla.blit(sprite, (start_x + i * spacing, y_pos))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                return "menu"

        pygame.display.flip()

def mostrar_seleccion_nivel(pantalla):
    global musica_activada
    fondo = pygame.image.load("imgs/background4.png").convert()
    fondo = pygame.transform.scale(fondo, pantalla.get_size())

    fuente = cargar_fuente(40)
    opciones = ["Nivel 1", "Nivel 2", "Nivel 3", "Volver al menú"]
    rects_opciones = []

    boton_musica_rect = pygame.Rect(pantalla.get_width() - 50, 10, 40, 40)

    while True:
        pantalla.blit(fondo, (0, 0))

        rects_opciones.clear()
        for i, texto in enumerate(opciones):
            render = fuente.render(texto, True, (0, 0, 0))
            rect = render.get_rect(center=(pantalla.get_width() // 2, 350 + i * 70))
            pantalla.blit(render, rect)
            rects_opciones.append((rect, texto))

        dibujar_boton_musica(pantalla, musica_activada, boton_musica_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_musica_rect.collidepoint(evento.pos):
                    musica_activada = not musica_activada
                    if musica_activada:
                        reproducir_musica_menu()
                    else:
                        detener_musica_menu()
                for rect, texto in rects_opciones:
                    if rect.collidepoint(evento.pos):
                        detener_musica_menu()
                        if texto == "Nivel 1":
                            return "jugar_1"
                        elif texto == "Nivel 2":
                            return "jugar_2"
                        elif texto == "Nivel 3":
                            return "jugar_3"
                        elif texto == "Volver al menú":
                            return "menu"
        pygame.display.flip()

def mostrar_puntuaciones(pantalla):
    fondo = pygame.image.load("imgs/background5.png").convert()
    fondo = pygame.transform.scale(fondo, pantalla.get_size())

    efecto = pygame.mixer.Sound("canciones/efecto.wav")
    efecto.set_volume(0.25)  # Volumen reducido
    efecto.play()

    fuente_titulo = cargar_fuente(52)
    fuente_texto = cargar_fuente(26)
    titulo = fuente_titulo.render("PUNTUACIONES", True, (255, 255, 0))

    conn = sqlite3.connect("puntuaciones.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS puntuaciones (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, puntos INTEGER, combo INTEGER, aciertos INTEGER, nivel TEXT)")
    cursor.execute("SELECT nombre, puntos, combo, aciertos, nivel FROM puntuaciones ORDER BY puntos DESC LIMIT 10")
    resultados = cursor.fetchall()
    conn.close()

    clock = pygame.time.Clock()
    while True:
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 40))

        y = 140
        for i, fila in enumerate(resultados):
            nombre, puntos, combo, aciertos, nivel = fila
            texto = f"{i+1}. {nombre} - {puntos} PTS - COMBO: {combo} - ACIERTOS: {aciertos} - {nivel.upper()}"
            render = fuente_texto.render(texto, True, (255, 255, 255))
            pantalla.blit(render, (50, y))
            y += 40

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.MOUSEBUTTONDOWN:
                return "menu"

        pygame.display.flip()
        clock.tick(60)
