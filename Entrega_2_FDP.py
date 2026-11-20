# ENTREGA 2
# Carlos Pujalte Beltrá


# Imports
import copy
import os
import csv


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


def reparar_columna_casilla(casilla: str) -> str:
    """ Añade un 0 al inicio de la casilla en caso de que tras una conversion de 'int' a 'str' se haya perdido. """

    # Esta funcion se utiliza especialmente dentro de los metodos "movimientos_posibles" para la clase "Pieza" al buscar casillas relativas a otras mediante operaciones algebraicas con int
    if len(casilla) == 1 and int(casilla) >= 0:     # Filtra el caso en el que la casilla queda como numero de un digito (como "03", que pasaria a "3"), ya que al sumarlo en int se pierde el 0 y se le debe de añadir al reconvertirlo a str
        return "0" + casilla                        # Si esta mal, se devuelve la casilla con un 0 adicional
    else:
        return casilla                              # Si esta bien, simplemente se devuelve la casilla inicial


class Pieza:
    """ Representa una pieza en el tablero. Se divide en subclases dependiendo del tipo de pieza que es. """

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
        self.simbolo: str = self.unicode_list_pieza.get(nombre[0].upper()+color[0].upper())     # Automaticamente le asigna el simbolo adecuado a la pieza, puesto que toda su informacion ya viene dada por su color y su nombre
        self.tablero: "Tablero | None" = tablero                                                # Opcionalmente se le puede atribuir el argumento del tablero al que pertenece, util para poder crear piezas auxiliares (comprobacion de la dama)


# Creacion de la clase Tablero
class Tablero:
    """ Representa el tablero de una partida, guardando la informacion de sus casillas y de su partida de origen. """

    def __init__(self, partida: "Partida | None" = None) -> None:
        """ Genera el tablero y sus atributos. El tablero se genera completamente vacio. """

        self.casillas: list[list[Pieza | None]] = []
        self.partida: "Partida | None" = partida                # Atributo auxiliar, la partida a la que pertenece, dando margen para crear tableros auxiliares para guardar estados pasados de la partida al simular movimientos (comprobacion de rey ahogado)

        for i in range(8):                                      # Genera 8 filas vacias en un primer lugar
            fila_vacia: list[Pieza | None] = [None] * 8
            self.casillas.append(fila_vacia)
        self.reiniciar()                                        # Luego rellena esas 8 filas "reiniciando" el tablero

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

        Las unidades representan la fila mientras que las decenas representan la columna.
        Si se quiere comprobar una casilla relativa a otra, solo hace falta sumarle un n*1 para las filas y un m*10 para las columnas al ID de la casilla inicial.

        Es recurrente ver en ciertas funciones algo como 'self.casillas[int(casilla[1])][int(casilla[0])]'.
        Como self.casillas es una lista de listas, se puede acceder a los contenidos de cualquier casilla con su ID facilmente, puesto que lleva codificado su fila y su columna,
        donde [int(casilla[1])] representa el numero de la fila y [int(casilla[0])] el numero de la columna.
        """


    def colocar(self, pieza: Pieza | None, casilla: str) -> None:
        """ Coloca una pieza en cierta casilla. """

        self.casillas[int(casilla[1])][int(casilla[0])] = pieza


    def pieza_en_casilla(self, casilla: str) -> Pieza | None:
        """ Devuelve la pieza que se encuentra en cierta casilla. """

        if self.casillas[int(casilla[1])][int(casilla[0])] != None:
            return self.casillas[int(casilla[1])][int(casilla[0])]
        else:
            return None


    def existe_casilla(self, casilla: str) -> bool:
        """ Devuelve un bool que indica si la casilla introducida esta dentro del tablero. """

        if casilla[0] in "01234567" and casilla[1] in "01234567":
            return True
        else:
            return False


    def imprimir_tablero(self) -> None:
        """ Imprime el tablero por pantalla. """

        for i in range(8):

            if i == 0:
                print("   A B C D E F G H")

            print(8-i, end = "  ")                  # Imprime el número inicial
            for j in self.casillas[7-i]:            # Puesto que realmente la fila 0 en una lista de listas (self.casillas) es la superior, se debe de empezar a imprimir por la fila 7 (8 en notacion normal). De ahí el [7-i], ya que i comienza en 0.
                contenido: Pieza | None = j

                if isinstance(contenido, Pieza):    # Se filtra el caso en el que la casilla esta vacia, puesto que "None" no tiene atributos y daria error al buscar contenido.simbolo
                    contenido = contenido.simbolo

                else:                               # Caso de la casilla
                    contenido = "."

                print(contenido, end = " ")
            print("")
        print("")


    def reiniciar(self) -> None:
        """ Devuelve el tablero a su posicion inicial. """

        for i in range(8):                      # Devuelve el tablero a todo casillas en blanco
            for j in range(8):
                self.casillas[i][j] = None

        fila_a_colocar: int = 0
        columna_a_colocar: int = 0

        clases_pieza: dict[str, Pieza] = {      # Diccionario auxiliar para trabajar con clase str en lugar de clase Pieza
            "peon": Peon,
            "caballo": Caballo,
            "alfil": Alfil,
            "torre": Torre,
            "dama": Dama,
            "rey": Rey
        }

        for color in ["blanco", "negro"]:

            for nombre in ["torre", "caballo", "alfil", "dama", "rey", "alfil", "caballo", "torre"]:                        # Imprime las filas 1 y 8 (notacion normal), las filas traseras.
                self.colocar(clases_pieza[nombre](color, self), str(columna_a_colocar) + ["0", "7"][fila_a_colocar])        # Primer argumento: "clases_pieza[nombre]" determina la subclase de pieza, "(color, self)" son sus atributos, con self siendo el tablero al que pertenece.
                                                                                                                            # Segundo argumento: "str(columna_a_colocar)" determina la columna, sumando uno tras cada pieza,
                                                                                                                            #                    "["0", "7"][fila_a_colocar]" selecciona forzadamente las filas dependiendo del color, con 0 siendo blancas y 7 negras
                columna_a_colocar += 1
            columna_a_colocar = 0

            for nombre in range(8):                                                                                         # Imprime las filas 2 y 7 (notacion normal), las filas de peones. (Procedimiento análogo al anterior)
                self.colocar(clases_pieza["peon"](color, self), str(columna_a_colocar) + ["1", "6"][fila_a_colocar])        # Se fuerza a peon la pieza a colocar con ["peon"]
                columna_a_colocar += 1
            columna_a_colocar = 0
            fila_a_colocar += 1


    def mover_pieza(self,
                    casilla_inicio: str,
                    casilla_llegada: str,
                    verificar_movimiento: bool = True,          # Si False, se salta todo el proceso de verificación del movimiento, incluyendo el jaque a uno mismo
                    ignorar_estado: bool = False,               # Variable para excluir el caso específico de la comprobacion de la correspondencia del estado con el turno del jugador dentro del metodo "es_movimiento_valido"
                    forzar_comprobacion_jaque: bool = False,    # Fuerza la comprobacion de jaque a uno mismo tras el movimiento con prioridad sobre el argumento "verificar_movimiento"
                    indexar_movimiento: bool = False            # Indica si se debe guardar el movimiento en archivo txt
                    ) -> None:
        """ Mueve una pieza de una casilla a otra y permite activar y desactivar diferentes comprobaciones. """
        
        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)
        validez_movimiento: bool = True
        tablero_inicial: Tablero = Tablero()
        tablero_inicial.casillas = copy.deepcopy(self.casillas)         # Se crea una copia de las casillas del tablero en caso de que haya que restablecerlo a su estado inicial tras un movimiento no válido

        if verificar_movimiento == True:                                # Comprueba inicialmente si es necesario pasar por todo el proceso de validacion
            validez_movimiento = self.es_movimiento_valido(casilla_inicio, casilla_llegada, ignorar_estado)

        if validez_movimiento == True:                                                                  # Comienza a ejecutarse el movimiento tras las comprobaciones
            self.colocar(pieza, casilla_llegada)                                                        # Se coloca la pieza en la casilla de destino, independientemente de lo que haya, naturalmente capturando si se da el caso
            self.colocar(None, casilla_inicio)                                                          # Se remplaza la casilla inicial con una casilla vacia

            if isinstance(pieza, Peon):                                                                 # Si la pieza movida es un peon, se comprueba si ha coronado
                self.comprobar_coronacion(casilla_llegada)

            if forzar_comprobacion_jaque or verificar_movimiento:
                if self.comprobar_rey_en_jaque(pieza.color) == True:                                    # Comprobacion de que el movimiento no ha dejado al rey propio en jaque tras haber movido
                    self.casillas = copy.deepcopy(tablero_inicial.casillas)                             # Si sí que deja al rey propio en jaque, el tablero se restablece a su estado inicial
                    raise ValueError("Ese movimiento deja a tu propio rey en jaque.")                   # Tras restablecer el tablero, se manda un mensaje de error

            if indexar_movimiento == True:                                                              # Proceso de guardado del movimiento en archivo.txt
                casilla_inicio_notacion: str = ID_a_casilla(casilla_inicio)
                casilla_llegada_notacion: str = ID_a_casilla(casilla_llegada)
                movimiento: str = casilla_inicio_notacion + " " + casilla_llegada_notacion              # Se reconstruye el movimiento mandado por el usuario inicialmente (es decir, se transforma a formato "e2 e4")
                self.partida.guardar_historial(movimiento, self.partida.ruta_txt)                       # Se manda el movimiento a guardar


    def es_movimiento_valido(self,
                             casilla_inicio: str,
                             casilla_llegada: str,
                             ignorar_estado: bool = False
                             ) -> bool:
        """ Comprueba diferentes condiciones necesarias para que el movimiento sea válido. """

        pieza: Pieza | None = self.pieza_en_casilla(casilla_inicio)

        if casilla_inicio == casilla_llegada:
            """ Error de casillas de inicio y llegada idénticas """
            raise ValueError("El origen y el destino son la misma casilla.")
    
        elif pieza == None:
            """ Error de casilla inicial vacia """
            raise ValueError("No hay ninguna pieza en la casilla de origen.")
        
        elif not ignorar_estado and ((pieza.color == "blanco" and self.partida.estado == "turno_negras") or (pieza.color == "negro" and self.partida.estado == "turno_blancas")):   # ignorar_estado se utiliza en simulaciones de movimientos como comprobaciones de jaque globales
            """ Error de intento de mover pieza del oponente """
            color_turno: str

            if self.partida.estado == "turno_blancas":      # If auxiliar para escribir el mensaje de error correcto despues
                color_turno = "blancas"
            elif self.partida.estado == "turno_negras":
                color_turno = "negras"

            raise ValueError("Esa pieza no es tuya, es el turno de las " + color_turno + ".")
        
        elif self.pieza_en_casilla(casilla_llegada) != None and pieza.color == self.pieza_en_casilla(casilla_llegada).color:        # Primero comprueba que la casilla no este vacia, y luego busca el atributo "color" de la pieza para evitar errores
            """ Error de captura a pieza propia """
            raise ValueError("La casilla de destino está ocupada por una pieza propia.")
        
        elif casilla_llegada not in pieza.movimientos_posibles(casilla_inicio):
            """ Error de movimiento no valido por las reglas de movimiento de las piezas, exceptuando jaque a uno mismo """
            raise ValueError("Movimiento no valido para esta pieza (" + pieza.nombre + ").")

        else: return True       # Si todas las comprobaciones dan negativo, se devuelve True


    def comprobar_coronacion(self, casilla_llegada: str | None = None) -> None:
        """ Si casilla_llegada esta vacio, comprueba todo el tablero para coronar. Si no, comprueba una casilla específica. """

        # Caso 1: Se ha introducido una casilla especifica
        if isinstance(self.pieza_en_casilla(casilla_llegada), Peon) and casilla_llegada[1] in ["0", "7"]:               # Se comprueba que la pieza es peon (por si acaso se ha introducido una pieza diferente) y esta en las ultimas filas
            self.colocar(Dama(self.pieza_en_casilla(casilla_llegada).color, self), casilla_llegada)                           # Se remplaza el peon con una dama mediante "self.colocar"

        # Caso 2: No se ha introducido una casilla especifica
        else:
            for fila in [0, 7]:                                                                                         # Recorre las 2 ultimas filas enteras y comprueba casilla a casilla que no hay un peon
                for columna in range(8):
                    casilla_a_comprobar: str = str(columna) + str(fila)                                                 # Construccion de la casilla adecuada a comprobar

                    if isinstance(self.pieza_en_casilla(casilla_a_comprobar), Peon):
                        self.colocar(Dama(self.pieza_en_casilla(casilla_a_comprobar).color, self), casilla_a_comprobar)       # Remplazo de la pieza por dama


    def casilla_de_rey(self, color: str) -> str:
        """ Devuelve la casilla en la que se encuentra el rey de cierto color. """

        for fila in range(8):
            for columna in range(8):                                                    # Comprueba casilla a casilla todo el tablero

                casilla_a_comprobar: str = str(columna) + str(fila)                     # Definicion del ID de la casilla que va a ser comprobada
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)

                if isinstance(pieza, Rey):                                              # Comprueba que es rey
                    if pieza.color == color:                                            # Comprueba que el color del rey corresponde con el introducido inicialmente
                        return(casilla_a_comprobar)


    def comprobar_rey_en_jaque(self, color: str) -> bool:
        """ Devuelve un bool que indica si el rey de cierto color esta en jaque. """
        
        color_rey_comprobacion: str = color                                                     # Color del jugador cuyo rey se quiere comprobar si esta en jaque
        color_piezas_amenaza: str
        casilla_rey: str = self.casilla_de_rey(color_rey_comprobacion)                          # Se le asigna a una variable el ID de la casilla en la que se encuentra el rey del color establecido

        if color_rey_comprobacion == "blanco":                                                  # Asignacion del color del oponente para comprobar unicamente en las piezas opuestas si hacen jaque al rey establecido o no
            color_piezas_amenaza = "negro"
        else:
            color_piezas_amenaza = "blanco"

        for fila in range(8):
            for columna in range(8):                                                            # Va casilla por casilla comprobando si la pieza en ella hace jaque al rey

                casilla_a_comprobar: str = str(columna) + str(fila)                             # Se establece la casilla que va a ser revisada
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)
                                                                                                # Considero favorable hacer una torre con 3 "if" uno detrás de otro en lugar de una cadena de "and" para poder discernir mejor las condiciones de cada paso a simple vista
                if isinstance(pieza, Pieza):                                                    # Se filtra el caso en el cual la casilla esta vacia
                    if color_piezas_amenaza == pieza.color:                                     # Se comprueba que la pieza cuyos movimientos van a ser calculados es del bando contrario
                        if casilla_rey in pieza.movimientos_posibles(casilla_a_comprobar):      # Se comprueba si la casilla del rey se encuentra en las casillas amenazadas por una pieza rival
                            return True                                                         # Si la casilla del rey esta amenazada, se devuelve True

        return False                                                                            # En caso de no encontrar ninguna pieza que haga jaque, es decir, el bucle ha finalizado y no se ha dado True, entonces se devuelve False   


    def comprobar_rey_ahogado(self, color: str) -> bool:
        """ Devuelve un bool que indica si el rey de cierto color esta en rey ahogado. """

        # El metodo simula los movimientos posibles de todas las piezas de un bando.
        # Si se encuentra un movimiento favorable, no hay rey ahogado por ende, el metodo deja de comprobar movimientos y se devuelve False.
        # Si, por otro lado, no encuentra un movimiento posible, hay rey ahogado y se devuelve True.

        tablero_inicial: Tablero = Tablero()
        tablero_inicial.casillas = copy.deepcopy(self.casillas)                                                     # Se crea un tablero auxiliar para guardar el estado inicial del tablero

        for fila in range(8):
            for columna in range(8):                                                                                # Se recorre el tablero casilla a casilla

                casilla_a_comprobar: str = str(columna) + str(fila)
                pieza: Pieza | None = self.pieza_en_casilla(casilla_a_comprobar)                                    # Se definen variables con la casilla que se va a comprobar y la pieza en esa casilla

                if isinstance(pieza, Pieza):                                                                        # Se filtra el caso en el que la casilla esta vacia
                    if pieza.color == color:                                                                        # Se comprueba que la pieza es del color del cual se quiere comprobar el rey ahogado
                        movimientos_a_comprobar: list[str] = pieza.movimientos_posibles(casilla_a_comprobar)        # Lista con todas las casillas a las que se puede mover la pieza seleccionada

                        for casilla_llegada in movimientos_a_comprobar:                                             # Recorre esa lista con todas las casillas de llegada posibles, saltando la pieza si la lista esta vacia (porque no se puede mover)

                            try:
                                self.mover_pieza(casilla_a_comprobar, casilla_llegada, verificar_movimiento = False, forzar_comprobacion_jaque = True)      # Prueba a mover esa pieza y comprueba si ese movimiento genera un jaque a uno mismo
                                self.casillas = copy.deepcopy(tablero_inicial.casillas)                                                                     # Si el movimiento se ha ejecutado correctamente, se restablece el tablero a su estado inicial para no corromperlo
                                return False                                                                                                                # Se devuelve false directamente para evitar que el programa siga comprobando movimientos: con 1 posible basta
                            
                            except ValueError:
                                self.casillas = copy.deepcopy(tablero_inicial.casillas)                                                                     # Si se da error por jaque a uno mismo, se devuelve el tablero a su estado inicial y sigue comprobando movimientos

        return True                                                                                                 # Si, tras comprobar todos los movimientos, no hay ninguno favorable o no hay movimientos posibles, hay rey ahogado y se devuelve True 


    def analizar_posicion_color(self, color: str) -> str | None:
        """ Devuelve "jaque", "jaque mate" o "rey ahogado" dependiendo de cómo se encuentra cierto color en el tablero. """

        jaque: bool = self.comprobar_rey_en_jaque(color)
        rey_ahogado: bool = self.comprobar_rey_ahogado(color)       # Variables que simplemente comprueban si hay jaque o rey ahogado y lo almacenan en un bool

        if jaque and rey_ahogado:           # El jaque mate se puede definir como la combinacion de jaque y rey ahogado, puesto que si el rey esta en jaque y no hay ningún movimiento legal (rey ahogado), entonces ha perdido por definicion (jaque mate)
            return "jaque mate"
        
        elif jaque:
            return "jaque"
        
        elif rey_ahogado:
            return "rey ahogado"


# Creacion de la clase Peon
class Peon(Pieza):
    """ Representa un peon blanco o negro en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Peon derivados de Pieza. """
        super().__init__("peon", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto peon. """

        casillas_mov_perm: list[str] = []
        casilla_a_comprobar: str = ""

        """ Determinacion del sentido hacia el cual el peon se debe dirigir dependiendo de su color """
        if self.color == "blanco":      # Si el peon es blanco, se dirige hacia el norte del tablero (sentido positivo de las filas)
            peon_sentido: int = 1
        elif self.color == "negro":     # Si es negro, se dirige hacia el sur (sentido negativo de las filas)
            peon_sentido: int = -1


        """ Comprobación de la casilla de en frente del peon """
        casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + 1*peon_sentido))                   # Se le suma (o resta, dependiendo del color) 1 a la fila de la casilla del peon

        if self.tablero.existe_casilla(casilla_a_comprobar):                                                # Se comprueba si la casilla se encuentra dentro del tablero de manera redundante,
                                                                                                            # puesto que en una partida ordinaria ya habria coronado si ha llegado a la ultima fila,
                                                                                                            # pero se mantiene para evitar IndexError en casos degenerados no convencionales en partidas normales.
            if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:                                  # Solo se añade la casilla a los movimientos posibles si esta vacia, puesto que un peon no puede capturar delante
                casillas_mov_perm.append(casilla_a_comprobar)
                
                """ Comprobación de la posibilidad del salto doble del peon en caso de que puede moverse un espacio hacia delante """
                if casilla[1] in "16":                                                                      # Comprueba si el peon se encuentra en una de las filas iniciales, de manera que puede dar doble salto
                    casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + 2*peon_sentido))       # Se encuentra la casilla del avance doble
                                                                                                            # Se hace este caso tras la comprobacion del avance unico ya que el peon podria saltar piezas en el doble movimiento en caso contrario
                    if self.tablero.existe_casilla(casilla_a_comprobar):                                    # Filtra el caso en el que un peon del un bando se encuentra en la fila de inicial de los peones del bando contrario, dando un doble salto a una casilla fuera del tablero

                        if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:                      # Al igual que el salto unico, solo se permite el movimiento si la casilla esta vacia, sin capturas
                            casillas_mov_perm.append(casilla_a_comprobar)


        """ Comprobación de la posible captura del peon """
        for i in [1, -1]:                                                                                   # Comprueba las casillas diagonales al peon enfrente: primero una fila este y luego otra oeste
            casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + 1*peon_sentido + 10*i))        # Encuentra las primeras casillas diagonales relativas a la casilla de inicio
                                                                                                            # "+ 1*peon_sentido" mueve la posicion a la siguiente fila
                                                                                                            # "+ 10*i" mueve la posicion a las columnas adyacentes

            if self.tablero.existe_casilla(casilla_a_comprobar):                                            # Comprueba que la casilla no sale fuera del tablero

                if self.tablero.pieza_en_casilla(casilla_a_comprobar) != None and self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.color:   # Solo permite el movimiento si la casilla de destino tiene una pieza; no puede estar vacia en la captura
                    casillas_mov_perm.append(casilla_a_comprobar)
        
        return casillas_mov_perm


# Creacion de la clase Caballo
class Caballo(Pieza):
    """ Representa un caballo blanco o negro en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Caballo derivados de Pieza. """
        super().__init__("caballo", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto caballo. """

        # Sabemos 2 normas que permiten definir el movimiento del caballo de manera no ambigua:
        # 1 - La suma de las diferencias vertical y horizontal de la casilla del caballo respecto a su casilla de destino debe sumar 3.
        # 2 - No obstante, el caballo podria moverse 3 casillas en una direccion en concreto, por lo que hace falta restringir esa posibilidad diciendo que las diferencias tanto vertical como horizontal deben ser o 1 o 2, pero no 3:
        """
        C: Caballo
        *: Casilla no apta segun las normas
        X: Casilla apta segun las normas

        Solo Norma 1:           Norma 1 y Norma 2:
        * * * X * * *           * * * * * * *
        * * X * X * *           * * X * X * *
        * X * * * X *           * X * * * X *
        X * * C * * X           * * * C * * *
        * X * * * X *           * X * * * X *
        * * X * X * *           * * X * X * *
        * * * X * * *           * * * * * * *
        """

        casillas_mov_perm: list[str] = []
        casilla_a_comprobar: str = ""

        for polaridad_vert in [1, -1]:                           # Comprueba primero la mitad superior del tablero y luego la inferior respecto al caballo
            for polaridad_horiz in [1, -1]:                      # En cada uno de los dos ciclos formados por el for anterior, comprueba individualmente la mitad derecha y luego la mitad izquierda, dejando 4 cuadrantes totales

                for diferencia in range(1, 3):      # Norma 2: Primero comprueba diferencia 1 y luego diferencia 2, pero no 3

                    casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + diferencia * polaridad_vert + 10 * (3 - diferencia) * polaridad_horiz))

                    # Norma 1: "diferencia" y "(3 - diferencia)" hacen que si la diferencia vertical es 1, la horizontal sea 2 y viceversa, es decir, suman 3
                    if self.tablero.existe_casilla(casilla_a_comprobar):                    # Si la casilla esta dentro del tablero, continua la comprobacion

                        if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:      # Filtra el caso en el que la casilla de llegada esta vacia para evitar errores
                            casillas_mov_perm.append(casilla_a_comprobar)

                        elif self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:      # Comprueba que la pieza en la casilla de llegada es del color opuesto para poder capturarla
                            casillas_mov_perm.append(casilla_a_comprobar)

        return casillas_mov_perm


# Creacion de la clase Alfil
class Alfil(Pieza):
    """ Representa un alfil blanco o negro en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Alfil derivados de Pieza. """
        super().__init__("alfil", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto alfil. """

        casillas_mov_perm: list[str] = []
        casilla_a_comprobar: str = ""

        for polaridad_vert in [1, -1]:                  # Comprueba primero la mitad superior del tablero y luego la inferior respecto al alfil
            for polaridad_horiz in [1, -1]:             # En cada uno de los dos ciclos formados por el for anterior, comprueba individualmente la mitad derecha y luego la mitad izquierda

                for desplazamiento in range(1, 8):      # Incrementa progresivamente el desplazamiento en cierta direccion y sentido

                    # Simula el desplazamiento de la pieza en una misma cantidad en el eje vertical y el horizontal
                    casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + desplazamiento * polaridad_vert + 10 * desplazamiento * polaridad_horiz))

                    if not self.tablero.existe_casilla(casilla_a_comprobar):            # Si la casilla se sale del tablero, debe dejar de comprobar en esa direccion y pasar a la siguiente
                        break

                    elif self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:    # Si la casilla esta libre, debe seguir incrementando el desplazamiento en esa direccion
                        casillas_mov_perm.append(casilla_a_comprobar)

                    else:                                                               # Si se llega a este caso, se ha encontrado una pieza en el camino, por lo que el ciclo debe detenerse
                        if self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                            casillas_mov_perm.append(casilla_a_comprobar)               # Comprueba si la pieza con la que se ha encontrado es del mismo color o no para saber si permitir la captura
                        break                                                           # Pueda capturar la pieza o no, se detiene la comprobacion en esa direccion

        return casillas_mov_perm


# Creacion de la clase Torre
class Torre(Pieza):
    """ Representa una torre blanca o negra en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Torre derivados de Pieza. """
        super().__init__("torre", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierta torre. """
        
        casillas_mov_perm: list[str] = []
        casilla_a_comprobar: str = ""

        for direccion in [1, -1, 10, -10]:          # Cicla las 4 direcciones cardinales, hacia las que se puede mover la torre

            for desplazamiento in range(1, 8):      # Incrementa progresivamete el desplazamiento en cierta direccion y sentido

                # Simula el desplazamiento de la pieza en una direccion ortogonal en concreto
                casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + desplazamiento * direccion))

                if not self.tablero.existe_casilla(casilla_a_comprobar):            # Si la casilla se sale del tablero, debe dejar de comprobar en esa direccion y pasar a la siguiente
                    break

                elif self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:    # Si la casilla esta libre, debe seguir incrementando el desplazamiento en esa direccion
                    casillas_mov_perm.append(casilla_a_comprobar)

                else:                                                               # Si se llega a este caso, se ha encontrado una pieza en el camino, por lo que el ciclo debe detenerse
                    if self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:
                        casillas_mov_perm.append(casilla_a_comprobar)               # Comprueba si la pieza con la que se ha encontrado es del mismo color o no para saber si permitir la captura
                    break                                                           # Pueda capturar la pieza o no, se detiene la comprobacion en esa direccion

        return casillas_mov_perm


# Creacion de la clase Dama
class Dama(Pieza):
    """ Representa una dama blanca o negra en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Dama derivados de Pieza. """
        super().__init__("dama", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierta dama. """
        
        casillas_mov_perm: list[str] = []

        # Genera una torre y un alfil auxiliares para simular el movimiento de una dama
        dama_torre: Torre = Torre(self.color, self.tablero)
        dama_alfil: Alfil = Alfil(self.color, self.tablero)

        # Junta los movimientos posibles para el alfil y la torre simuladas para generar la lista definitiva
        casillas_mov_perm = dama_torre.movimientos_posibles(casilla) + dama_alfil.movimientos_posibles(casilla)
        return casillas_mov_perm


# Creacion de la clase Rey
class Rey(Pieza):
    """ Representa el rey blanco o negro en el tablero. """

    def __init__(self, color: str, tablero: "Tablero | None") -> None:
        """ Define los atributos de Rey derivados de Pieza. """
        super().__init__("rey", color, tablero)


    def movimientos_posibles(self, casilla: str) -> list[str]:
        """ Devuelve una lista con todas las casillas a las que se puede mover cierto rey. No comprueba el jaque. """

        casillas_mov_perm: list[str] = []
        casilla_a_comprobar: str = ""

        for desplazamiento_vert in range(-1, 2):
            for desplazamiento_horiz in range(-1, 2):                           # Comprueba las casillas en el cuadrado 3x3 alrededor del rey

                if desplazamiento_vert == 0 and desplazamiento_horiz == 0:      # Si la casilla es la casilla de inicio, se salta para evitar errores
                    continue

                casilla_a_comprobar = reparar_columna_casilla(str(int(casilla) + desplazamiento_vert + 10*desplazamiento_horiz))

                if self.tablero.existe_casilla(casilla_a_comprobar):                    # Si existe la casilla, continua la comprobacion

                    if self.tablero.pieza_en_casilla(casilla_a_comprobar) == None:      # Si la casilla esta vacia, es valida
                        casillas_mov_perm.append(casilla_a_comprobar)

                    elif self.tablero.pieza_en_casilla(casilla_a_comprobar).color != self.tablero.pieza_en_casilla(casilla).color:      # Si la pieza en la casilla de llegada es del color contrario, permite la captura
                        casillas_mov_perm.append(casilla_a_comprobar)

        return casillas_mov_perm    # La lista devuelta ignora por completo el jaque, que se comprueba en el metodo "mover_pieza"


# Creacion de la clase Partida
class Partida:
    """ Representa el contexto entero de una partida, englobando el tablero, los movimientos que ya han transcurrido y el estado de su maquina de estados. Permite guardar rutas para su archivo .txt y .csv correspondiente. """

    def __init__(self, ruta_txt: str = "partida.txt", ruta_csv: str = "partida.csv") -> None:
        """ Definicion de los atributos de la clase Partida. La ruta se establece por defecto a "partida.txt". """

        self.movimientos: list[str] = []            # Lista con todos los movimientos jugados hasta ahora en formato estandarizado (e2 e4)
        self.estado: str = "turno_blancas"          # Estado de la maquina de estados, que adquiere los valores "turno_blancas", "turno_negras" y "fin_partida"
        self.tablero: Tablero = Tablero(self)       # Genera un tablero intrinsecamente relacionado a la partida para que el tablero pueda acceder al turno de su partida en concreto
        self.ruta_txt: str = ruta_txt               # La ruta esta hardcodeada a "partida.txt" por los requisitos de la entrega, pero la pongo como atributo para poder cambiarla facilmente
        self.ruta_csv: str = ruta_csv               # Ruta para el csv tambien hardcodeada por los requisitos


    def reiniciar(self) -> None:
        """ Devuelve tanto el estado de Tablero como el resto de atributos de Partida a su estado inicial. """
        
        self.movimientos = []
        self.estado = "turno_blancas"
        self.tablero.reiniciar()


    def comenzar_partida(self) -> None:
        """ Pone en marcha la máquina de estados. """

        self.tablero.imprimir_tablero()

        # Variables auxiliares para poder imprimir mensajes a la consola con gramatica correcta segun genero y numero
        color_estado: str = ""
        nombre_estado: str = ""
        nombre_opuesto: str = ""
            
        while self.estado != "fin_partida":

            # Asignacion de valores a esas variables auxiliares
            if self.estado == "turno_blancas":
                color_estado = "blanco"
                nombre_estado = "blancas"
                nombre_opuesto = "negras"
            elif self.estado == "turno_negras":
                color_estado = "negro"
                nombre_estado = "negras"
                nombre_opuesto = "blancas"

            # Comprobacion de jaque, jaque mate y rey ahogado e impresion del mensaje correspondiente en la consola
            posicion_estado: str | None = self.tablero.analizar_posicion_color(color_estado)

            if posicion_estado == "jaque":
                print(f"Jaque a las {nombre_estado}.")

            elif posicion_estado == "jaque mate":
                print(f"Jaque mate. Ganan las {nombre_opuesto}, fin de la partida.")
                self.estado = "fin_partida"

            elif posicion_estado == "rey ahogado":
                print(f"Rey ahogado a las {nombre_estado}, fin de la partida")
                self.estado = "fin_partida"

            # Si el turno es de las blancas
            if self.estado == "turno_blancas":
                print("Turno de las blancas.")

                try:

                    if self.ejecutar_turno() == True and self.estado == "turno_blancas":    # Ejecuta el turno y si se ha realizado un movimiento correctamente y el estado no es "fin_partida", se cambia el truno a "turno_negras"
                        self.estado = "turno_negras"

                except ValueError as error:     # Atrapa el error correspondiente y lo imprime por pantalla sin cambiar el turno
                    print(error)

            # Si el turno es de las negras
            elif self.estado == "turno_negras":
                print("Turno de las negras.")

                try:

                    if self.ejecutar_turno() == True and self.estado == "turno_negras":     # Ejecuta el turno y si se ha realizado un movimiento correctamente y el estado no es "fin_partida", se cambia el truno a "turno_blancas"
                        self.estado = "turno_blancas"

                except ValueError as error:     # Atrapa el error correspondiente y lo imprime por pantalla sin cambiar el turno
                    print(error)


    def ejecutar_turno(self) -> bool:
        """ Pregunta al jugador por el movimiento y comprueba que es válida la sintaxis del input. El bool que devuelve indica si se debe alternar el turno, no que no se haya ejecutado correctamente. """

        user_input: str = ""
        casilla_inicio: str = ""
        casilla_llegada: str = ""

        # Se permite la introduccion de mayusculas y espacios al principio, al final y entre las casillas
        user_input = input("Introduce un movimiento valido, escribe 'salir' para finalizar o 'exportar' para generar un archivo csv: ").lower().strip()

        # Caso de finalizacion del programa
        if user_input == "salir":
            self.estado = "fin_partida"
            return False

        # Caso de exportacion de la informacion de la partira a archivo csv sin cambiar el turno
        elif user_input == "exportar":
            self.exportar_historial_csv(self.ruta_csv)
            return False

        # Caso de movimiento con sintaxis valida y con casillas dentro del tablero
        else:
            # Se reescribe la lista en partes para detectar un numero de espacios intermedios anomalo
            partes: list[str] = user_input.split()

            # Se comprueba si el movimiento tiene 2 partes para evitar index error en caso de estar vacio
            if len(partes) == 2:
                movimiento: str = partes[0] + " " + partes[1]
                print("")

                # Se comprueba la estructura del movimiento precisa
                if len(movimiento) == 5 and movimiento[0] in letras_perm and movimiento[1] in numeros_perm and movimiento[2] == " " and movimiento[3] in letras_perm and movimiento[4] in numeros_perm:

                    # Uso de slicing para determinar las casillas de inicio y llegada y conversion a ID
                    casilla_inicio = casilla_a_ID(movimiento[0:2])
                    casilla_llegada = casilla_a_ID(movimiento[3:5])

                    # Intento de mover la pieza
                    self.tablero.mover_pieza(casilla_inicio, casilla_llegada, indexar_movimiento = True)
                    print("")

                    self.tablero.imprimir_tablero()

                    return True

        # Si ninguno de los 3 casos se da, se devuelve un error
        raise ValueError("Formato no valido. Escribe origen y destino, por ejemplo: e2 e4")


    def cargar_historial(self, ruta_txt: str) -> None:
        """ Busca el archivo tipo .txt seleccionado y simula los movimientos para cargar la partida, devolviendo error si el archivo es invalido. """

        numero_movimientos: int = 0

        with open(ruta_txt, "r") as archivo:

            # Se extraen los movimientos en formato estandarizado (e2 e4) en una lista
            movimientos: list[str] = archivo.readlines()

            # Se recorre la lista movimiento por movimiento y se limpian los saltos de linea y cualquier otro tipo de interferencia de formato con .strip
            for movimiento in movimientos:
                movimiento = movimiento.strip()

                # Filtracion del caso en el que la linea esta vacia, que se debe saltar
                if movimiento == "":
                    continue

                # Comprobacion de la sintaxis correcta del movimiento
                if len(movimiento) == 5 and movimiento[0] in letras_perm and movimiento[1] in numeros_perm and movimiento[2] == " " and movimiento[3] in letras_perm and movimiento[4] in numeros_perm:

                    # Obtencion de la casilla de salida y de llegada y su conversion a ID
                    casilla_inicio: str = casilla_a_ID(movimiento[0:2])
                    casilla_llegada: str = casilla_a_ID(movimiento[3:5])

                    try:
                        # Intenta mover la pieza, devolviendo error si se hace un movimiento invalido
                        self.tablero.mover_pieza(casilla_inicio, casilla_llegada)

                        self.movimientos.append(movimiento)

                        if self.estado == "turno_blancas":
                            self.estado = "turno_negras"
                        elif self.estado == "turno_negras":
                            self.estado = "turno_blancas"
                        
                        numero_movimientos += 1

                        # Comprueba si la partida ya ha acabo en jaque o en jaque mate para las blancas
                        if numero_movimientos % 2 == 0:
                            posicion_blancas: str | None = self.tablero.analizar_posicion_color("blanco")

                            if posicion_blancas == "jaque mate" or posicion_blancas == "rey ahogado":
                                print("La partida cargada ya ha finalizado. Comenzando partida nueva.\n")
                                self.reiniciar()
                                return

                        # Comprueba si la partida ya ha acabo en jaque o en jaque mate para las negras
                        else:
                            posicion_negras: str | None = self.tablero.analizar_posicion_color("negro")

                            if posicion_negras == "jaque mate" or posicion_negras == "rey ahogado":
                                print("La partida cargada ya ha finalizado. Comenzando partida nueva.\n")
                                self.reiniciar()
                                return
                        
                    except ValueError:      # Si el movimiento no es valido, se ignora el archivo, se resetea la partida y se comienza una partida nueva
                        print("El archivo guardado no es válido.\n")
                        self.reiniciar()
                        return

                else:                       # Si una linea no tiene sintaxis correcta, se ignora el archivo, se resetea la partida y se comienza una partida nueva
                    print("El archivo guardado no es válido.\n")
                    self.reiniciar()
                    return

        # Si se han simulado correctamente todos los movimientos de la partida, se determina el turno segun el numero de movimientos que han transcurrido
        if numero_movimientos % 2 == 0:
            self.estado = "turno_blancas"
        else:
            self.estado = "turno_negras"


    def guardar_historial(self, movimiento: str, ruta_txt: str) -> None:
        """ Guarda cierto movimiento en formato estandarizado (e2 e4) en la lista del historial de la partida y actualiza el archivo txt correspondiente. """

        self.movimientos.append(movimiento)

        # Abre el archivo, lo vacia y vuelve a escribir todos los movimientos guardados desde el comienzo
        with open(ruta_txt, "w") as archivo:
            for movimiento in self.movimientos:
                archivo.write(movimiento + "\n")


    def exportar_historial_csv(self, ruta_csv: str) -> None:
        """ Genera un archivo con la informacion de todos los movimientos de la partida (numero de turno, jugador que mueve, casilla de origen y casilla de destino) en formato .csv. """

        with open(ruta_csv, "w", newline = "") as archivo:
            escritor = csv.writer(archivo)
            numero_movimiento: int = 1
            turno: str = "blancas"
            casilla_inicio: str = ""
            casilla_llegada: str = ""

            # La primera linea que escribe determina los titulos de las columnas
            escritor.writerow(["numero", "turno", "origen", "destino"])

            # Recorre la lista de movimientos y guarda su informacion en una linea de archivo .csv por movimiento
            for movimiento in self.movimientos:

                # Determina el turno segun el numero del movimiento
                if numero_movimiento % 2 == 1:
                    turno = "blancas"
                else:
                    turno = "negras"

                # Encuentra las casillas de inicio y llegada con slicing
                casilla_inicio = movimiento[0:2]
                casilla_llegada = movimiento[3:5]

                # Guarda la informacion en una linea de golpe
                escritor.writerow([numero_movimiento, turno, casilla_inicio, casilla_llegada])
                
                numero_movimiento += 1

        print("Partida exportada con éxito.")


    def iniciar_juego(self) -> None:
        """ Comprueba que el archivo existe y pregunta por la continuacion de la partida. """

        ruta: str = self.ruta_txt

        # Si se detecta que una partida en .txt existe, se pregunta si se quiere continuar
        if os.path.exists(ruta):

            user_input: str = input("Se ha detectado una partida existente. Si desea cargarla, introduzca 's': ").lower().strip()
            if user_input == "s":

                # Intenta cargar la partida, comenzando una nueva si el archivo no es valido 
                self.cargar_historial(ruta)

        # Comienza la partida en el estado en el que se encuentre, independientemente de si se ha cargado la partida o no
        # La comprobacion de la validez de la partida ya se ha ejecutado en cargar_historial(ruta), por lo que no hace falta comprobarlo aqui
        self.comenzar_partida()


# Comienzo de la partida
partida_main: Partida = Partida()
partida_main.iniciar_juego()