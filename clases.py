import pygame as pg
import math

class Letra:
    def __init__(self, letra, angulo, centro, radio_circulo, radio_rosco, fuente):
        self.letra = letra
        self.angulo = angulo  # en radianes
        self.centro_x, self.centro_y = centro
        self.radio_circulo = radio_circulo
        self.radio_rosco = radio_rosco
        self.fuente = fuente
        self.color_circulo = (30, 36, 157)
        self.color_texto = (255, 255, 255)
        self.pos = self.calcular_posicion()
        

    def calcular_posicion(self):
        x = self.centro_x + int(self.radio_rosco * math.cos(self.angulo))
        y = self.centro_y + int(self.radio_rosco * math.sin(self.angulo))
        return (x, y)

    def dibujar(self, superficie):
        # Dibujar círculo
        pg.draw.circle(superficie, self.color_circulo, self.pos, self.radio_circulo)
        # Dibujar letra centrada
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
        self.texto_titulo = self.fuente_titulo.render("¡Bienvenido a Pasa la Cabra!", True, (30, 36, 157))

        self.letras = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]
        self.centro = (ancho // 2, alto // 2)
        self.radio = 200
        self.radio_circulo_letra = 20

        self.letras_objetos = []
        self.crear_letras()

        self.clock = pg.time.Clock()
        self.running = True

    def crear_letras(self):
        total = len(self.letras)
        for i, letra in enumerate(self.letras):
            # Empezamos desde la parte superior (ángulo -pi/2)
            angulo = (2 * math.pi / total) * i - math.pi / 2
            letra_obj = Letra(letra, angulo, self.centro, self.radio_circulo_letra, self.radio, self.fuente_letra)
            self.letras_objetos.append(letra_obj)

    def dibujar(self):
        self.pantalla.fill((178, 96, 137))
        self.pantalla.blit(self.texto_titulo, (50, 30))
        for letra_obj in self.letras_objetos:
            letra_obj.dibujar(self.pantalla)

    def run(self):
        while self.running:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    self.running = False

            self.dibujar()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()

