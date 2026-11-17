# ENTREGA 2
# Carlos Pujalte Beltrá


# Imports
import copy
import os


# Creación de una función que convierte una casilla a ID y viceversa.
letras_perm: str = "abcdefgh"
numeros_perm: str = "12345678"
def casilla_a_ID(casilla: str) -> str:
    """ Convierte una casilla de formato estandarizado (e2) a ID interno (31). """

    fila: str = casilla[1]
    columna: str = casilla[0]
    fila = str(numeros_perm.find(fila))
    columna = str(letras_perm.find(columna))
    return columna + fila


def ID_a_casilla(casilla: str) -> str:
    """ Convierte una casilla de ID interno (31) a formato estandarizado (e2). """

    fila: str = casilla[1]
    columna: str = casilla[0]
    fila = str(numeros_perm[int(fila)])
    columna = str(letras_perm[int(columna)])
    return columna + fila

# Creacion de la clase Pieza
class Pieza:

    # Diccionario con todos los unicode para su posterior asignacion.
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


    def __init__(self, nombre: str, color: str, tablero: "Tablero | None" = None) -> None:
        """ Genera una pieza y le atribuye su simbolo adecuado. Atribuirle un tablero es opcional. """

        self.nombre: str = nombre
        self.color: str = color
        self.simbolo: str = self.unicode_list_pieza.get(nombre[0].upper()+color[0].upper())
        self.tablero: Tablero = tablero


# Creacion de la clase Tablero
class Tablero:

    def __init__(self, partida: "Partida | None" = None) -> None:
        """ Genera el tablero y sus atributos. El tablero se genera completamente vacio. """

        self.casillas: list[list[Pieza | None]] = []
        self.partida: "Partida | None" = partida
        for i in range(8):
            fila_vacia: list[Pieza | None] = [None] * 8
            self.casillas.append(fila_vacia)
        self.reiniciar()

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


    def colocar(self, pieza: Pieza, casilla: str) -> None:
        """ Coloca una pieza en cierta casilla. """

        self.casillas[int(casilla[1])][int(casilla[0])] = pieza


    def pieza_en_casilla(self, casilla: str) -> Pieza | None:
        """ Devuelve la pieza en cierta casilla. """

        if self.casillas[int(casilla[1])][int(casilla[0])] != None:
            return self.casillas[int(casilla[1])][int(casilla[0])]
        else: return None


    def existe_casilla(self, casilla: str) -> bool:
        """ Devuelve un bool que indica si la casilla introducida esta dentro del tablero. """

        if casilla[0] in "01234567" and casilla[1] in "01234567":
            return True
        else:
            return False


    def imprimir_tablero(self) -> None:
        """ Imprime el tablero por pantalla. """

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


    def reiniciar(self) -> None:
        """ Devuelve el tablero a su posicion inicial. """

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
                self.colocar(clases_pieza[nombre](color, self), str(columna_a_colocar) + ["0", "7"][fila_a_colocar])
                columna_a_colocar += 1
            columna_a_colocar = 0

            for nombre in range(8):
                self.colocar(clases_pieza["peon"](color, self), str(columna_a_colocar) + ["1", "6"][fila_a_colocar])
                columna_a_colocar += 1
            columna_a_colocar = 0
            fila_a_colocar += 1


    def mover_pieza(self,
                    casilla_inicio: str,
                    casilla_llegada: str,
                    verificar_movimiento: bool = True,  # Si False, se salta todo el proceso de verificación del movimiento, actualmente no utilizado
                    ignorar_estado: bool = False,       # Variable para excluir el caso específico de la comprobación de la correspondencia del estado con el turno del jugador
                    indexar_movimiento: bool = False    # Indica si se debe guardar el movimiento en archivo txt
                    ) -> None:
        """ Mueve una pieza de una casilla a otra y permite activar y desactivar diferentes comprobaciones. """
        
        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)
        validez_movimiento: bool = True
        tablero_inicial = Tablero()
        tablero_inicial.casillas = copy.deepcopy(self.casillas)

        if verificar_movimiento == True:
            validez_movimiento = self.es_movimiento_valido(casilla_inicio, casilla_llegada, ignorar_estado)

        if validez_movimiento == True:
            self.colocar(pieza, casilla_llegada)
            self.colocar(None, casilla_inicio)
            if isinstance(pieza, Peon):
                self.comprobar_coronacion(casilla_llegada)

            if verificar_movimiento == True and self.comprobar_rey_en_jaque(pieza.color) == True:
                self.casillas = copy.deepcopy(tablero_inicial.casillas)
                raise ValueError("Ese movimiento deja a tu propio rey en jaque.")

            if indexar_movimiento == True:
                casilla_inicio_notacion: str = ID_a_casilla(casilla_inicio)
                casilla_llegada_notacion: str = ID_a_casilla(casilla_llegada)
                movimiento: str = casilla_inicio_notacion + " " + casilla_llegada_notacion
                self.partida.guardar_historial(movimiento, self.partida.ruta)


    def es_movimiento_valido(self, casilla_inicio: str, casilla_llegada: str, ignorar_estado: bool = False) -> bool:
        """ Comprueba diferentes condiciones necesarias para que el movimiento sea válido. """

        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)

        if pieza == None:
            raise ValueError("No hay ninguna pieza en la casilla de origen.")
        
        elif not ignorar_estado and ((pieza.color == "blanco" and self.partida.estado == "turno_negras") or (pieza.color == "negro" and self.partida.estado == "turno_blancas")):
            color_turno: str
            if self.partida.estado == "turno_blancas":
                color_turno = "blancas"
            elif self.partida.estado == "turno_negras":
                color_turno = "negras"
            raise ValueError("Esa pieza no es tuya, es el turno de las " + color_turno + ".")
        
        elif casilla_inicio == casilla_llegada:
            raise ValueError("El origen y el destino son la misma casilla.")
        
        elif self.pieza_en_casilla(casilla_llegada) != None and pieza.color == self.pieza_en_casilla(casilla_llegada).color:
            raise ValueError("La casilla de destino está ocupada por una pieza propia.")
        
        elif casilla_llegada not in pieza.movimientos_posibles(casilla_inicio):
            raise ValueError("Movimiento no valido para esta pieza (" + pieza.nombre + ").")

        else: return True


    def comprobar_coronacion(self, casilla_llegada: str | None = None) -> None:
        """ Si casilla_llegada esta vacio, comprueba todo el tablero para coronar. Si no, comprueba una casilla específica. """

        if isinstance(casilla_llegada, Peon):
            self.colocar(Dama(self.pieza_en_casilla(casilla_llegada).color), casilla_llegada)
        else:
            for fila in [0, 7]:
                for columna in range(8):
                    casilla_a_comprobar: str = str(columna) + str(fila)
                    if isinstance(self.pieza_en_casilla(casilla_a_comprobar), Peon):
                        self.colocar(Dama(self.pieza_en_casilla(casilla_a_comprobar).color), casilla_a_comprobar)


    def casilla_de_rey(self, color) -> str:
        """ Devuelve la casilla en la que se encuentra el rey de cierto color. """

        for fila in range(8):
            for columna in range(8):
                casilla_a_comprobar: str = str(columna) + str(fila)
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)
                if isinstance(pieza, Rey):
                    if pieza.color == color:
                        return(casilla_a_comprobar)


    def comprobar_rey_en_jaque(self, color) -> bool:
        """ Devuelve un bool que indica si el rey de cierto color esta en jaque. """
        
        color_rey_comprobacion: str = color
        color_piezas_amenaza: str
        casilla_rey: str = self.casilla_de_rey(color_rey_comprobacion)

        if color_rey_comprobacion == "blanco":
            color_piezas_amenaza = "negro"
        else:
            color_piezas_amenaza = "blanco"

        for fila in range(8):
            for columna in range(8):
                casilla_a_comprobar: str = str(columna) + str(fila)
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)
                if isinstance(pieza, Pieza):
                    if color_piezas_amenaza == pieza.color:
                        if casilla_rey in pieza.movimientos_posibles(casilla_a_comprobar):
                            return True     # Si la casilla del rey esta amenazada, se devuelve True

        return False    # En caso de no encontrar ninguna pieza que haga jaque, se devuelve False   


    def comprobar_rey_ahogado(self, color) -> bool:
        """ Devuelve un bool que indica si el rey de cierto color esta en jaque. """

        tablero_inicial = Tablero()
        tablero_inicial.casillas = copy.deepcopy(self.casillas)
        for fila in range(8):
            for columna in range(8):
                casilla_a_comprobar: str = str(columna) + str(fila)
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)

                if isinstance(pieza, Pieza):
                    if pieza.color == color:
                        movimientos_a_comprobar: list[str] = pieza.movimientos_posibles(casilla_a_comprobar)

                        for casilla_llegada in movimientos_a_comprobar:
                            try:
                                self.mover_pieza(casilla_a_comprobar, casilla_llegada, ignorar_estado = True)
                                self.casillas = copy.deepcopy(tablero_inicial.casillas)
                                return False
                            
                            except ValueError:
                                self.casillas = copy.deepcopy(tablero_inicial.casillas)
        return True


    def analizar_posicion_color(self, color: str) -> str:
        """ Devuelve "jaque", "jaque mate" o "rey ahogado" dependiendo de cómo se encuentra cierto color en el tablero. """

        jaque: bool = self.comprobar_rey_en_jaque(color)
        rey_ahogado: bool = self.comprobar_rey_ahogado(color)
        if jaque and rey_ahogado:
            return "jaque mate"
        elif jaque:
            return "jaque"
        elif rey_ahogado:
            return "rey ahogado"


# Creacion de la clase Peon
class Peon(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("peon", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto peon. """

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
        if self.tablero.existe_casilla(casilla_a_comprobar):
            if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                casillas_mov_perm.append(casilla_a_comprobar)
                
                # Comprobación de la posibilidad del salto doble del peon en caso de que puede moverse un espacio hacia delante
                if casilla[1] in "16":
                    casilla_a_comprobar = str(int(casilla) + 2*peon_sentido)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if self.tablero.existe_casilla(casilla_a_comprobar):
                        if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                            casillas_mov_perm.append(casilla_a_comprobar)

        # Comprobación de la posible captura del peon
        for i in [1, -1]:
            casilla_a_comprobar = str(int(casilla) + 1*peon_sentido + 10*i)
            if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                casilla_a_comprobar = "0" + casilla_a_comprobar
            if self.tablero.existe_casilla(casilla_a_comprobar):
                if self.tablero.pieza_en_casilla(casilla_a_comprobar) != None and self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.color:
                    casillas_mov_perm.append(casilla_a_comprobar)
        
        return casillas_mov_perm


# Creacion de la clase Caballo
class Caballo(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("caballo", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto caballo. """

        casillas_mov_perm: list[str] = []
        for n in [1, -1]:
            for m in [1, -1]:
                for i in range(1, 3):
                    casilla_a_comprobar = str(int(casilla) + i*n + 10*(3-i)*m)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if self.tablero.existe_casilla(casilla_a_comprobar):
                        if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                            casillas_mov_perm.append(casilla_a_comprobar)
                        elif self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                            casillas_mov_perm.append(casilla_a_comprobar)
        return casillas_mov_perm


# Creacion de la clase Alfil
class Alfil(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("alfil", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto alfil. """

        casillas_mov_perm: list[str] = []
        for n in [1, -1]:
            for m in [1, -1]:
                for i in range(1, 8):
                    casilla_a_comprobar = str(int(casilla) + i*n + 10*i*m)
                    if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                        casilla_a_comprobar = "0" + casilla_a_comprobar
                    if not self.tablero.existe_casilla(casilla_a_comprobar):
                        break
                    elif self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    else:
                        if self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                            casillas_mov_perm.append(casilla_a_comprobar)
                        break
        return casillas_mov_perm


# Creacion de la clase Torre
class Torre(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("torre", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierta torre. """
        
        casillas_mov_perm: list[str] = []
        for n in [1, -1, 10, -10]:
            for i in range(1, 8):
                casilla_a_comprobar: str = str(int(casilla) + i*n)
                if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                    casilla_a_comprobar = "0" + casilla_a_comprobar
                if not self.tablero.existe_casilla(casilla_a_comprobar):
                    break
                elif self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                    casillas_mov_perm.append(casilla_a_comprobar)
                else:
                    if self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    break
        return casillas_mov_perm


# Creacion de la clase Dama
class Dama(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("dama", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierta dama. """
        
        casillas_mov_perm: list[str] = []

        # Genera una torre y un alfil auxiliares para simular el movimiento de una dama.
        dama_torre = Torre(self.color, self.tablero)
        dama_alfil = Alfil(self.color, self.tablero)

        casillas_mov_perm = dama_torre.movimientos_posibles(casilla) + dama_alfil.movimientos_posibles(casilla)
        return casillas_mov_perm


# Creacion de la clase Rey
class Rey(Pieza):

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        super().__init__("rey", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto rey. """

        casillas_mov_perm: list[str] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                casilla_a_comprobar: str = str(int(casilla) + i + 10*j)
                if len(casilla_a_comprobar) == 1 and int(casilla_a_comprobar) >= 0:
                    casilla_a_comprobar = "0" + casilla_a_comprobar
                if self.tablero.existe_casilla(casilla_a_comprobar):
                    if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:
                        casillas_mov_perm.append(casilla_a_comprobar)
                    elif self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                        casillas_mov_perm.append(casilla_a_comprobar)
        return casillas_mov_perm

# Creacion de la clase Partida
class Partida:

    def __init__(self, ruta: str = "partida.txt") -> None:
        """ Definicion de los atributos de la clase Partida. La ruta se establece por defecto a "partida.txt". """

        self.movimientos: list[str] = []
        self.estado: str = "turno_blancas"
        self.tablero = Tablero(self)
        self.ruta = ruta             # La ruta esta hardcodeada por los requisitos de la entrega, pero la pongo como atributo para poder cambiarla facilmente


    def reiniciar(self) -> None:
        """ Devuelve tanto el estado del tablero como el resto de variables intrinsecas de la partida a su estado inicial. """
        
        self.movimientos = []
        self.estado = "turno_blancas"
        self.tablero.reiniciar()


    def comenzar_partida(self) -> None:
        """ Pone en marcha la máquina de estados. """

        self.tablero.imprimir_tablero()
        color_estado: str = ""
        nombre_estado: str = ""
        nombre_opuesto: str = ""
            
        while self.estado != "fin_partida":

            if self.estado == "turno_blancas":
                color_estado = "blanco"
                nombre_estado = "blancas"
                nombre_opuesto = "negras"
            elif self.estado == "turno_negras":
                color_estado = "negro"
                nombre_estado = "negras"
                nombre_opuesto = "blancas"

            posicion_estado: str = self.tablero.analizar_posicion_color(color_estado)
            if posicion_estado == "jaque":
                print("Jaque a las " + nombre_estado + ".")
            elif posicion_estado == "jaque mate":
                print("Jaque mate. Ganan las " + nombre_opuesto + ", fin de la partida.")
                self.estado = "fin_partida"
            elif posicion_estado == "rey ahogado":
                print("Rey ahogado a las " + nombre_estado + ", fin de la partida.")
                self.estado = "fin_partida"
            
            if self.estado == "turno_blancas":
                print("Turno de las blancas.")

                try:    
                    self.ejecutar_turno()

                    if self.estado == "turno_blancas":
                        self.estado = "turno_negras"

                except ValueError as error:
                    print(error)

            elif self.estado == "turno_negras":
                print("Turno de las negras.")

                try:
                    self.ejecutar_turno()

                    if self.estado == "turno_negras":
                        self.estado = "turno_blancas"

                except ValueError as error:
                    print(error)


    def ejecutar_turno(self) -> bool | str:
        """ Pregunta al jugador por el movimiento y comprueba que es válida la sintaxis del input. """

        user_input: str = ""
        casilla_inicio: str = ""
        casilla_llegada: str = ""

        user_input = input("Introduce un movimiento valido o escribe 'salir' para finalizar: ").lower()
        print("")

        if "salir" == user_input:
            self.estado = "fin_partida"

        elif len(user_input) == 5 and user_input[0] in letras_perm and user_input[1] in numeros_perm and user_input[2] == " " and user_input[3] in letras_perm and user_input[4] in numeros_perm:
            casilla_inicio = casilla_a_ID(user_input[0:2])
            casilla_llegada = casilla_a_ID(user_input[3:5])
            self.tablero.mover_pieza(casilla_inicio, casilla_llegada, indexar_movimiento = True)
            print("")
            self.tablero.imprimir_tablero()

        else:
            raise ValueError("Formato no valido. Escribe origen y destino, por ejemplo: e2 e4")


    def cargar_historial(self, ruta: str) -> None:
        """ Busca el archivo seleccionado e intenta cargar la partida """

        numero_movimientos: int = 0
        with open(ruta, "r") as archivo:
            movimientos: list[str] = archivo.readlines()
            
            for movimiento in movimientos:
                movimiento = movimiento.strip("\n")

                if len(movimiento) == 5 and movimiento[0] in letras_perm and movimiento[1] in numeros_perm and movimiento[2] == " " and movimiento[3] in letras_perm and movimiento[4] in numeros_perm:
                    casilla_inicio = casilla_a_ID(movimiento[0:2])
                    casilla_llegada = casilla_a_ID(movimiento[3:5])

                    try:
                        self.tablero.mover_pieza(casilla_inicio, casilla_llegada, ignorar_estado = True, indexar_movimiento = True)
                        numero_movimientos += 1

                        if numero_movimientos % 2 == 0:
                            posicion_blancas: str = self.tablero.analizar_posicion_color("blanco")
                            if posicion_blancas == "jaque mate" or posicion_blancas == "rey ahogado":
                                print("La partida cargada ya ha finalizado. Comenzando partida nueva.\n")
                                self.reiniciar()
                                return

                        else:
                            posicion_negras: str = self.tablero.analizar_posicion_color("negro")
                            if posicion_negras == "jaque mate" or posicion_negras == "rey ahogado":
                                print("La partida cargada ya ha finalizado. Comenzando partida nueva.\n")
                                self.reiniciar()
                                return
                        
                    except ValueError:
                        print("El archivo guardado no es válido.\n")
                        self.reiniciar()
                        break

                else:
                    print("El archivo guardado no es válido.\n")
                    self.reiniciar()
                    break

        if numero_movimientos % 2 == 0:
            self.estado = "turno_blancas"
        else:
            self.estado = "turno_negras"


    def guardar_historial(self, movimiento: str, ruta: str) -> None:
        """ Guarda cierto movimiento en la lista del historial de la partida y actualiza el archivo txt correspondiente. """

        self.movimientos.append(movimiento)
        with open(ruta, "w") as archivo:
            for movimiento in self.movimientos:
                archivo.write(movimiento + "\n")


    def iniciar_juego(self) -> None:
        """ Comprueba que el archivo existe y pregunta por la continuacion de la partida. """

        ruta: str = self.ruta
        if os.path.exists(ruta):

            user_input: str = input("Se ha detectado una partida existente. Si desea cargarla, introduzca 's': ").lower()
            if user_input == "s":
                self.cargar_historial(ruta)
                partida_main.comenzar_partida()

            else:
                partida_main.comenzar_partida()

        else:
            partida_main.comenzar_partida()


# Comienzo de la partida
partida_main = Partida()
partida_main.iniciar_juego()