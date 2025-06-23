import pygame
import sys
import time
import random
import os
from configuracion import Configuracion

class Nivel:
    def __init__(self, pantalla, fuente, reloj, config):
        self.pantalla = pantalla
        self.fuente = fuente
        self.reloj = reloj
        self.config = config

        try:
            ruta_fuente = os.path.join("birdhunt", "src", "fuentes", "Minecraft.ttf")
            self.fuente = pygame.font.Font(ruta_fuente, 30)
        except:
            print("No se pudo cargar la fuente Minecraft.ttf")
            self.fuente = pygame.font.SysFont(None, 30)

    def mostrar_arma(self, estado, arma_esperando, arma_disparo, arma_retroceso):
        ancho, largo = self.config.ancho, self.config.largo
        borde_inferior = -40

        if estado == "esperando":
            arma = arma_esperando
            offset_y = 0
        elif estado == "disparo":
            arma = arma_disparo 
            offset_y = -20
        elif estado == "retroceso":
            arma = arma_retroceso
            offset_y = 10
        elif estado == "recargando":
            arma = arma_esperando
            offset_y = 0
        else:
            return

        arma_ancho = arma.get_width()
        arma_alto = arma.get_height()
        x = (ancho - arma_ancho) // 2
        y = largo - arma_alto + offset_y - borde_inferior
        self.pantalla.blit(arma, (x, y))

    def procesar_eventos(self, pajaros, sonido_disparo, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga, sonido_recarga):
        arma_estado = "esperando"
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and balas_restantes > 0 and tiempo_recarga <= 0:
                if sonido_disparo:
                    sonido_disparo.play()
                balas_restantes -= 1
                arma_estado = "disparo"
                mx, my = pygame.mouse.get_pos()
                for pajaro in pajaros:
                    if pajaro.rect.collidepoint(mx, my):
                        pajaros_destruidos += 1
                        puntuacion += 100
                        pajaro.reset_pos()

            if evento.type == pygame.MOUSEBUTTONUP:
                arma_estado = "esperando"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e and balas_restantes < 5 and tiempo_recarga <= 0:
                print("Recargando...")
                if sonido_recarga:
                    sonido_recarga.play()
                tiempo_recarga = pygame.time.get_ticks()
                arma_estado = "recargando"

        return arma_estado, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga

    def actualizar_pantalla(self, pajaros, pajaros_destruidos, balas_restantes, arma_estado,
                            arma_esperando, arma_disparo, arma_retroceso, puntuacion, tiempo_restante):
        for pajaro in pajaros:
            pajaro.mover()
            pajaro.dibujar(self.pantalla)

        blanco = Configuracion.blanco
        self.pantalla.blit(self.fuente.render(f"Pajaros derribados: {pajaros_destruidos}", True, blanco), (20, 20))
        self.pantalla.blit(self.fuente.render(f"Puntuacion: {puntuacion}", True, blanco), (20, 50))
        self.pantalla.blit(self.fuente.render(f"Balas restantes: {balas_restantes}", True, blanco), (20, 80))
        self.pantalla.blit(self.fuente.render(f"Tiempo restante: {int(tiempo_restante)}s", True, blanco), (20, 110))
        self.mostrar_arma(arma_estado, arma_esperando, arma_disparo, arma_retroceso)

    def mostrar_estadisticas_finales(self, puntuacion, pajaros_destruidos):
        try:
            fondo_final = pygame.image.load(os.path.join("birdhunt", "src", "Imgs", "instrucciones.png")).convert()
            fondo_final = pygame.transform.scale(fondo_final, (self.config.ancho, self.config.largo))
        except:
            fondo_final = pygame.Surface((self.config.ancho, self.config.largo))
            fondo_final.fill((0, 0, 0))

        self.pantalla.blit(fondo_final, (0, 0))
        centro_x = self.config.ancho // 2
        y = 200

        estadisticas = [
            f"¡Tiempo finalizado!",
            f"Puntuacion final: {puntuacion}",
            f"Pajaros derribados: {pajaros_destruidos}",
            f"Presiona ENTER para volver al menu."
        ]

        for linea in estadisticas:
            texto = self.fuente.render(linea, True, (255, 255, 255))
            rect = texto.get_rect(center=(centro_x, y))
            self.pantalla.blit(texto, rect)
            y += 50

        pygame.display.update()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    esperando = False

    def ejecutar_modo_tiempo(self, pajaros, sonido_disparo, imagen_fondo,
                             arma_esperando, arma_disparo, arma_retroceso, puntuacion_inicial):

        # Sonido de recarga
        try:
            ruta_sonido = os.path.join("birdhunt", "src", "Sonido", "recarga.mp3")
            sonido_recarga = pygame.mixer.Sound(ruta_sonido)
            sonido_recarga.set_volume(0.3)
        except:
            print("No se pudo cargar el sonido de recarga.")
            sonido_recarga = None

        if sonido_disparo:
            sonido_disparo.set_volume(0.4)

        arma_esperando = pygame.transform.smoothscale(arma_esperando, (200, 200))
        arma_disparo = pygame.transform.smoothscale(arma_disparo, (200, 200))
        arma_retroceso = pygame.transform.smoothscale(arma_retroceso, (200, 200))
        imagen_fondo = pygame.transform.scale(imagen_fondo, (self.config.ancho, self.config.largo))

        pajaros_destruidos = 0
        balas_restantes = 10
        arma_estado = "esperando"
        puntuacion = puntuacion_inicial
        tiempo_limite = 60
        tiempo_inicio = pygame.time.get_ticks()
        tiempo_recarga = 0

        for pajaro in pajaros:
            pajaro.velocidad = random.randint(2, 5)

        while True:
            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - tiempo_inicio) / 1000
            tiempo_restante = max(0, tiempo_limite - segundos_transcurridos)

            if tiempo_restante <= 0:
                self.mostrar_estadisticas_finales(puntuacion, pajaros_destruidos)
                return puntuacion

            if int(tiempo_restante) % 10 == 0:
                for pajaro in pajaros:
                    pajaro.velocidad = random.randint(3, 7)

            self.pantalla.blit(imagen_fondo, (0, 0))

            arma_estado, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga = self.procesar_eventos(
                pajaros, sonido_disparo, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga, sonido_recarga
            )

            if arma_estado == "disparo":
                self.mostrar_arma(arma_estado, arma_esperando, arma_disparo, arma_retroceso)
                pygame.display.flip()
                pygame.time.delay(80)
                self.mostrar_arma("retroceso", arma_esperando, arma_disparo, arma_retroceso)
                pygame.display.flip()
                pygame.time.delay(80)
                arma_estado = "esperando"

            self.actualizar_pantalla(
                pajaros, pajaros_destruidos, balas_restantes, arma_estado,
                arma_esperando, arma_disparo, arma_retroceso, puntuacion, tiempo_restante
            )

            if tiempo_recarga > 0 and (pygame.time.get_ticks() - tiempo_recarga) / 1000 >= 3:
                balas_restantes = 10
                tiempo_recarga = 0

            pygame.display.update()
            self.reloj.tick(self.config.fps)
