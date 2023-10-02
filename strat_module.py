import pygame
import random
import math
import rps_module

"""
Questo modulo contiene le funzione per le strategie:
-funzioni di inizializzazione, servono per inizializzare la posizione di tutti i pallini:
    -hanno come nome init_{nome}
    -prendono in input un oggetto di tipo rps_module.Game
    -restituiscono tre liste con cui vengono inizializzati lista_r, lista_g, lista_b della
    classe rps_module.Game
-funzioni per le mosse, servono per scegliere come muovere i pallini:
    -hanno come nome move_{nome}
    -prende in input un oggetto di tipo rps_module.Game e una variabile tipo (carattere minuscolo)
    -restituisce una lista di angoli in radianti che rappresentano delle direzioni
"""


# data l'intera situazione del "oggetto_game" devi restituire un lista di angoli
# che rappresentano le mosse di "tipo"
def move_random(oggetto_game, tipo):
    l = []
    if tipo == "r":
        l = oggetto_game.list_r
    if tipo == "g":
        l = oggetto_game.list_g
    if tipo == "b":
        l = oggetto_game.list_b
    ...
    return [random.uniform(0, 2 * math.pi) for _ in l]


def init_triang(oggetto_game, **kwargs):

    # raggio del cerchio grande
    R = oggetto_game.width / 2
    # raggio della circonferenza circoscritta nel triangolo
    raggio_tr = kwargs['r_t'] * R
    # sfasamento
    sfas = kwargs['sfas']

    return [rps_module.Circle(R + raggio_tr * math.cos(sfas), R - raggio_tr * math.sin(sfas), oggetto_game.r, rps_module.RED) for i
            in range(oggetto_game.dim)], \
           [rps_module.Circle(R + raggio_tr * math.cos(sfas + 2 * math.pi / 3), R - raggio_tr * math.sin(sfas + 2 * math.pi / 3),
                              oggetto_game.r, rps_module.YEL) for i in range(oggetto_game.dim)], \
           [rps_module.Circle(R + raggio_tr * math.cos(sfas + 4 * math.pi / 3), R - raggio_tr * math.sin(sfas + 4 * math.pi / 3),
                              oggetto_game.r, rps_module.BLUE) for i in range(oggetto_game.dim)]
