import math
import time
import rps_module
import strat_module
import csv

file_csv = "salvatest.csv"


def crea_csv():
    # Nomi delle colonne
    # nomi_colonne = ["Num_partite", "Init", "Move_R", "Move_G", "Move_B", "Velocità", "Num_pallini", "Raggio_pallini",
    #                 "EsitoR", "EsitoG", "EsitoB", "Tempo"]

    # Percorso al nuovo file CSV
    percorso_file = "salvatest.csv"

    # Apri il nuovo file CSV in modalità write ("w") e scrivi i nomi delle colonne
    with open(percorso_file, mode="w", newline="") as file:
        writer = csv.writer(file)


def test(num, init, moveR, moveG, moveB, vel, dim, r, **kwargs):
    lista_risultati = [0, 0, 0]
    start = time.process_time()
    for _ in range(num):
        G = rps_module.Game(mr=moveR, mg=moveG, mb=moveB, vel=vel, d=dim, r=r, init=init, **kwargs)
        esito = G.start_simulation()
        if esito == 'R':
            lista_risultati[0] += 1
        if esito == 'G':
            lista_risultati[1] += 1
        if esito == 'B':
            lista_risultati[2] += 1
    print(time.process_time() - start, "seconds")
    # Apri il file CSV in modalità append ("a") e scrivi la nuova riga
    with open(file_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        riga = {'NumPartite': num, 'PosizInit': init.__name__, 'MoveR': moveR.__name__, 'MoveG': moveG.__name__,
                'MoveB': moveB.__name__, 'vel': vel, 'NumPalline': dim, 'RaggioPallina': r, **kwargs}
        fieldnames = riga.keys()
        csv_writer = csv.DictWriter(riga, fieldnames=fieldnames)
        csv_writer.writerow(riga)

    return lista_risultati


def prova(init, moveR, moveG, moveB, vel, dim, r, **kwargs):
    G = rps_module.Game(mr=moveR, mg=moveG, mb=moveB, vel=vel, d=dim, r=r, init=init, **kwargs)
    G.start_animation()


for r_t in [0.9, 0.7, 0.5, 0.3, 0.1]:
    print(test(num=10, init=strat_module.init_triang, moveR=strat_module.move_random,
               moveG=strat_module.move_random, moveB=strat_module.move_random, vel=10, dim=10, r=5,
               r_t=r_t, sfas=math.pi / 3))
