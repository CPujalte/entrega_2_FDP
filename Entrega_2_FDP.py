# ENTREGA 2

# Declaración de variables con los símbolos unicode para las piezas de manera que no es necesario copiar el unicode repetidamente.
PB: str = "\u2659"
CB: str = "\u2658"
AB: str = "\u2657"
TB: str = "\u2656"
DB: str = "\u2655"
RB: str = "\u2654"
PN: str = "\u265F"
CN: str = "\u265E"
AN: str = "\u265D"
TN: str = "\u265C"
DN: str = "\u265B"
RN: str = "\u265A"

# Declaración de dos listas, una con las piezas blancas y otra con las piezas negras.
piezas_blancas: tuple = (PB, CB, AB, TB, DB, RB)
piezas_negras: tuple = (PN, CN, AN, TN, DN, RN)

# Creación de un diccionario con todos los nombres de las piezas para imprimir para tener el género correcto de cada sustantivo.
mensajes: dict = {
    PB: "un peón blanco",
    CB: "un caballo blanco",
    AB: "un alfil blanco",
    TB: "una torre blanca",
    DB: "una dama blanca",
    RB: "un rey blanco",
    PN: "un peón negro",
    CN: "un caballo negro",
    AN: "un alfil negro",
    TN: "una torre negra",
    DN: "una dama negra",
    RN: "un rey negro"
}

# Declaración de variables con los caracteres posibles para determinar si el input es válido.
letras_perm: str = "abcdefgh"
numeros_perm: str = "12345678"

# Formación del tablero inicial.
tablero_inicial: tuple = (
    [TB, CB, AB, DB, RB, AB, CB, TB],   # Fila de piezas blancas específicas.
    [PB] * 8,                           # Fila de peones blancos.
    ["·"] * 8,                          # Fila vacía.
    ["·"] * 8,                          # Fila vacía.
    ["·"] * 8,                          # Fila vacía.
    ["·"] * 8,                          # Fila vacía.
    [PN] * 8,                           # Fila de peones negros.
    [TN, CN, AN, DN, RN, AN, CN, TN]    # Fila de piezas negras específicas.
)

"""
ID de cada casilla del tablero como guía, las casillas se almacenan de esta manera internamente en el código
   A  B  C  D  E  F  G  H
8  00 10 20 30 40 50 60 70
7  01 11 21 31 41 51 61 71
6  02 12 22 32 42 52 62 72
5  03 13 23 33 43 53 63 73
4  04 14 24 34 44 54 64 74
3  05 15 25 35 45 55 65 75
2  06 16 26 36 46 56 66 76
1  07 17 27 37 47 57 67 77
"""

# Declaración del tablero inicial modificable para la partida.
tablero: list = list(tablero_inicial)

# Función para imprimir el tablero
def _imprimir_tablero():
    global tablero
    print("   A B C D E F G H")
    for i in range(8):
        print(8-i, end = "  ")
        for j in tablero[7-i]:
            print(j, end = " ")
        print("")
    print("")

# Función para cambiar el turno
estado: str = "blancas"
def _cambiar_turno():
    global estado
    if estado == "blancas":
        estado = "negras"
    else:
        estado = "blancas"

# Declaración de una variable global que guarda las casillas a las que una pieza se puede mover
casillas_mov_perm: list = []

# Función que devuelve el color de la pieza
def _color_pieza(p):
    global piezas_blancas
    global piezas_negras
    if p in piezas_blancas:
        return "blancas"
    elif p in piezas_negras:
        return "negras"
    else:
        return "vacío"

# Función para mover una pieza de una casilla a otra
def _mover_pieza(c1, c2):
    global tablero
    global casillas_mov_perm
    casillas_mov_perm = []
    pieza = tablero[int(c1[1])][int(c1[0])]
    tablero[int(c2[1])][int(c2[0])] = pieza
    tablero[int(c1[1])][int(c1[0])] = "·"

# Función que dirige el código a la comprobación del movimiento de pieza necesaria y si es posible realizarlo
def _mov_valido(c1, c2, p):
    global estado
    if _color_pieza(p) == "vacío":      # Comprobación de que se ha seleccionado una pieza y no una casilla vacía
        print("La casilla está vacía, selecciona una casilla válida para mover la pieza.")
        return False
    elif _color_pieza(p) != estado:     # Comprobación de que el color de la pieza es del jugador al que le toca
        print("Selecciona una pieza de las " + estado + ".")
        return False

# Cúmulo de funciones para comprobar los movimientos de las diferentes piezas.
def _comp_torre(c1, c2):
    for i in range(7):
        print("")
        
    
# Declaración de la función que pone en marcha la máquina de estados para comenzar la partida.
def _comenzar_partida():
    _imprimir_tablero()
    user_input: str = ""
    casilla_1: str = "."
    casilla_2: str = "."
    global estado
    while user_input != "salir":
        print("Turno de las", estado + ".")
        user_input = input("Introduce un movimiento válido o escribe 'salir' para finalizar: ")

        if user_input == "salir":
            estado = "salir"

        elif len(user_input) == 5 and user_input[0] in letras_perm and user_input[1] in numeros_perm and user_input[2] == " " and user_input[3] in letras_perm and user_input[4] in numeros_perm:
            casilla_1 = str(letras_perm.find(user_input[0])) + str(numeros_perm.find(user_input[1]))
            casilla_2 = str(letras_perm.find(user_input[3])) + str(numeros_perm.find(user_input[4]))
            _mover_pieza(casilla_1, casilla_2)
            _imprimir_tablero()
            _cambiar_turno()

        else:
            print("Comando no válido.")
        print("")

# Comienzo del programa
_comenzar_partida()