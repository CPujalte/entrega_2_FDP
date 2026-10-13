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

# Creación de una lista con todos los ID de casillas válidas para poder comprobar rápidamente si una casilla existe en el tablero mediante una función.

"""
ID de cada casilla del tablero como guía, las casillas se almacenan de esta manera internamente en el código
   A  B  C  D  E  F  G  H
8  07 17 27 37 47 57 67 77
7  06 16 26 36 46 56 66 76
6  05 15 25 35 45 55 65 75
5  04 14 24 34 44 54 64 74
4  03 13 23 33 43 53 63 73
3  02 12 22 32 42 52 62 72
2  01 11 21 31 41 51 61 71
1  00 10 20 30 40 50 60 70
"""

casillas_ID_perm: list = []
for i in range(8):
    for j in range(8):
        casillas_ID_perm.append(str(i)+str(j))

def _comprobar_casilla_ID(c1):
    return c1 in casillas_ID_perm

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
def _color_pieza(p: str):
    global piezas_blancas
    global piezas_negras
    if p in piezas_blancas:
        return "blancas"
    elif p in piezas_negras:
        return "negras"
    else:
        return "vacío"

# Función que devuelve la pieza en cierta casilla
def _pieza_en_casilla(c1: str):
    global tablero
    return tablero[int(c1[1])][int(c1[0])]

# Función para mover una pieza de una casilla a otra
def _mover_pieza(c1: str, c2: str):
    global tablero
    global casillas_mov_perm
    casillas_mov_perm = []
    pieza = _pieza_en_casilla(c1)
    if _mov_valido(c1, c2, pieza):
        tablero[int(c2[1])][int(c2[0])] = pieza
        tablero[int(c1[1])][int(c1[0])] = "·"
        _cambiar_turno()

# Función que dirige el código a la comprobación del movimiento de pieza necesaria y si es posible realizarlo
def _mov_valido(c1: str, c2: str, p: str):
    global estado
    if _color_pieza(p) == "vacío":      # Comprobación de que se ha seleccionado una pieza y no una casilla vacía
        print("No hay ninguna pieza en la casilla de origen.")
        return False
    elif _color_pieza(p) != estado:     # Comprobación de que el color de la pieza es del jugador al que le toca
        print("Esa pieza no es tuya, es el turno de las " + estado + ".")
        return False
    elif c1 == c2:
        print("El origen y el destino son la misma casilla.")
        return False
    elif _color_pieza(_pieza_en_casilla(c1)) == _color_pieza(_pieza_en_casilla(c2)):
        print("La casilla de destino está ocupada por una pieza propia.")
        return False
    else:
        if p == TB or p == TN:
            resultado = _comp_torre(c1, c2)
            if resultado == False:
                print("Movimiento no válido, selecciona un movimiento válido para la torre.")
            return resultado
        return True

# Cúmulo de funciones para comprobar los movimientos de las diferentes piezas.
"""
Las funciones siguientes son algo complejas por lo que precisaré en cada una individualmente cuando sea necesario.

El objetivo de las funciones es comprobar que el la pieza puede desplazarse desde c1 hasta c2, devolviendo True si ese es el caso.
Hay una función para cada pieza a excepción de para la dama, puesto que es la combinación de la torre y el alfil.
En la función _mov_válido se decide cuál de las funciones es la necesaria dependiendo de la pieza.
"""

def _comp_torre(c1: str, c2: str) -> bool:
    global estado
    global casillas_mov_perm

    """
    Para la comprobación de la torre, simulamos el avance de la torre en las 4 direcciones cardinales, expresadas con la lista [1, -1, 10, -10]
    La c se le multiplica a la i para determinar la dirección y el sentido en cada una de las 4 iteraciones del bucle completo.
    Al multiplicar por c=1 o c=-1 se simula el cambio de fila hacia el Norte y hacia el Sur, respectivamente.
    Al multiplicar por c=10 o c=-10 se simula el cambio de columna hacia el Este y hacia el Oeste, respectivamente.
    Cuando se topa con una pieza, el bulce se detiene y se pasa a la siguiente dirección cardinal.
    """
    # Comprobación de las 4 direcciones
    for c in [1, -1, 10, -10]:
        for i in range(1, 8):
            casilla_a_comprobar = str(int(c1) + i*c)
            if _comprobar_casilla_ID(casilla_a_comprobar) == False:     # Comprobación de que el ID de la casilla es válido
                break
            elif _pieza_en_casilla(casilla_a_comprobar) == "·":         # Si la casilla está vacía, se añade a la lista de movimientos permitidos, si no la pieza no puede seguir avanzando y se detiene el bucle para esta dirección
                casillas_mov_perm.append(casilla_a_comprobar)
            else:                                                       # La condición siguiente sirve para filtrar el caso en el que el programa se topa con una casilla que tiene una pieza de color opuesto, de manera que la captura.
                if (estado == "blancas" and _pieza_en_casilla(casilla_a_comprobar) in piezas_negras) or (estado == "negras" and _pieza_en_casilla(casilla_a_comprobar) in piezas_blancas):
                    casillas_mov_perm.append(casilla_a_comprobar)
                break

    # Devolución de un bool que indica si el movimiento final es legal o no
    return c2 in casillas_mov_perm

# Declaración de la función que pone en marcha la máquina de estados para comenzar la partida.
def _comenzar_partida():
    global estado
    _imprimir_tablero()
    user_input: str = ""
    casilla_1: str = "."
    casilla_2: str = "."
    while user_input != "salir":
        print("Turno de las", estado + ".")
        user_input = input("Introduce un movimiento válido o escribe 'salir' para finalizar: ").lower()

        if user_input == "salir":
            estado = "salir"

        elif len(user_input) == 5 and user_input[0] in letras_perm and user_input[1] in numeros_perm and user_input[2] == " " and user_input[3] in letras_perm and user_input[4] in numeros_perm:
            casilla_1 = str(letras_perm.find(user_input[0])) + str(numeros_perm.find(user_input[1]))
            casilla_2 = str(letras_perm.find(user_input[3])) + str(numeros_perm.find(user_input[4]))
            _mover_pieza(casilla_1, casilla_2)
            print("")
            _imprimir_tablero()

        else:
            print("Formato no válido. Escribe origen y destino, por ejemplo: e2 e4")

# Comienzo del programa
_comenzar_partida()