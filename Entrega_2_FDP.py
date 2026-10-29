# ENTREGA 2

# Declaracion de variables con los caracteres posibles para determinar si las casillas son validas.
letras_perm: str = "abcdefgh"
numeros_perm: str = "12345678"

# Creacion de la clase Pieza
class Pieza:

    # Diccionario con todos los unicode para su posterior asignacion
    unicode_list_pieza: dict[str, str] = {
        "PB": "\u2659",
        "CB": "\u2658",
        "AB": "\u2657",
        "TB": "\u2656",
        "DB": "\u2655",
        "RB": "\u2654",
        "PN": "\u265F",
        "CN": "\u265E",
        "AN": "\u265D",
        "TN": "\u265C",
        "DN": "\u265B",
        "RN": "\u265A"
    }

    # Definicion de pieza en particular
    def __init__(self, nombre:str, color:str) -> None:
        self.nombre: str = nombre
        self.color: str = color
        self.simbolo: str = self.unicode_list_pieza.get(nombre[0].upper()+color[0].upper())

# Creacion de la clase Tablero
class Tablero:

    # Definicion de tablero vacio
    def __init__(self) -> None:
        self.casillas: list[list[Pieza | None]] = []
        for i in range(8):
            fila_vacia: list[Pieza | None] = [None] * 8
            self.casillas.append(fila_vacia)

        # Lista con todos los ID de casillas validas y sus respectivas posiciones.
        """
        ID de cada casilla del tablero como guia, las casillas se almacenan de esta manera internamente en el codigo
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

    # Metodo para colocar una pieza en una casilla
    def colocar(self, pieza: Pieza, casilla: str) -> None:
        self.casillas[int(casilla[1])][int(casilla[0])] = pieza

    # Metodo para obtener la pieza en cierta casilla
    def pieza_en_casilla(self, casilla: str) -> Pieza | None:
        if self.casillas[int(casilla[1])][int(casilla[0])] != None:
            return self.casillas[int(casilla[1])][int(casilla[0])]
        else: return None

    # Metodo para comprobar la existencia de cierta casilla
    def existe_casilla(self, casilla: str) -> bool:
        if casilla[0] in "01234567" and casilla[1] in "01234567":
            return True
        else: return False

    # Metodo para imprimir el tablero
    def imprimir_tablero(self) -> None:
        print("   A B C D E F G H")
        for i in range(8):
            print(8-i, end = "  ")
            for j in self.casillas[7-i]:
                contenido: Pieza | None = j
                if isinstance(contenido, Pieza):
                    contenido = contenido.simbolo
                else:
                    contenido = "."
                print(contenido, end = " ")
            print("")
        print("")

    # Metodo para reemplazar el tablero por un tablero en la posicion inicial
    def reiniciar(self) -> None:
        for i in range(8):
            for j in range(8):
                self.casillas[i][j] = None

        fila_a_colocar: int = 0
        columna_a_colocar: int = 0

        clases_pieza: dict[str, Pieza] = {
            "peon": Peon,
            "caballo": Caballo,
            "alfil": Alfil,
            "torre": Torre,
            "dama": Dama,
            "rey": Rey
        }

        for color in ["blanco", "negro"]:
            for nombre in ["torre", "caballo", "alfil", "dama", "rey", "alfil", "caballo", "torre"]:
                self.colocar(clases_pieza[nombre](color), str(columna_a_colocar) + ["0", "7"][fila_a_colocar])
                columna_a_colocar += 1
            columna_a_colocar = 0
            for nombre in range(8):
                self.colocar(clases_pieza["peon"](color), str(columna_a_colocar) + ["1", "6"][fila_a_colocar])
                columna_a_colocar += 1
            columna_a_colocar = 0
            fila_a_colocar += 1

    # Metodo para mover una pieza de una casilla a otra
    def mover_pieza(self, casilla_inicio: str, casilla_llegada: str, verificar_movimiento: bool = True) -> None:
        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)
        global estado
        validez_movimiento: bool = True

        if verificar_movimiento == True:
            validez_movimiento = self.es_movimiento_valido(casilla_inicio, casilla_llegada)

        if validez_movimiento == True:
            self.colocar(pieza, casilla_llegada)
            self.colocar(None, casilla_inicio)
            if isinstance(pieza, Peon):
                self.comprobar_coronacion(casilla_llegada)

    # Metodo para comprobar la validez de cierto movimiento
    def es_movimiento_valido(self, casilla_inicio: str, casilla_llegada: str, comp_jaque: bool = True) -> bool:
        global estado
        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)
        validez_movimiento: bool = True

        if pieza == None:
            print("No hay ninguna pieza en la casilla de origen")
            validez_movimiento = False
        elif (pieza.color == "blanco" and estado == "turno_negras") or (pieza.color == "negro" and estado == "turno_blancas"):
            print("Esa pieza no es tuya, es el turno del " + estado + ".")
            validez_movimiento = False
        elif casilla_inicio == casilla_llegada:
            print("El origen y el destino son la misma casilla.")
            validez_movimiento = False
        elif self.pieza_en_casilla(casilla_llegada) != None and pieza.color == self.pieza_en_casilla(casilla_llegada).color:
            print("La casilla de destino está ocupada por una pieza propia.")
            validez_movimiento = False
        else:
            print(casilla_inicio, casilla_llegada)
            validez_movimiento: bool = casilla_llegada in pieza.movimientos_posibles(casilla_inicio, comp_jaque)

        return validez_movimiento

    # Metodo para comprobar si se ha coronado
    def comprobar_coronacion(self, casilla_llegada: str | None = None):
        if isinstance(casilla_llegada, Peon):
            self.colocar(Dama(self.pieza_en_casilla(casilla_llegada).color), casilla_llegada)
        else:
            for fila in [0, 7]:
                for columna in range(8):
                    casilla_a_comprobar: str = str(columna) + str(fila)
                    if isinstance(self.pieza_en_casilla(casilla_a_comprobar), Peon):
                        self.colocar(Dama(self.pieza_en_casilla(casilla_a_comprobar).color), casilla_a_comprobar)

# Creacion de la clase Peon
class Peon(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("peon", color)

    # Metodo para comprobar los movimientos posibles para una torre
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []

        # Determinacion del sentido hacia el cual el peon se debe dirigir dependiendo de su color
        if self.color == "blanco":
            peon_sentido: int = 1
        elif self.color == "negro":
            peon_sentido: int = -1

        # Comprobación de la casilla de en frente del peon
        casilla_a_comprobar = str(int(casilla) + 1*peon_sentido)
        if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
            casilla_a_comprobar = "0" + casilla_a_comprobar
        if tablero.existe_casilla(casilla_a_comprobar):
            if tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                casillas_mov_perm.append(casilla_a_comprobar)
                
                # Comprobación de la posibilidad del salto doble del peon en caso de que puede moverse un espacio hacia delante
                if casilla[1] in "16":
                    casilla_a_comprobar = str(int(casilla) + 2*peon_sentido)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if tablero.existe_casilla(casilla_a_comprobar):
                        if tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                            casillas_mov_perm.append(casilla_a_comprobar)

        # Comprobación de la posible captura del peon
        for i in [1, -1]:
            casilla_a_comprobar = str(int(casilla) + 1*peon_sentido + 10*i)
            if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                casilla_a_comprobar = "0" + casilla_a_comprobar
            if tablero.existe_casilla(casilla_a_comprobar):
                if tablero.pieza_en_casilla(casilla_a_comprobar) != None and tablero.pieza_en_casilla(casilla_a_comprobar).color != self.color:
                    casillas_mov_perm.append(casilla_a_comprobar)
        
        return casillas_mov_perm

# Creacion de la clase Caballo
class Caballo(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("caballo", color)

    # Metodo para comprobar los movimientos posibles para un caballo
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []
        for n in [1, -1]:
            for m in [1, -1]:
                for i in range(1, 3):
                    casilla_a_comprobar = str(int(casilla) + i*n + 10*(3-i)*m)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if tablero.existe_casilla(casilla_a_comprobar):
                        if tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                            casillas_mov_perm.append(casilla_a_comprobar)
                        elif tablero.pieza_en_casilla(casilla_a_comprobar).color != tablero.pieza_en_casilla(casilla).color:
                            casillas_mov_perm.append(casilla_a_comprobar)
        return casillas_mov_perm

# Creacion de la clase Alfil
class Alfil(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("alfil", color)

    # Metodo para comprobar los movimientos posibles para un alfil
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []
        for n in [1, -1]:
            for m in [1, -1]:
                for i in range(1, 8):
                    casilla_a_comprobar = str(int(casilla) + i*n + 10*i*m)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if not tablero.existe_casilla(casilla_a_comprobar):
                        break
                    elif tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    else:
                        if tablero.pieza_en_casilla(casilla_a_comprobar).color != tablero.pieza_en_casilla(casilla).color:
                            casillas_mov_perm.append(casilla_a_comprobar)
                        break
        return casillas_mov_perm

# Creacion de la clase Torre
class Torre(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("torre", color)

    # Metodo para comprobar los movimientos posibles para una torre
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []
        for n in [1, -1, 10, -10]:
            for i in range(1, 8):
                casilla_a_comprobar: str = str(int(casilla) + i*n)
                if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                    casilla_a_comprobar = "0" + casilla_a_comprobar
                if not tablero.existe_casilla(casilla_a_comprobar):
                    break
                elif tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                    casillas_mov_perm.append(casilla_a_comprobar)
                else:
                    if tablero.pieza_en_casilla(casilla_a_comprobar).color != tablero.pieza_en_casilla(casilla).color:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    break
        return casillas_mov_perm

# Creacion de la clase Dama
class Dama(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("dama", color)

    # Metodo para comprobar los movimientos posibles para una dama combinando las funciones de la torre y el alfil
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []
        dama_torre = Torre(self.color)
        dama_alfil = Alfil(self.color)
        casillas_mov_perm = dama_torre.movimientos_posibles(casilla, comp_jaque) + dama_alfil.movimientos_posibles(casilla, comp_jaque)
        return casillas_mov_perm

# Creacion de la clase Rey
class Rey(Pieza):

    def __init__(self, color: str) -> None:
        super().__init__("rey", color)

    # Metodo para comprobar los movimientos posibles para un rey
    def movimientos_posibles(self, casilla: str, comp_jaque: bool = True) -> list[str]:
        casillas_mov_perm: list[str] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                casilla_a_comprobar: str = str(int(casilla) + i + 10*j)
                if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                    casilla_a_comprobar = "0" + casilla_a_comprobar
                if tablero.existe_casilla(casilla_a_comprobar):
                    if tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    elif tablero.pieza_en_casilla(casilla_a_comprobar).color != tablero.pieza_en_casilla(casilla).color:
                        casillas_mov_perm.append(casilla_a_comprobar)
        return casillas_mov_perm

# Generacion del tablero inicial
tablero: Tablero = Tablero()

# Definicion de una funcion para alternar el turno
estado: str = "turno_blancas"

def _ejecutar_turno() -> None:

    global estado
    user_input: str = ""
    casilla_inicio: str = ""
    casilla_llegada: str = ""

    if estado == "turno_blancas":
        print("Turno de las blancas.")
    elif estado == "turno_negras":
        print("Turno de las negras.")
    user_input = input("Introduce un movimiento valido o escribe 'salir' para finalizar: ").lower()
    print("")

    if "salir" == user_input:
        estado = "fin_partida"
    elif len(user_input) == 5 and user_input[0] in letras_perm and user_input[1] in numeros_perm and user_input[2] == " " and user_input[3] in letras_perm and user_input[4] in numeros_perm:
        casilla_inicio = str(letras_perm.find(user_input[0])) + str(numeros_perm.find(user_input[1]))
        casilla_llegada = str(letras_perm.find(user_input[3])) + str(numeros_perm.find(user_input[4]))
        tablero.mover_pieza(casilla_inicio, casilla_llegada)
        print("")
        tablero.imprimir_tablero()
    else:
        print("Formato no valido. Escribe origen y destino, por ejemplo: e2 e4")

# Definicion de la maquina de estados
estado: str = "turno_blancas"
def _comenzar_partida():

    tablero.reiniciar()
    tablero.imprimir_tablero()
    global estado
    estado = "turno_blancas"
        
    while estado != "fin_partida":
        if estado == "turno_blancas":
            _ejecutar_turno()
            if estado != "fin_partida":
                estado = "turno_negras"
        elif estado == "turno_negras":
            _ejecutar_turno()
            if estado != "fin_partida":
                estado = "turno_blancas"
        
# Comienzo del programa
_comenzar_partida()