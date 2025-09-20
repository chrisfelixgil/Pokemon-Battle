#Importaciones de módulos
import time
import os
from random import randint
import readchar

#Variables definidas
nombre_del_jugador = ''
nombre_del_enemigo = ''

#Constantes definidas
POSICION_X = 0
POSICION_Y = 1
ANCHO_MAPA = 46
ALTO_MAPA = 20
ANCHO_MAPA_LAB = 49
ALTO_MAPA_LAB = 15
VIDA_INICIAL_PIKACHU = 80
VIDA_INICIAL_SQUARTLE = 90

vida_pikachu = VIDA_INICIAL_PIKACHU
vida_squartle = VIDA_INICIAL_SQUARTLE

TAMANIO_BARRA_VIDA = 10

#Ataques de Pikachu
BOLA_VOLTIO = 10
ONDA_TRUENO = 11

#Ataques de Squirtle
PLACAJE = 10
PISTOLA_AGUA = 12
BURBUJAS = 9

#Vectores
mi_posicion = [12,9]
mi_posicion_lab = [20,8]
mi_posicion_villano = [34,17]
objetos_del_lab = [[27,11], [30,11], [33,11]]
obstaculos_a_dibujar = ['#', '_', 'R', '|', '-', '[', ']']
obstaculos_a_dibujar_villano = ['#', '_', 'R', '|', '-', '[', ']']
objetos_del_mapa = [[21,0], [22,0], [23,0], [24,0], [25,0], [21,1], [22,1], [23,1], [24,1], [25,1], [21,2], [22,2], [23,2], [24,2], [25,2], [21,3], [22,3], [23,3], [24,3], [25,3], [21,4], [22,4], [23,4], [24,4], [25,4]]
objetos_del_mapa_villano = [[21,0], [22,0], [23,0], [24,0], [25,0], [21,1], [22,1], [23,1], [24,1], [25,1], [21,2], [22,2], [23,2], [24,2], [25,2], [21,3], [22,3], [23,3], [24,3], [25,3], [21,4], [22,4], [23,4], [24,4], [25,4]]
obstaculos_a_dibujar_lab = ['#', '_', '|', '-', '[', ']', '@', 'O', 'K', 'A', 'L', 'B', 'R', 'T', 'I', '*', '.']
obstaculos_no_atravesar_lab = ['|', '-', '*', 'O', 'K', 'A', '_']

#Booleanos
tocar_objeto = False
tocar_objeto_lab = False
tocar_objeto_villano = False

#Mapas a dibujar
obstaculos_en_mapa = """\
#####################     ####################
#####################     ####################
#####################     ####################
#####################     ####################
#####################     ####################
#         ________           ___________     #
#        |--------|         |-----------|    #
#        | [_][_] |         | [__] _[_] |    #
#        |_| |____|         |_____| |___|    #
#                                            #
#                                            #
#                         _____________      #
#                        |             |     #
#                        |_ _ _ _ _ _ _|     #
#                        |[][][] [][][]|     #
#                        | - - - - - - |     #
#                        |_RRRR_| |_RRR|     #
#                                            #
#                                            #
##############################################\
"""

obstaculos_en_mapa_villano = """\
#####################     ####################
#####################     ####################
#####################     ####################
#####################     ####################
#####################     ####################
#         ________           ___________     #
#        |--------|         |-----------|    #
#        | [_][_] |         | [__] _[_] |    #
#        |_| |____|         |_____| |___|    #
#                                            #
#                                            #
#                         _____________      #
#                        |             |     #
#                        |_ _ _ _ _ _ _|     #
#                        |[][][] [][][]|     #
#                        | - - - - - - |     #
#                        |_RRRR_| |_RRR|     #
#                                            #
#                                            #
##############################################\
"""

obstaculos_en_lab = """\
#################################################
##########     L A B O R A T O R I O   ##########
##########@---------------------------@##########
##########|[___][____]       |--|--|--|##########
##########|                  |__|__|__|##########
##########|             OKA           |##########
##########|                           |##########
##########|                           |##########
##########|             *             |##########
##########|                           |##########
##########|              |.........|  |##########
##########|              |         |  |##########
##########|              |.........|  |##########
##########|                           |##########
##########@---------------------------@##########\
"""

#Funciones
#Funcion para esperar la pantalla
def esperar_pantalla():
    time.sleep(2)
    os.system('cls')

#Funcion para presionar Enter y limpiar pantalla
def enter_y_limpia_pantalla():
    input('')
    os.system('cls')

#Funcion para cargar pantalla inicial
def pantalla_de_carga():
    carga = 0
    for i in range(0, 105, 5):
        print(f'CARGANDO... {carga}%')
        carga = carga + 5
        time.sleep(0.2)
        os.system('cls')
    return carga

"""
#Página incial
print('''
                        ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
                        ▐ ██████   ██████  ██   ██ ███████ ███    ███  ██████  ███    ██ ▌
                        ▐ ██   ██ ██    ██ ██  ██  ██      ████  ████ ██    ██ ████   ██ ▌
                        ▐ ██████  ██    ██ █████   █████   ██ ████ ██ ██    ██ ██ ██  ██ ▌
                        ▐ ██      ██    ██ ██  ██  ██      ██  ██  ██ ██    ██ ██  ██ ██ ▌
                        ▐ ██       ██████  ██   ██ ███████ ██      ██  ██████  ██   ████ ▌
                        ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌                                                         
''')
enter_y_limpia_pantalla()

#Página incial 2
print('''                                                       
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠖⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡤⢤⡀⠀⠀⠀⠀⢸⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡀⠈⠢⡀⠀⠀⢀⠀⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⡔⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠊⡹⠀⠀⠘⢄⠀⠈⠲⢖⠈⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠙⣄⠈⠢⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠖⠁⢠⠞⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠈⡆⠀⠀⠉⠑⠢⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⡠⠚⠁⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⠇⠀⡤⡀⠀⠀⠀⢀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢠⣾⣿⣷⣶⣤⣄⣉⠑⣄⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⢀⠞⢁⣴⣾⣿⣿⡆⢇⠀⠀⠀⠀⠀⠸⡀⠀⠂⠿⢦⡰⠀⠀⠋⡄⠀⠀⠀⠀⠀⠀⠀⢰⠁⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⢆⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⡴⢁⣴⣿⣿⣿⣿⣿⣿⡘⡄⠀⠀⠀⠀⠀⠱⣔⠤⡀⠀⠀⠀⠀⠀⠈⡆⠀⠀⠀⠀⠀⠀⡜⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⢣⠀⠀⠀⠀⠀
            ⠀⠀⠀⡼⢠⣾⣿⣿⣿⣿⣿⣿⣿⣧⡘⢆⠀⠀⠀⠀⠀⢃⠑⢌⣦⠀⠩⠉⠀⡜⠀⠀⠀⠀⠀⠀⢠⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣣⡀⠀⠀⠀
            ⠀⠀⢰⢃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠱⡀⠀⠀⠀⢸⠀⠀⠓⠭⡭⠙⠋⠀⠀⠀⠀⠀⠀⠀⡜⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡱⡄⠀⠀
            ⠀⠀⡏⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢃⠀⠀⠀⢸⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⢀⠜⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣆⠀
            ⠀⢸⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡘⣆⠀⠀⡆⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⡠⠖⣡⣾⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⠀
            ⠀⡏⣾⣿⣿⣿⣿⡿⡛⢟⢿⣿⣿⣿⣿⣿⣿⣧⡈⢦⣠⠃⠀⠀⠀⠀⠀⢱⣀⠤⠒⢉⣾⡉⠻⠋⠈⢘⢿⣿⣿⣿⣿⠿⣿⣿⠏⠉⠻⢿⣿⣿⣿⣿⡘⡆
            ⢰⡇⣿⣿⠟⠁⢸⣠⠂⡄⣃⠜⣿⣿⠿⠿⣿⣿⡿⠦⡎⠀⠀⠀⠀⠀⠒⠉⠉⠑⣴⣿⣿⣎⠁⠠⠂⠮⢔⣿⡿⠉⠁⠀⠹⡛⢀⣀⡠⠀⠙⢿⣿⣿⡇⡇
            ⠘⡇⠏⠀⠀⠀⡾⠤⡀⠑⠒⠈⠣⣀⣀⡀⠤⠋⢀⡜⣀⣠⣤⣀⠀⠀⠀⠀⠀⠀⠙⢿⡟⠉⡃⠈⢀⠴⣿⣿⣀⡀⠀⠀⠀⠈⡈⠊⠀⠀⠀⠀⠙⢿⡇⡇
            ⠀⠿⠀⠀⠀⠀⠈⠀⠉⠙⠓⢤⣀⠀⠁⣀⡠⢔⡿⠊⠀⠀⠀⠀⠙⢦⡀⠀⠐⠢⢄⡀⠁⡲⠃⠀⡜⠀⠹⠟⠻⣿⣰⡐⣄⠎⠀⠀⠀⠀⠀⠀⠀⠀⢣⡇
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠀⠀⠙⢦⣀⢀⡴⠁⠀⠀⠀⠀⠉⠁⢱⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠈⢏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠱⡄⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠁⠀⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⢀⡴⠁⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠀⠘⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⣧⣠⠤⠖⠋⠀⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀⠳⢄⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠊⠈⠁⠀⠀⠀⡔⠛⠲⣤⣀⣀⣀⠀⠈⢣⡀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⢀⡠⢔⠝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢈⠤⠒⣀⠀⠀⠀⠀⣀⠟⠀⠀⠀⠑⠢⢄⡀⠀⠀⠈⡗⠂⠀⠀⠀⠙⢦⠤⠒⢊⡡⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠒⣒⡁⠬⠦⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠒⢺⢠⠤⡀⢀⠤⡀⠠⠷⡊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠣⡀⡱⠧⡀⢰⠓⠤⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ''')
esperar_pantalla()

#Página incial 3
print('''    
                                @-----------------------------------------------@
                                |                                               |
                                |  ©2024 ITLA                                   |
                                |                                               |
                                |         Fundamentos de Programación           |
                                |              Prof. Wilmer Fariña              |                     
                                |                                               |
                                |          Autores:                             |
                                |               Lesley Peguero 2023-1234        |
                                |               Christian Gil 2012-1036         |
                                @-----------------------------------------------@
''')
esperar_pantalla()

#Funcion para gargar la pantalla inicial
pantalla_de_carga()

print('''
      ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠉⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣴⣶⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⢤
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠋⠀⠐⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠖⢉⣿⣿⣿⠟⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⡼
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡼⠀⠀⠈⢆⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠊⠁⠀⠀⢸⣿⡿⠃⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠊⠁⠀⠀⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠞⠁⠀⠀⠀⠀⠀⣾⠟⠡⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⡏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠄⢼⠀⠀⢀⣀⣤⠤⠤⠤⣤⣀⣀⡤⠋⠀⠀⠀⠀⠀⠀⢀⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⢀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠟⠚⠉⠁⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠍⣀⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⡠⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠶⢷⡀⠀⠀⠀⠀⠀⠀⢀⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⣸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡹⣦⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠔⠚⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⠃⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠚⠀⠀⠀⠀⠀⠀⠀⠈⠁⠞⡹⢾⣧⣠⣠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠔⠋⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣴⠮⡍⡏⠀⣿⣽⡄⠀⠀⠀⠀⢀⠀⣠⢶⣿⣿⣧⠀⠀⢠⠞⠀⠀⢠⡏⣳⣯⠚⠉⠯⢽⣷⢤⡀⠀⠀⠀⠀⠀⢠⠴⠚⠁⠀⠃⠀⠀⠀⠀⠀⠀⠀
⢸⡉⢆⣀⡏⡰⣦⣇⡟⣦⠹⠿⠿⠀⠀⠀⠀⠘⠞⠹⢾⣿⣿⢟⣠⣒⣿⠿⣭⣲⣼⡿⠘⠞⠠⠀⠁⠀⢳⡄⠉⠳⢦⡀⠀⠀⠈⠳⢆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠢⠇⣴⣆⣺⡵⢹⣿⣉⢿⣇⠀⠀⠀⠦⠀⠀⠀⠀⠀⠀⠀⢇⠀⣇⠈⠿⠒⢯⠀⠻⣃⠇⠀⠀⠀⠀⠀⣜⣿⡄⠀⠀⠈⠓⢦⡀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠸⣑⢫⡵⠀⠈⠈⠳⣟⠀⠀⠙⠒⠒⠢⠤⠞⠁⠀⠀⠈⠀⠙⠣⠽⠶⠋⠀⠀⠚⠋⠀⠀⠀⠀⣼⣿⣿⣷⡀⠀⠀⢀⠜⠁⠀⠀⠀⠀⣹⠆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⢪⠳⠀⠀⠀⠀⢈⠟⠂⣢⣄⡀⠀⠀⠀⠀⠀⠀⣀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠁⠀⢣⢠⡴⠋⠀⠀⠀⣠⠔⠋⡄⠐⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢏⡴⠋⠁⠹⠷⣆⠀⠀⠀⢰⠏⠇⠈⠙⠲⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡏⠀⠀⣠⠖⠋⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠁⢀⠀⡹⠄⠀⠀⢸⡄⠈⠒⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣀⠀⠈⠷⠦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣀⠀⠀⣨⡷⢻⠀⠀⠀⠀⠹⣆⠀⠀⠀⠀⠀⠀⣀⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡏⣉⣾⣳⣬⣺⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢩⠟⣇⠀⠁⠀⠀⠀⠀⠀⠈⠑⠢⠤⠤⠔⢊⠵⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⠟⠋⢁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⠸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⡄⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠈⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣗⡢⠤⠄⣈⣙⣲⣤⣀⡀⠀⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣲⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⠏⣨⠎⣳⠤⠚⠉⠀⠀⠀⠉⠙⠓⠒⠒⠒⡒⠛⠲⢤⣀⣀⣀⣀⠤⠤⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠙⠉⠀⡄⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣓⡍⠉⡒⡾⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠑⠋⠙⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')
input('Presiona la tecla Enter para sumergirte al fascinante mundo Pokémon...')
os.system('cls')

print('''
@-----------------------------------------------@
|                                               |
|  En el mundo al que estás a punto de entrar,  |
|  te embarcarás en una gran aventura tú como   |
|  el héroe.                                    |
|                                               |
|  Habla con las personas y revisa cosas        |
|  dondequiera que vayas, ya sea en ciudades,   |
|  caminos o cuevas. Recopila información y     |
|  pistas de todas las fuentes.                 |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
@-----------------------------------------------@
|                                               |
|  Se te abrirán nuevos caminos ayudando a      |
|  las personas necesitadas, superando          |
|  desafíos y resolviendo misterios.            |
|                                               |
|  A veces, serás desafiado por otros y         |
|  atacado por criaturas salvajes. Sé valiente  |
|  y sigue adelante.                            |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
@-----------------------------------------------@
|                                               |
|  A través de tu aventura, esperamos que       |
|  interactúes con todo tipo de personas y      |
|  logres crecimiento personal.                 |
|  Ese es nuestro mayor objetivo.               |
|                                               |
| ¡Presiona ENTER, y que comience tu aventura!  |
|                                               |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|      ¡Hola! ¡Encantado de conocerte!          |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|     ¡Bienvenido al mundo de Pokémon!          |
|           Mi nombre es OAK.                   |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|        La gente me llama cariñosamente        |
|            el Profesor Pokémon.               |
|                                            ↓  |
@-----------------------------------------------@ 
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|               Este mundo…                     |
|                                            ↓  |
@-----------------------------------------------@ 
''')
enter_y_limpia_pantalla()

print('''
		⠀⠀⠀⠀⠀⢸⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠙⢤⡷⣤⣦⣀⠤⠖⠚⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⣠⡿⠢⢄⡀⠀⡇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠸⠷⣶⠂⠀⠀⠀⣀⣀⠀⠀⠀
		⢸⣃⠀⠀⠉⠳⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⢉⡭⠋
		⠀⠘⣆⠀⠀⠀⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀
		⠀⠀⠘⣦⠆⠀⠀⢀⡎⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⣠⠔⠋⠀⠀⠀⠀
		⠀⠀⠀⡏⠀⠀⣆⠘⣄⠸⢧⠀⠀⠀⠀⢀⣠⠖⢻⠀⠀⠀⣿⢥⣄⣀⣀⣀⠀⠀
		⠀⠀⢸⠁⠀⠀⡏⢣⣌⠙⠚⠀⠀⠠⣖⡛⠀⣠⠏⠀⠀⠀⠇⠀⠀⠀⠀⢙⣣⠄
		⠀⠀⢸⡀⠀⠀⠳⡞⠈⢻⠶⠤⣄⣀⣈⣉⣉⣡⡔⠀⠀⢀⠀⠀⣀⡤⠖⠚⠀⠀
		⠀⠀⡼⣇⠀⠀⠀⠙⠦⣞⡀⠀⢀⡏⠀⢸⣣⠞⠀⠀⠀⡼⠚⠋⠁⠀⠀⠀⠀⠀
		⠀⢰⡇⠙⠀⠀⠀⠀⠀⠀⠉⠙⠚⠒⠚⠉⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⢧⡀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠙⣶⣶⣿⠢⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠉⠀⠀⠀⠙⢿⣳⠞⠳⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠹⣄⣀⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    

@-----------------------------------------------@
|                                               |
| está habitado por criaturas llamadas Pokémon. |
|                                               |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
		⠀⠀⠀⠀⠀⢸⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠙⢤⡷⣤⣦⣀⠤⠖⠚⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⣠⡿⠢⢄⡀⠀⡇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠸⠷⣶⠂⠀⠀⠀⣀⣀⠀⠀⠀
		⢸⣃⠀⠀⠉⠳⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⢉⡭⠋
		⠀⠘⣆⠀⠀⠀⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀
		⠀⠀⠘⣦⠆⠀⠀⢀⡎⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⣠⠔⠋⠀⠀⠀⠀
		⠀⠀⠀⡏⠀⠀⣆⠘⣄⠸⢧⠀⠀⠀⠀⢀⣠⠖⢻⠀⠀⠀⣿⢥⣄⣀⣀⣀⠀⠀
		⠀⠀⢸⠁⠀⠀⡏⢣⣌⠙⠚⠀⠀⠠⣖⡛⠀⣠⠏⠀⠀⠀⠇⠀⠀⠀⠀⢙⣣⠄
		⠀⠀⢸⡀⠀⠀⠳⡞⠈⢻⠶⠤⣄⣀⣈⣉⣉⣡⡔⠀⠀⢀⠀⠀⣀⡤⠖⠚⠀⠀
		⠀⠀⡼⣇⠀⠀⠀⠙⠦⣞⡀⠀⢀⡏⠀⢸⣣⠞⠀⠀⠀⡼⠚⠋⠁⠀⠀⠀⠀⠀
		⠀⢰⡇⠙⠀⠀⠀⠀⠀⠀⠉⠙⠚⠒⠚⠉⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⢧⡀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠙⣶⣶⣿⠢⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠉⠀⠀⠀⠙⢿⣳⠞⠳⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠹⣄⣀⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

@-----------------------------------------------@
|                                               |
|  Para algunas personas, los Pokémon           |
|  son mascotas. Otros los usan para luchar.    |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
		⠀⠀⠀⠀⠀⢸⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠙⢤⡷⣤⣦⣀⠤⠖⠚⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⣠⡿⠢⢄⡀⠀⡇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠸⠷⣶⠂⠀⠀⠀⣀⣀⠀⠀⠀
		⢸⣃⠀⠀⠉⠳⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⢉⡭⠋
		⠀⠘⣆⠀⠀⠀⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀
		⠀⠀⠘⣦⠆⠀⠀⢀⡎⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⣠⠔⠋⠀⠀⠀⠀
		⠀⠀⠀⡏⠀⠀⣆⠘⣄⠸⢧⠀⠀⠀⠀⢀⣠⠖⢻⠀⠀⠀⣿⢥⣄⣀⣀⣀⠀⠀
		⠀⠀⢸⠁⠀⠀⡏⢣⣌⠙⠚⠀⠀⠠⣖⡛⠀⣠⠏⠀⠀⠀⠇⠀⠀⠀⠀⢙⣣⠄
		⠀⠀⢸⡀⠀⠀⠳⡞⠈⢻⠶⠤⣄⣀⣈⣉⣉⣡⡔⠀⠀⢀⠀⠀⣀⡤⠖⠚⠀⠀
		⠀⠀⡼⣇⠀⠀⠀⠙⠦⣞⡀⠀⢀⡏⠀⢸⣣⠞⠀⠀⠀⡼⠚⠋⠁⠀⠀⠀⠀⠀
		⠀⢰⡇⠙⠀⠀⠀⠀⠀⠀⠉⠙⠚⠒⠚⠉⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⢧⡀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠙⣶⣶⣿⠢⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠉⠀⠀⠀⠙⢿⣳⠞⠳⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠹⣄⣀⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     

@-----------------------------------------------@
|                                               |
|             En cuanto a mí.                   |
|                                            ↓  |
@-----------------------------------------------@ 
''')
enter_y_limpia_pantalla()

print('''
		⠀⠀⠀⠀⠀⢸⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠙⢤⡷⣤⣦⣀⠤⠖⠚⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⣠⡿⠢⢄⡀⠀⡇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠸⠷⣶⠂⠀⠀⠀⣀⣀⠀⠀⠀
		⢸⣃⠀⠀⠉⠳⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⢉⡭⠋
		⠀⠘⣆⠀⠀⠀⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀
		⠀⠀⠘⣦⠆⠀⠀⢀⡎⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⣠⠔⠋⠀⠀⠀⠀
		⠀⠀⠀⡏⠀⠀⣆⠘⣄⠸⢧⠀⠀⠀⠀⢀⣠⠖⢻⠀⠀⠀⣿⢥⣄⣀⣀⣀⠀⠀
		⠀⠀⢸⠁⠀⠀⡏⢣⣌⠙⠚⠀⠀⠠⣖⡛⠀⣠⠏⠀⠀⠀⠇⠀⠀⠀⠀⢙⣣⠄
		⠀⠀⢸⡀⠀⠀⠳⡞⠈⢻⠶⠤⣄⣀⣈⣉⣉⣡⡔⠀⠀⢀⠀⠀⣀⡤⠖⠚⠀⠀
		⠀⠀⡼⣇⠀⠀⠀⠙⠦⣞⡀⠀⢀⡏⠀⢸⣣⠞⠀⠀⠀⡼⠚⠋⠁⠀⠀⠀⠀⠀
		⠀⢰⡇⠙⠀⠀⠀⠀⠀⠀⠉⠙⠚⠒⠚⠉⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⢧⡀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠙⣶⣶⣿⠢⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠉⠀⠀⠀⠙⢿⣳⠞⠳⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠹⣄⣀⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    

@-----------------------------------------------@
|                                               |
|  Estudio a los Pokémon como profesión.        |
|                                            ↓  |
@-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|   Pero primero, cuéntame un poco sobre ti.    |
|                                            ↓  |
@-----------------------------------------------@  
''')
enter_y_limpia_pantalla()

print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 

@-----------------------------------------------@
|                                               |
|   Comencemos con tu nombre. ¿Cómo te llamas?  |
|                                               |
@-----------------------------------------------@
''')

while not nombre_del_jugador:
    nombre_del_jugador = input('Escribe tu nombre aquí: ')
os.system('cls')

print('    __ _              ')
print('   /___|_|            ')
print('   l___l__l          ')
print('  /___/  |            ')
print('   l + ~/_/           ')
print('   |___/_/|           ')
print('   /l l l l|          ')
print('  / l l l l|/|        ')
print(' / +l l l l | |       ')
print(' |/|l~__l l / /       ')
print('  |/l l l l l_l       ')
print('    l_l l_l           ')
print('    /_/ |_|           ')
print('                      ')
print('')
print(' @----------------------------------------------@')
print('    Correcto...                                 ')
print(f'   Entonces tu nombre es {nombre_del_jugador}  ')
print(' ')
print('                                              ↓ ')
print(' @----------------------------------------------@')
enter_y_limpia_pantalla()

print('                  __ __        ')
print('                 /     |/|_ _  ')
print('                / __/||l /_/  ')
print('                |/l~ ~l/  l_l   ')
print('                  |_u_/|__| |   ')
print('                 /l   Q ___|_|  ')
print('                 ll    l        ')
print('               /_l  __l        ')
print('                l_l__l__l       ')
print('                  l l ~ l       ')
print('                 l l l l       ')
print('                  l l l l       ')
print('                 /_/ |_|       ')
print('')
print('@----------------------------------------------@')
print('|                                              |')
print('|  Este es mi nieto.                           |')
print('|  Él ha sido tu rival desde que eras un niño. |')
print('|                                              |')
print('|                                            ↓ |')
print('@----------------------------------------------@')
enter_y_limpia_pantalla()

print('                  __ __        ')
print('                 /     |/|_ _  ')
print('                / __/||l /_/  ')
print('                |/l~ ~l/  l_l   ')
print('                  |_u_/|__| |   ')
print('                 /l   Q ___|_|  ')
print('                 ll    l        ')
print('               /_l  __l        ')
print('                l_l__l__l       ')
print('                  l l ~ l       ')
print('                 l l l l       ')
print('                  l l l l       ')
print('                 /_/ |_|       ')
print('')
print('@----------------------------------------------@')
print('|                                              |')
print('|  Hmmmm...                                    |')
print('|  ¿Podrías decirme cómo se llama?             |')
print('@----------------------------------------------@')

while not nombre_del_enemigo:
    nombre_del_enemigo = input('Escribe el nombre de tu rival aquí: ')
os.system('cls')

print('                  __ __        ')
print('                 /     |/|_ _  ')
print('                / __/||l /_/  ')
print('                |/l~ ~l/  l_l   ')
print('                  |_u_/|__| |   ')
print('                 /l   Q ___|_|  ')
print('                 ll    l        ')
print('               /_l  __l        ')
print('                l_l__l__l       ')
print('                  l l ~ l       ')
print('                 l l l l       ')
print('                  l l l l       ')
print('                 /_/ |_|       ')
print('')
print('@----------------------------------------------@')
print('')
print('    ¡Ah, sí!  !Ahora lo recuerdo!              ')
print(f'   ¡Se llama {nombre_del_enemigo}!            ')
print('                                             ↓ ')
print('@----------------------------------------------@')
enter_y_limpia_pantalla()

print('    __ _              ')
print('   /___|_|            ')
print('   l___l__l          ')
print('  /___/  |            ')
print('   l + ~/_/           ')
print('   |___/_/|           ')
print('   /l l l l|          ')
print('  / l l l l|/|        ')
print(' / +l l l l | |       ')
print(' |/|l~__l l / /       ')
print('  |/l l l l l_l       ')
print('    l_l l_l           ')
print('    /_/ |_|           ')
print('                      ')
print('')
print(' @------------------------------------------------------@')
print('')
print(f'   ¡{nombre_del_jugador}! ')
print('   ¡Tu propia leyenda POKéMON está a punto de comenzar!  ')
print('')
print('                                                      ↓  ')
print(' @------------------------------------------------------@')
enter_y_limpia_pantalla()

print('    __ _              ')
print('   /___|_|            ')
print('   l___l__l          ')
print('  /___/  |            ')
print('   l + ~/_/           ')
print('   |___/_/|           ')
print('   /l l l l|          ')
print('  / l l l l|/|        ')
print(' / +l l l l | |       ')
print(' |/|l~__l l / /       ')
print('  |/l l l l l_l       ')
print('    l_l l_l           ')
print('    /_/ |_|           ')
print('                      ')
print('')
print(' @----------------------------------------------@')
print(' |                                              |')
print(' |  ¡Te espera un mundo de sueños y aventuras   |')
print(' |   con los POKéMON!                           |')
print(' |                                            ↓ |')
print(' @----------------------------------------------@')
enter_y_limpia_pantalla()
"""
#Creación de los obstaculos en el mapa
obstaculos_en_mapa = [list(row) for row in obstaculos_en_mapa.split('\n')]


while not tocar_objeto:
    #Impresión de los bordes del mapa
    
    

    for coordenada_y in range(ALTO_MAPA):
        print('|', end='')
        for coordenada_x in range(ANCHO_MAPA):
            
            caracter_a_dibujar = ' '
            objeto_en_celda = None #Inicia la variable de objetos del mapa
            
            #Coloca los objetos en el mapa (puertas, pokebolas, etc..)
            for objeto_del_mapa in objetos_del_mapa:
               if objeto_del_mapa[POSICION_X] == coordenada_x and objeto_del_mapa[POSICION_Y] == coordenada_y:
                    caracter_a_dibujar = '¥'
                    objeto_en_celda = objeto_del_mapa #crea los objetos del mapa
                
            if mi_posicion[POSICION_X] == coordenada_x and mi_posicion[POSICION_Y] == coordenada_y:
                caracter_a_dibujar = '■'
                
                #Para eliminar los objetos del mapa y que no se vuelvan a ver
                if objeto_en_celda:
                    tocar_objeto = True
                    #objetos_del_mapa.remove(objeto_en_celda)
        
            if obstaculos_en_mapa[coordenada_y][coordenada_x] in obstaculos_a_dibujar:
                caracter_a_dibujar = obstaculos_en_mapa[coordenada_y][coordenada_x]
                
            
            print('{}'.format(caracter_a_dibujar), end='')  
            
        print('|')

    print('-' * (ANCHO_MAPA + 2))

    #Movimiento del usuario
    direccion = readchar.readchar()
    nueva_posicion = None

    if direccion.lower() == 'w':
        nueva_posicion = [mi_posicion[POSICION_X], (mi_posicion[POSICION_Y] - 1)]
        
    elif direccion.lower() == 's':
        nueva_posicion = [mi_posicion[POSICION_X], (mi_posicion[POSICION_Y] + 1)]
        
    elif direccion.lower() == 'a':
        nueva_posicion = [(mi_posicion[POSICION_X] - 1), mi_posicion[POSICION_Y]]
        
    elif direccion.lower() == 'd':
        nueva_posicion = [(mi_posicion[POSICION_X] + 1), mi_posicion[POSICION_Y]]
         
    elif direccion == 'q':
        break
    
   
    if obstaculos_en_mapa[nueva_posicion[POSICION_Y]][nueva_posicion[POSICION_X]] not in obstaculos_a_dibujar:
        mi_posicion = nueva_posicion
   
    os.system('cls') 

#Para salir del bucle e iniciar con la entrada del profesor oak
if tocar_objeto:
    print('''
@----------------------------------------------@
|                                              |
|           OAK: ¡HEY ALTO NO VAYAS!           |
|                                              |
@----------------------------------------------@
    ''')
    esperar_pantalla()

    print('''
@----------------------------------------------@
|                                              |
|           ¡Ufff! ¡Estuvo cerca!              |
|                                              |
@----------------------------------------------@
    ''')
    esperar_pantalla()

    print('''
@----------------------------------------------@
|                                              |
|     ¡En la hierba viven POKéMON salvajes!    |
|                                              |
@----------------------------------------------@
    ''')
    esperar_pantalla()
    
    print('''
                          __________
                        (Pika pika!) 
                        (/      
                /\_.._(\   /z 
                (O^__^O) Z__7 
                (v____v)Z 7    
                  v  v         
          _____________________

  @----------------------------------------------@
  |                                              |
  |  ¡Un PIKACHU salvaje aparecio!               |
  |                                              |
  @----------------------------------------------@      
      ''')
    esperar_pantalla()
    
    print('''
                            __________
                          (Pika pika!) 
                          (/      
                  /\_.._(\   /z 
                  (O^__^O) Z__7 
                  (v____v)Z 7    
                    v  v         
            _____________________

  @----------------------------------------------@
  |                                              |
  |  ¡El profesor utiliza pokeball!              |
  |                                              |
  @----------------------------------------------@
      ''')
    esperar_pantalla() 
    
    print('''
                   ° °      
                 °     °     
                °-------° 
                 °     °  
                   ° ° 

@----------------------------------------------@
|                                              |
|     ¡Muy bien! ¡PIKACHU fue atrapado!        |
|                                              |
@----------------------------------------------@
      ''')
    esperar_pantalla()
    
    print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__| 
@----------------------------------------------@
|                                              |
|     Vaya...                                  |
|     ¡Necesitas a tu propio POKéMON como      |
|      protección!                             |
|                                              |
@----------------------------------------------@
       ''')
    esperar_pantalla()
    
    print('''
                    >MVM
                    M~ ~M 
                   °| _ |
                 __-   /-__
                |   ____   | 
                | |_|>  |  | 
                |___>___|| |
                  /  _  |<_|
                 |  / | | 
                 |__| |__|
@----------------------------------------------@
|                                              |
|               ¡Ven conmigo!                  |
|                                            ↓ |
@----------------------------------------------@
     ''')
    enter_y_limpia_pantalla()
    
    print('  ################################################# ')
    print('  ##########     L A B O R A T O R I O   ########## ')
    print('  ##########@---------------------------@########## ')
    print('  ##########|[___][____]       |--|--|--|########## ')
    print('  ##########|                  |__|__|__|########## ')
    print('  ##########|             OKA           |########## ')
    print('  ##########|                           |########## ')
    print('  ##########|                           |########## ')
    print('  ##########|        ■    *             |########## ')
    print('  ##########|                           |########## ')
    print('  ##########|              |---------|  |########## ')
    print('  ##########|              | Ψ  Ф  ȸ |  |########## ')
    print(' @-------------------------------------------------@')
    print('')
    print(f'   {nombre_del_enemigo}: ¡Abuelo! ¡Estoy harto     ')
    print('     de esperar!                                    ')
    print(f'    OAK: ¿{nombre_del_enemigo}?  ')
    print('                                                ↓   ')                        
    print(' @-------------------------------------------------@')
    enter_y_limpia_pantalla()
    
    print('  #################################################')
    print('  ##########     L A B O R A T O R I O   ##########')
    print('  ##########@---------------------------@##########')
    print('  ##########|[___][____]       |--|--|--|##########')
    print('  ##########|                  |__|__|__|##########')
    print('  ##########|             OKA           |##########')
    print('  ##########|                           |##########')
    print('  ##########|                           |##########')
    print('  ##########|        ■    *             |##########')
    print('  ##########|                           |##########')
    print('  ##########|              |---------|  |##########')
    print('  ##########|              | Ψ  Ф  ȸ |  |##########')
    print(' @-------------------------------------------------@')
    print(' |                                                 |')
    print(' |    OAK: ¿Hum? ¿Qué haces aquí?                  |')
    print(' |         Te dije que vinieras más  tarde...      |')
    print(' |         ¡No importa!    Espera ahí.             |')
    print(' |                                               ↓ |')
    print(' @-------------------------------------------------@')
    enter_y_limpia_pantalla()
    
    print('  #################################################')
    print('  ##########     L A B O R A T O R I O   ##########')
    print('  ##########@---------------------------@##########')
    print('  ##########|[___][____]       |--|--|--|##########')
    print('  ##########|                  |__|__|__|##########')
    print('  ##########|             OKA           |##########')
    print('  ##########|                           |##########')
    print('  ##########|                           |##########')
    print('  ##########|        ■    *             |##########')
    print('  ##########|                           |##########')
    print('  ##########|              |---------|  |##########')
    print('  ##########|              | Ψ  Ф  ȸ |  |##########')
    print(' @-------------------------------------------------@')
    print(' ')
    print(f' OAK: ¡Mira, {nombre_del_jugador}! ¿Ves las bolas que')
    print('        están en la mesa? Se llaman POKéBALL.')
    print('       ¡Cada una, contiene un POKéMON en su interior.')
    print('                                                ↓ ')
    print(' @-------------------------------------------------@')
    enter_y_limpia_pantalla()
    
    print('  #################################################')
    print('  ##########     L A B O R A T O R I O   ##########')
    print('  ##########@---------------------------@##########')
    print('  ##########|[___][____]       |--|--|--|##########')
    print('  ##########|                  |__|__|__|##########')
    print('  ##########|             OKA           |##########')
    print('  ##########|                           |##########')
    print('  ##########|                           |##########')
    print('  ##########|        ■    *             |##########')
    print('  ##########|                           |##########')
    print('  ##########|              |---------|  |##########')
    print('  ##########|              | Ψ  Ф  ȸ |  |##########')
    print(' @-------------------------------------------------@')
    print(' |                                                 |')
    print(' |    OAK: ¡Puedes elegir la que quieras!          |')
    print(' |         ¡Es para ti!                            |')
    print(' |                                               ↓ |')
    print(' @-------------------------------------------------@')
    enter_y_limpia_pantalla()
    
    #Creación de los obstaculos en el mapa
obstaculos_en_lab = [list(row) for row in obstaculos_en_lab.split('\n')]


while not tocar_objeto_lab:
  #Impresión de los bordes del mapa
  print('-' * (ANCHO_MAPA_LAB + 2))
  
  for coordenada_y in range(ALTO_MAPA_LAB):
      print('|', end='')
      for coordenada_x in range(ANCHO_MAPA_LAB):
          
          caracter_a_dibujar = ' '
          objeto_en_celda = None #Inicia la variable de objetos del mapa
          
          #Coloca los objetos en el mapa (puertas, pokebolas, etc..)
          for objeto_del_mapa in objetos_del_lab:
            if objeto_del_mapa[POSICION_X] == coordenada_x and objeto_del_mapa[POSICION_Y] == coordenada_y:
                  caracter_a_dibujar = 'Ф'
                  objeto_en_celda = objeto_del_mapa #crea los objetos del mapa
              
          if mi_posicion_lab[POSICION_X] == coordenada_x and mi_posicion_lab[POSICION_Y] == coordenada_y:
              caracter_a_dibujar = '■'
              
              #Para eliminar los objetos del mapa y que no se vuelvan a ver
              if objeto_en_celda:
                  tocar_objeto_lab = True
                  #objetos_del_lab.remove(objeto_en_celda)
      
          #Crear los objetos del mapa        
          if obstaculos_en_lab[coordenada_y][coordenada_x] in obstaculos_a_dibujar_lab:
              caracter_a_dibujar = obstaculos_en_lab[coordenada_y][coordenada_x]
              
          
          print('{}'.format(caracter_a_dibujar), end='')  
          
      print('|')

  print('-' * (ANCHO_MAPA_LAB + 2))

  #Movimiento del usuario
  direccion = readchar.readchar()
  nueva_posicion = None

  if direccion.lower() == 'w':
      nueva_posicion = [mi_posicion_lab[POSICION_X], (mi_posicion_lab[POSICION_Y] - 1)]
      
  elif direccion.lower() == 's':
      nueva_posicion = [mi_posicion_lab[POSICION_X], (mi_posicion_lab[POSICION_Y] + 1)]
      
  elif direccion.lower() == 'a':
      nueva_posicion = [(mi_posicion_lab[POSICION_X] - 1), mi_posicion_lab[POSICION_Y]]
      
  elif direccion.lower() == 'd':
      nueva_posicion = [(mi_posicion_lab[POSICION_X] + 1), mi_posicion_lab[POSICION_Y]]
      
  elif direccion == 'q':
      break
  

  if obstaculos_en_lab[nueva_posicion[POSICION_Y]][nueva_posicion[POSICION_X]] not in obstaculos_no_atravesar_lab:
      mi_posicion_lab = nueva_posicion

  os.system('cls') 

#Para salir del bucle
if tocar_objeto_lab:
  print(' @-------------------------------------------------@')
  print(' ')
  print(f'     {nombre_del_enemigo}: ¿Y yo que?')
  print(f'     OAK: ¡Tranquilo, {nombre_del_enemigo}! ')
  print('           Te daré otro a ti más tarde.      ')
  print('                                                ↓ ')
  print(' @-------------------------------------------------@')
  enter_y_limpia_pantalla()
  
  print(' @-------------------------------------------------@')
  print(' ')
  print(f'   OAK: {nombre_del_jugador}, este es el Pokémon ')
  print('          que atrapaste antes. Puedes tenerlo.    ')
  print('                                                ↓ ')
  print(' @-------------------------------------------------@')
  enter_y_limpia_pantalla()
  
  print(' ')
  print('⠀⠀⠀⠀⠀⣁⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣄⡀⠀⢀⣀⣀⡀')
  print('⠀⠀⠀⠀⣼⠝⠉⠉⠛⠷⣦⣤⣶⣶⣶⣶⡾⠃⠀⠈⢻⡾⠛⠉⠉⢻')
  print('⠀⠀⠀⠀⣿⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⣼⠁⠀⣾⢻⡶⠛⠲⣄⣤⠼⢧⣄')
  print('⠀⠀⠀⠀⣿⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⢙⣿⡀⠀⠀⣹⢶⡄⠀⣹⡀')
  print('⠀⠀⠀⣰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠛⠒⢺⡛⠛⠁⣰⠏')
  print('⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠚⢹⡇')
  print('⢠⡶⢼⣷⢤⠄⠀⠀⢀⣀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⣀⠀⠀⠀⠤⠾⣿⠖⠶⠆')
  print('⠀⠀⢈⣿⣀⡀⠀⠀⢿⡿⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠸⣿⠇⠀⠀⠠⣴⣿⣄⣀')
  print('⠀⠘⠋⠹⣷⣀⣀⠀⠀⠀⠀⠀⠀⠀⠯⣦⠽⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⠃')
  print('⠀⠀⣠⡴⠟⠻⣧⡶⠳⣦⣠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡟⠋⠛⠶⠄⠀')
  print('⠀⠀⠁⠀⢀⡾⠛⠂⣀⡈⠀⢹⣧⣤⣄⣀⣀⣠⣤⣤⣴⣶⣾⠛⠁')
  print('⠀⠀⠀⠀⠈⣷⣤⠄⠛⠃⠈⢿⢹⣄⠀⠀⠀⢠⡿⠀⠈⢷⡉⣻⣦⣤⣀')
  print('⠀⠀⠀⠀⣼⠏⢿⣤⣴⡷⣶⡟⠀⠙⠳⠶⠶⠛⠁⠀⠀⠈⣿⡋⠀⠈⣿⠆')
  print('⠀⠀⠀⠀⢻⣆⠀⠀⢸⣿⣜⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⣽')
  print('⠀⠀⠀⠀⠀⠙⠻⣶⠞⠃⠙⠶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡶⠾⠋')
  print('⠀⠀⠀⠀⠀⠀⢸⡿⠶⢶⣤⣤⣤⣤⣤⣿⣤⣤⣤⣤⣤⣤⡶⢾⡇')
  print('⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⣸⡇')
  print('⠀⠀⠀⠀⠀⠀⠀⠹⣷⣤⣀⣀⣀⣀⣠⣿⣀⣀⣀⣀⣀⣠⣴⠟')
  print('       ⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠛⠛⠛⠋⠉')
  print(' @-------------------------------------------------@')
  print(' ')
  print(f'   {nombre_del_jugador} ¡Has adquirido a SQUARTLE ')
  print('                                                ↓ ')
  print(' @-------------------------------------------------@')
  enter_y_limpia_pantalla()


#Creación de los obstaculos en el mapa
obstaculos_en_mapa_villano = [list(row) for row in obstaculos_en_mapa_villano.split('\n')]


while not tocar_objeto_villano:
    #Impresión de los bordes del mapa
    print('-' * (ANCHO_MAPA + 2))

    for coordenada_y in range(ALTO_MAPA):
        print('|', end='')
        for coordenada_x in range(ANCHO_MAPA):
            
            caracter_a_dibujar = ' '
            objeto_en_celda = None #Inicia la variable de objetos del mapa
            
            #Coloca los objetos en el mapa (puertas, pokebolas, etc..)
            for objeto_del_mapa in objetos_del_mapa_villano:
               if objeto_del_mapa[POSICION_X] == coordenada_x and objeto_del_mapa[POSICION_Y] == coordenada_y:
                    caracter_a_dibujar = '¥'
                    objeto_en_celda = objetos_del_mapa_villano #crea los objetos del mapa
                
            if mi_posicion_villano[POSICION_X] == coordenada_x and mi_posicion_villano[POSICION_Y] == coordenada_y:
                caracter_a_dibujar = '■'
                
                #Para eliminar los objetos del mapa y que no se vuelvan a ver
                if objeto_en_celda:
                    tocar_objeto_villano = True
                    #objetos_del_mapa_villano.remove(objeto_en_celda)
        
            if obstaculos_en_mapa_villano[coordenada_y][coordenada_x] in obstaculos_a_dibujar_villano:
                caracter_a_dibujar = obstaculos_en_mapa_villano[coordenada_y][coordenada_x]
                
            
            print('{}'.format(caracter_a_dibujar), end='')  
            
        print('|')

    print('-' * (ANCHO_MAPA + 2))

    #Movimiento del usuario
    direccion = readchar.readchar()
    nueva_posicion = None

    if direccion.lower() == 'w':
        nueva_posicion = [mi_posicion_villano[POSICION_X], (mi_posicion_villano[POSICION_Y] - 1)]
        
    elif direccion.lower() == 's':
        nueva_posicion = [mi_posicion_villano[POSICION_X], (mi_posicion_villano[POSICION_Y] + 1)]
        
    elif direccion.lower() == 'a':
        nueva_posicion = [(mi_posicion_villano[POSICION_X] - 1), mi_posicion_villano[POSICION_Y]]
        
    elif direccion.lower() == 'd':
        nueva_posicion = [(mi_posicion_villano[POSICION_X] + 1), mi_posicion_villano[POSICION_Y]]
         
    elif direccion == 'q':
        break
    
   
    if obstaculos_en_mapa_villano[nueva_posicion[POSICION_Y]][nueva_posicion[POSICION_X]] not in obstaculos_a_dibujar_villano:
        mi_posicion_villano = nueva_posicion
   
    os.system('cls') 

#Para salir del bucle
if tocar_objeto_villano:
    
    print('                  __\__        ')
    print('                 /     \/\_ _  ')
    print('                / __/\/\l /_/  ')
    print('                \/l~ ~l/  l_l   ')
    print('                  \_u_/\__\ \   ')
    print('                 /l   Q ___\_\  ')
    print('                 ll    l        ')
    print('               /_l  __l        ')
    print('                l_l__l__l       ')
    print('                  l l ~ l       ')
    print('                 l l l l       ')
    print('                  l l l l       ')
    print('                 /_/ \_\       ')
    print('')
    print('@----------------------------------------------@')
    print('')
    print(f' {nombre_del_enemigo}: Pensabas que te ibas   ')
    print('                        a escapar?             ')
    print('                                            ↓  ')
    print('@----------------------------------------------@')
    enter_y_limpia_pantalla()
    
    print('                  __\__        ')
    print('                 /     \/\_ _  ')
    print('                / __/\/\l /_/  ')
    print('                \/l~ ~l/  l_l   ')
    print('                  \_u_/\__\ \   ')
    print('                 /l   Q ___\_\  ')
    print('                 ll    l        ')
    print('               /_l  __l        ')
    print('                l_l__l__l       ')
    print('                  l l ~ l       ')
    print('                 l l l l       ')
    print('                  l l l l       ')
    print('                 /_/ \_\       ')
    print('')
    print('@----------------------------------------------@')
    print('')
    print(f' {nombre_del_enemigo}: Preparate para la    ')
    print('                        batalla Pokémon!       ')
    print('                                            ↓  ')
    print('@----------------------------------------------@')
    enter_y_limpia_pantalla()
    
    print('@----------------------------------------------@')
    print('')
    print(f' {nombre_del_enemigo}: Pikachu preparate a    ')
    print('                        pelar!       ')
    print('                                            ↓  ')
    print('@----------------------------------------------@')
    enter_y_limpia_pantalla()
    
    
    while vida_pikachu > 0 and vida_squartle > 0:
        #Inician los turnos de combate

        #Turno de Pikachu
        print('|----------------------|')         
        print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
        print('  Squartle                    ')
        print('|----------------------|           ________ ')
        print('                                   \/    \/ ')
        print('                                   / ^  ^ \ ')
        print('                                   I\____/I ')
        print('                                  /_\    /_\  ')
        print('       ________                     |    |')
        print('       \/    \/                    /_\__/_\ ')
        print('       /  ^^  \              |-----------------|')
        print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
        print('     /_\      /_\              Pikachu               ')
        print('       |      |              |-----------------|')
        print('      /_\____/_\                                ')
        print('@------------------------------------------------@')
        print('|         Turno de Pikachu para atacar           |')
        print('|                                              ↓ |')
        print('@------------------------------------------------@')
        enter_y_limpia_pantalla()
            
        ataque_pikachu = randint(1, 2)
        if ataque_pikachu == 1:
            #Bola voltio
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Pikachu ha utilizado Bola Voltio       |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            vida_squartle -= BOLA_VOLTIO
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Pikachu ha utilizado Bola Voltio       |')
            print('|         Parece ser muy efectivo!               |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()

        else:
            #Onda Trueno
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Pikachu ha utilizado Onda Trueno       |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            vida_squartle -= ONDA_TRUENO
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Pikachu ha utilizado Onda Trueno       |')
            print('|  Parece que este ataca es bastante efectivo    |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
             

        #Turno de Squartle
        print('|----------------------|')         
        print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
        print('  Squartle                    ')
        print('|----------------------|           ________ ')
        print('                                   \/    \/ ')
        print('                                   / ^  ^ \ ')
        print('                                   I\____/I ')
        print('                                  /_\    /_\  ')
        print('       ________                     |    |')
        print('       \/    \/                    /_\__/_\ ')
        print('       /  ^^  \              |-----------------|')
        print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
        print('     /_\      /_\              Pikachu               ')
        print('       |      |              |-----------------|')
        print('      /_\____/_\                                ')
        print('@------------------------------------------------@')
        print('|         Turno de Squartle para atacar          |')
        print('|                                              ↓ |')
        print('@------------------------------------------------@')
        enter_y_limpia_pantalla()
        
        if vida_squartle < 0:
                vida_squartle = 0

        if vida_pikachu < 0:
               vida_pikachu = 0

        ataque_squartle = ' '
        while ataque_squartle.upper() not in ['P', 'A', 'B', 'N']:
                   
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|     Que ataque deseas realizar?                |')
            print('|     [P]lacaje                                  |')
            print('|     Pistola de [A]gua                          |')
            print('|     [B]urbujas                                 |')
            print('|     [N]ada                                   ↓ |')
            print('@------------------------------------------------@')
            ataque_squartle = input('Introduce el ataque: ')
            
        if ataque_squartle.upper() == 'P':
            os.system('cls')
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Squartle ataca con Placaje             |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            
            vida_pikachu -= PLACAJE
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|         Squartle ataca con Placaje             |')
            print('|         No parece ser muy efectivo             |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            
        elif ataque_squartle.upper() == 'A':
            os.system('cls')
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|      Squartle ataca con Pistola de Agua        |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
           
            vida_pikachu -= PISTOLA_AGUA
            
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|      Squartle ataca con Pistola de Agua        |')
            print('|      Pikachu se queda empapado                 |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()

        elif ataque_squartle.upper() == 'B':
            os.system('cls')
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|      Squartle ataca con Burbujas               |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            
            vida_pikachu -= BURBUJAS
            
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|      Squartle ataca con Burbujas               |')
            print('|      Es muy poco efectivo                      |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            
        elif ataque_squartle.upper() == 'N':
            os.system('cls')
            print('|----------------------|')         
            print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
            print('  Squartle                    ')
            print('|----------------------|           ________ ')
            print('                                   \/    \/ ')
            print('                                   / ^  ^ \ ')
            print('                                   I\____/I ')
            print('                                  /_\    /_\  ')
            print('       ________                     |    |')
            print('       \/    \/                    /_\__/_\ ')
            print('       /  ^^  \              |-----------------|')
            print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
            print('     /_\      /_\              Pikachu               ')
            print('       |      |              |-----------------|')
            print('      /_\____/_\                                ')
            print('@------------------------------------------------@')
            print('|      Squirtle no hace nada....                 |')
            print('|                                              ↓ |')
            print('@------------------------------------------------@')
            enter_y_limpia_pantalla()
            
        if vida_squartle < 0:
            vida_squartle = 0

        if vida_pikachu < 0:
            vida_pikachu = 0

       
    if vida_pikachu > vida_squartle:
        os.system('cls')
        print('|----------------------|')         
        print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
        print('  Squartle                    ')
        print('|----------------------|           ________ ')
        print('                                   \/    \/ ')
        print('                                   / ^  ^ \ ')
        print('                                   I\____/I ')
        print('                                  /_\    /_\  ')
        print('       ________                     |    |')
        print('       \/    \/                    /_\__/_\ ')
        print('       /  ^^  \              |-----------------|')
        print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
        print('     /_\      /_\              Pikachu               ')
        print('       |      |              |-----------------|')
        print('      /_\____/_\                                ')
        print('@------------------------------------------------@')
        print('|      Squartle no tiene más vida!               |')
        print('|                                              ↓ |')
        print('@------------------------------------------------@')
        enter_y_limpia_pantalla()

        print('                  __\__        ')
        print('                 /     \/\_ _  ')
        print('                / __/\/\l /_/  ')
        print('                \/l~ ~l/  l_l   ')
        print('                  \_u_/\__\ \   ')
        print('                 /l   Q ___\_\  ')
        print('                 ll    l        ')
        print('               /_l  __l        ')
        print('                l_l__l__l       ')
        print('                  l l ~ l       ')
        print('                 l l l l       ')
        print('                  l l l l       ')
        print('                 /_/ \_\       ')
        print('')
        print('@----------------------------------------------@')
        print('')
        print(f'    ¡{nombre_del_enemigo} GANA!              ')
        print('                                             ↓ ')
        print('@----------------------------------------------@')
        enter_y_limpia_pantalla()
        
    else:
        os.system('cls')
        print('|----------------------|')         
        print( ' ',  vida_squartle, '/', VIDA_INICIAL_SQUARTLE, 'HP')
        print('  Squartle                    ')
        print('|----------------------|           ________ ')
        print('                                   \/    \/ ')
        print('                                   / ^  ^ \ ')
        print('                                   I\____/I ')
        print('                                  /_\    /_\  ')
        print('       ________                     |    |')
        print('       \/    \/                    /_\__/_\ ')
        print('       /  ^^  \              |-----------------|')
        print('      I   ^^   I ' ,'            ', vida_pikachu, '/', VIDA_INICIAL_PIKACHU, 'HP')       
        print('     /_\      /_\              Pikachu               ')
        print('       |      |              |-----------------|')
        print('      /_\____/_\                                ')
        print('@------------------------------------------------@')
        print('|      Pikachu no tiene más vida!                |')
        print('|                                              ↓ |')
        print('@------------------------------------------------@')
        enter_y_limpia_pantalla()
        
        print('    __ _              ')
        print('   /___|_|            ')
        print('   l___l__l          ')
        print('  /___/  |            ')
        print('   l + ~/_/           ')
        print('   |___/_/|           ')
        print('   /l l l l|          ')
        print('  / l l l l|/|        ')
        print(' / +l l l l | |       ')
        print(' |/|l~__l l / /       ')
        print('  |/l l l l l_l       ')
        print('    l_l l_l           ')
        print('    /_/ |_|           ')
        print('                      ')
        print('')
        print(' @------------------------------------------------------@')
        print('')
        print(f'   ¡{nombre_del_jugador} GANA! ')
        print('                                                       ↓')
        print(' @------------------------------------------------------@')
        enter_y_limpia_pantalla()


print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX| ¡Felicidades, entrenador!  |XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|                           ↓|XXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
enter_y_limpia_pantalla()

print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXX|Has demostrado tu valentía, |XXXXXXXXXX')
print('XXXXXXXXXX|sabiduría y amistad a lo    |XXXXXXXXXX')
print('XXXXXXXXXX|largo de tu viaje.          |XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|                           ↓|XXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
enter_y_limpia_pantalla()

print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXX|Que tu aventura nunca       |XXXXXXXXXX')
print('XXXXXXXXXX|termine y que la llama      |XXXXXXXXXX')
print('XXXXXXXXXX|de la pasión por los        |XXXXXXXXXX')
print('XXXXXXXXXX|Pokémon siempre arda en     |XXXXXXXXXX')
print('XXXXXXXXXX|tu corazón.                ↓|XXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
enter_y_limpia_pantalla()

print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|      ¡Hasta la próxima!    |XXXXXXXXXX')
print('XXXXXXXXXX|                            |XXXXXXXXXX')
print('XXXXXXXXXX|                           ↓|XXXXXXXXXX')
print('XXXXXXXXXX@----------------------------@XXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
enter_y_limpia_pantalla()

print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXX@---------------------------@XXXXXXXXXX')
print('XXXXXXXXXX|                           |XXXXXXXXXX')
print('XXXXXXXXXX|                           |XXXXXXXXXX')
print('XXXXXXXXXX|       Fin del juego       |XXXXXXXXXX')
print('XXXXXXXXXX|                           |XXXXXXXXXX')
print('XXXXXXXXXX|                          ↓|XXXXXXXXXX')
print('XXXXXXXXXX@---------------------------@XXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
enter_y_limpia_pantalla()

print('''    
                                @-----------------------------------------------@
                                |                                               |
                                |  ©2024 ITLA                                   |
                                |                                               |
                                |         Fundamentos de Programación           |
                                |              Prof. Wilmer Fariña              |                     
                                |                                               |
                                |          Autores:                             |
                                |               Lesley Peguero 2023-1234        |
                                |               Christian Gil 2012-1036     ↓   |
                                @-----------------------------------------------@
''')
enter_y_limpia_pantalla()

print('''
                        ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
                        ▐ ██████   ██████  ██   ██ ███████ ███    ███  ██████  ███    ██ ▌
                        ▐ ██   ██ ██    ██ ██  ██  ██      ████  ████ ██    ██ ████   ██ ▌
                        ▐ ██████  ██    ██ █████   █████   ██ ████ ██ ██    ██ ██ ██  ██ ▌
                        ▐ ██      ██    ██ ██  ██  ██      ██  ██  ██ ██    ██ ██  ██ ██ ▌
                        ▐ ██       ██████  ██   ██ ███████ ██      ██  ██████  ██   ████ ▌
                        ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌                                                         
''')
enter_y_limpia_pantalla()