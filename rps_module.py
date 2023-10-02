import pygame
import math

"""
Questo modulo contiene tutto il codice per eseguire delle partite
"""


# distanza
def dist(xA, yA, xB, yB):
    return ((xA - xB) ** 2 + (yA - yB) ** 2) ** 0.5


# colori
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YEL = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


# prende in input le coordinate rispetto al centro del cerchio e restituisce le nuove coordinate
# serve per sistemare quando arrivano al bordo
def sistema_pos(x, y, R):
    if x == 0:
        if y >= 0:
            ang = math.pi / 2
        else:
            ang = -math.pi / 2
    else:
        ang = math.atan(y / x)
    if x < 0:
        ang += math.pi
    # print(f"Angolo: {180 * ang / math.pi}")
    return R * math.cos(ang), R * math.sin(ang)


# classe cerchio
class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.radius = r
        self.color = color
        # self.speed = 1

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Game:
    def __init__(self, mr, mg, init, mb, vel, width=800, d=10, r=5, **kwargs):
        self.width = width # lato della finestra quadrata
        self.dim = d # numero di pallini per ogni squadra
        self.r = r # raggio dei pallini
        self.list_r, self.list_g, self.list_b = init(self, **kwargs) # liste contenenti gli angoli
        self.move_r = mr  # funzione per muovere, si trovano in strat_module
        self.move_g = mg
        self.move_b = mb
        self.vel = vel
        self.clock = 0
        self.window = 0

    def start_animation(self, fps=20):
        # funzione per fare l'animazione grafica di una partita
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("Moving Circle")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # muovi
            movements_r = self.move_r(self, "r")
            movements_g = self.move_g(self, "g")
            movements_b = self.move_b(self, "b")

            for i in range(len(self.list_r)):
                self.list_r[i].move(self.vel * math.cos(movements_r[i]), self.vel * math.sin(movements_r[i]))
            for i in range(len(self.list_g)):
                self.list_g[i].move(self.vel * math.cos(movements_g[i]), self.vel * math.sin(movements_g[i]))
            for i in range(len(self.list_b)):
                self.list_b[i].move(self.vel * math.cos(movements_b[i]), self.vel * math.sin(movements_b[i]))
            # controlla
            # contr se qualcuno ha vinto
            if len(self.list_r) == 0:
                print("Ha vinto il verde")
                return "G"
            if len(self.list_g) == 0:
                print("Ha vinto il blu")
                return "B"
            if len(self.list_b) == 0:
                print("Ha vinto il rosso")
                return "R"
            # controlla margini
            R = self.width / 2
            for circle in self.list_r + self.list_g + self.list_b:
                if dist(circle.x, circle.y, R, R) >= R:
                    X, Y = sistema_pos(circle.x - R, R - circle.y, R)
                    # (X, Y) è la nuova posizione in coordinate rispetto al centro
                    circle.x = X + R
                    circle.y = R - Y
            # controlla i contatti r-g
            for circle_r in self.list_r:
                for circle_g in self.list_g:
                    if dist(circle_r.x, circle_r.y, circle_g.x, circle_g.y) <= 2 * self.r:
                        circle_g.color = RED
                        self.list_r.append(self.list_g.pop(self.list_g.index(circle_g)))
            # controlla i contatti g-b
            for circle_g in self.list_g:
                for circle_b in self.list_b:
                    if dist(circle_g.x, circle_g.y, circle_b.x, circle_b.y) <= 2 * self.r:
                        circle_b.color = YEL
                        self.list_g.append(self.list_b.pop(self.list_b.index(circle_b)))
            # controlla i contatti b-r
            for circle_b in self.list_b:
                for circle_r in self.list_r:
                    if dist(circle_b.x, circle_b.y, circle_r.x, circle_r.y) <= 2 * self.r:
                        circle_r.color = BLUE
                        self.list_b.append(self.list_r.pop(self.list_r.index(circle_r)))

            # disegna
            self.window.fill(BLACK)
            pygame.draw.circle(self.window, WHITE, (self.width / 2, self.width / 2),
                               self.width / 2, 0)

            for circle in self.list_r:
                circle.draw(self.window)
            for circle in self.list_g:
                circle.draw(self.window)
            for circle in self.list_b:
                circle.draw(self.window)
            pygame.display.update()
            self.clock.tick(fps)

        pygame.quit()

    def start_simulation(self):
        # funzione per fare la simulazione, restituisce l'esito attraverso un carattere Maiuscolo
        running = True
        while running:
            # controlli
            # controlla se qualcuno ha vinto
            if len(self.list_r) == 0:
                # print("Ha vinto il verde")
                return "G"
            if len(self.list_g) == 0:
                # print("Ha vinto il blu")
                return "B"
            if len(self.list_b) == 0:
                # print("Ha vinto il rosso")
                return "R"
            # controlla margini
            R = self.width / 2
            for circle in self.list_r + self.list_g + self.list_b:
                if dist(circle.x, circle.y, R, R) >= R:
                    X, Y = sistema_pos(circle.x - R, R - circle.y, R)
                    # (X, Y) è la nuova posizione in coordinate rispetto al centro
                    circle.x = X + R
                    circle.y = R - Y
            # controlla i contatti r-g
            for circle_r in self.list_r:
                for circle_g in self.list_g:
                    if dist(circle_r.x, circle_r.y, circle_g.x, circle_g.y) <= 2 * self.r:
                        circle_g.color = RED
                        self.list_r.append(self.list_g.pop(self.list_g.index(circle_g)))
            # controlla i contatti g-b
            for circle_g in self.list_g:
                for circle_b in self.list_b:
                    if dist(circle_g.x, circle_g.y, circle_b.x, circle_b.y) <= 2 * self.r:
                        circle_b.color = YEL
                        self.list_g.append(self.list_b.pop(self.list_b.index(circle_b)))
            # controlla i contatti b-r
            for circle_b in self.list_b:
                for circle_r in self.list_r:
                    if dist(circle_b.x, circle_b.y, circle_r.x, circle_r.y) <= 2 * self.r:
                        circle_r.color = BLUE
                        self.list_b.append(self.list_r.pop(self.list_r.index(circle_r)))

            # muovi
            movements_r = self.move_r(self, "r")
            movements_g = self.move_g(self, "g")
            movements_b = self.move_b(self, "b")

            for i in range(len(self.list_r)):
                self.list_r[i].move(self.vel * math.cos(movements_r[i]), self.vel * math.sin(movements_r[i]))
            for i in range(len(self.list_g)):
                self.list_g[i].move(self.vel * math.cos(movements_g[i]), self.vel * math.sin(movements_g[i]))
            for i in range(len(self.list_b)):
                self.list_b[i].move(self.vel * math.cos(movements_b[i]), self.vel * math.sin(movements_b[i]))
