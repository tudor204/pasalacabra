import pygame as pg
import math
from datos import *

class Letra:
    def __init__(self, letra, angulo, centro, radio_circulo, radio_rosco, fuente):
        self.letra = letra
        self.angulo = angulo  
        self.centro_x, self.centro_y = centro
        self.radio_circulo = radio_circulo
        self.radio_rosco = radio_rosco
        self.fuente = fuente
        self.color_circulo = (30, 36, 157)
        self.color_texto = (255, 255, 255)
        self.pos = self.calcular_posicion()
        self.estado = "pendiente"  # pendiente, correcto, incorrecto

    def calcular_posicion(self):
        x = self.centro_x + int(self.radio_rosco * math.cos(self.angulo))
        y = self.centro_y + int(self.radio_rosco * math.sin(self.angulo))
        return (x, y)

    def dibujar(self, superficie, es_actual=False):
        if self.estado == "correcto":
            color_circulo = (0, 180, 0)  # verde
        elif es_actual:
            color_circulo = (255, 165, 0)  # naranja para la letra actual
        else:
            color_circulo = self.color_circulo

        pg.draw.circle(superficie, color_circulo, self.pos, self.radio_circulo)
        texto_render = self.fuente.render(self.letra, True, self.color_texto)
        rect = texto_render.get_rect(center=self.pos)
        superficie.blit(texto_render, rect)

class Rosco:
    def __init__(self, ancho=800, alto=600):
        pg.init()
        self.pantalla = pg.display.set_mode((ancho, alto))
        pg.display.set_caption("Pasa la Cabra")
        self.fuente_titulo = pg.font.SysFont("arial", 48, bold=True)
        self.fuente_letra = pg.font.SysFont("arial", 24, bold=True)
        self.fuente_pregunta = pg.font.SysFont("arial", 28)
        self.fuente_respuesta = pg.font.SysFont("arial", 32, bold=True)
        self.texto_titulo = self.fuente_titulo.render("¡Bienvenido a Pasa la Cabra!", True, (30, 36, 157))
        
        self.letras = letras
        self.preguntas = preguntas
        self.respuestas = respuestas
        
        self.centro = (ancho // 2, alto // 2)
        self.radio = 200
        self.radio_circulo_letra = 20

        self.letras_objetos = []
        self.crear_letras()

        

        self.letra_actual_index = 0
        self.entrada_usuario = ""
        self.feedback = ""

        self.clock = pg.time.Clock()
        self.running = True

    def crear_letras(self):
        total = len(self.letras)
        for i, letra in enumerate(self.letras):
            angulo = (2 * math.pi / total) * i - math.pi / 2
            letra_obj = Letra(letra, angulo, self.centro, self.radio_circulo_letra, self.radio, self.fuente_letra)
            self.letras_objetos.append(letra_obj)

    def siguiente_letra(self):
        total = len(self.letras)
        for i in range(1, total + 1):
            idx = (self.letra_actual_index + i) % total
            if self.letras_objetos[idx].estado == "pendiente":
                self.letra_actual_index = idx
                self.entrada_usuario = ""
                self.feedback = ""
                return
        self.feedback = "¡Has completado el rosco! Gracias por jugar."

    def pasar_letra(self):
        self.siguiente_letra()

    def validar_respuesta(self):
        letra_actual = self.letras[self.letra_actual_index]
        respuesta_correcta = self.respuestas.get(letra_actual, "").upper()
        if self.entrada_usuario.strip().upper() == respuesta_correcta:
            self.letras_objetos[self.letra_actual_index].estado = "correcto"
            self.feedback = "¡Correcto!"
        else:
            self.feedback = f"Incorrecto. La respuesta correcta es: {respuesta_correcta}"
        self.siguiente_letra()

    def dibujar(self):
        self.pantalla.fill((178, 96, 137))
        self.pantalla.blit(self.texto_titulo, (50, 30))

        for i, letra_obj in enumerate(self.letras_objetos):
            letra_obj.dibujar(self.pantalla, es_actual=(i == self.letra_actual_index))

        letra_actual = self.letras[self.letra_actual_index]
        pregunta = self.preguntas.get(letra_actual, "Sin pregunta para esta letra")
        texto_pregunta = self.fuente_pregunta.render(f"{letra_actual}: {pregunta}", True, (255, 255, 255))
        self.pantalla.blit(texto_pregunta, (50, 500))

        texto_entrada = self.fuente_respuesta.render(self.entrada_usuario, True, (255, 255, 0))
        self.pantalla.blit(texto_entrada, (50, 540))

        color_feedback = (0, 255, 0) if "Correcto" in self.feedback else (255, 0, 0)
        texto_feedback = self.fuente_pregunta.render(self.feedback, True, color_feedback)
        self.pantalla.blit(texto_feedback, (50, 580))

    def run(self):
        while self.running:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    self.running = False

                elif evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_BACKSPACE:
                        self.entrada_usuario = self.entrada_usuario[:-1]

                    elif evento.key == pg.K_RETURN:
                        self.validar_respuesta()

                    elif evento.key == pg.K_SPACE:
                        self.pasar_letra()

                    else:
                        if len(self.entrada_usuario) < 20 and evento.unicode.isprintable():
                            self.entrada_usuario += evento.unicode.upper()

            self.dibujar()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()


