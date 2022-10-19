from os import cpu_count
import random
from copy import deepcopy
from colorama import init, Fore, Style
init()

MIN_FILAS = 5
MAX_FILAS = 10
MIN_COLUM = 6
MAX_COLUM = 10
ESPACIO_VACIO = " "
SIMBOLO1 = "x"
SIMBOLO2 = "o"
JUGADOR1 = 1
JUGADOR2 = 2
CONECTA = 4
CPU_ON = False



# Aquí estarán definidas las funciones que rigen la cantidad de columnas y filas que tendrá el tablero.

def solicitar_entero_valido(mensaje):
   
    while True:
        try:
            posible_entero = int(input(mensaje))
            return posible_entero
        except ValueError:
            continue


def solicitar_columnas():
    while True:
        columnas = solicitar_entero_valido("Ingresa el número de columnas:")
        if columnas < MIN_COLUM or columnas > MAX_COLUM:
            print(f"El mínimo de columnas es {MIN_COLUM} y el máximo {MAX_COLUM}")
        else:
            return columnas


def solicitar_filas():
    while True:
        filas = solicitar_entero_valido("Ingresa el número de filas:")
        if filas < MIN_FILAS or filas > MAX_FILAS:
            print(f"El mínimo de filas es {MIN_FILAS} y el máximo {MAX_FILAS}")
        else:
            return filas

# Aquí estarán las funciones que rigan la creación del tablero.

def crear_tablero(filas, columnas):
    tablero = []
    for fila in range(filas):
        tablero.append([])
        for columna in range(columnas):
            tablero[fila].append(ESPACIO_VACIO)
    return tablero


def imprimir_tablero(tablero):
    
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            color_terminal = Fore.GREEN
            if valor == SIMBOLO1:
                color_terminal = Fore.RED
            print(color_terminal + valor, end="")
            print(Style.RESET_ALL, end="")
            print("|", end="")
        print("")
    
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")

# Aquí estarán las funciones que validen la disponibilidad de lugar en una fila/columna para colocar la pieza.

def obtener_fila_valida_en_columna(columna, tablero):
    indice = len(tablero) - 1
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            return indice
        indice -= 1
    return -1


def solicitar_columna(tablero):
    
    while True:
        columna = solicitar_entero_valido("Ingresa la columna para colocar la pieza: ")
        if columna <= 0 or columna > len(tablero[0]):
            print("Columna no válida.")
        elif tablero[0][columna - 1] != ESPACIO_VACIO:
            print("Esa columna ya está llena.")
        else:
            return columna - 1


def colocar_pieza(columna, jugador, tablero):
  
    color = SIMBOLO1
    if jugador == JUGADOR2:
        color = SIMBOLO2
    fila = obtener_fila_valida_en_columna(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = color
    return True

# Aquí estarán las funciones del conteo de fichas.

def obtener_conteo_der(fila, columna, color, tablero):
    fin_columnas = len(tablero[0])
    contador = 0
    for i in range(columna, fin_columnas):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_izq(fila, columna, color, tablero):
    contador = 0
    # -1 porque no es inclusivo
    for i in range(columna, -1, -1):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0

    return contador


def obtener_conteo_abajo(fila, columna, color, tablero):
    fin_filas = len(tablero)
    contador = 0
    for i in range(fila, fin_filas):
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_arriba(fila, columna, color, tablero):
    contador = 0
    for i in range(fila, -1, -1):
        if contador >= CONECTA:
            return contador
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_arriba_der(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna += 1
    return contador


def obtener_conteo_arriba_izq(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna -= 1
    return contador


def obtener_conteo_abajo_izquierda(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna -= 1
    return contador


def obtener_conteo_abajo_der(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna += 1
    return contador


def obtener_direcciones():
    return [
        'izquierda',
        'arriba',
        'abajo',
        'derecha',
        'arriba_derecha',
        'abajo_derecha',
        'arriba_izquierda',
        'abajo_izquierda',
    ]


def obtener_conteo(fila, columna, color, tablero):
    direcciones = obtener_direcciones()
    for direccion in direcciones:
        funcion = globals()['obtener_conteo_' + direccion]
        conteo = funcion(fila, columna, color, tablero)
        if conteo >= CONECTA:
            return conteo
    return 0

# Aquí estará la función para declarar un color al jugador.

def obtener_color_de_jugador(jugador):
    color = SIMBOLO1
    if jugador == JUGADOR2:
        color = SIMBOLO2
    return color

# Aquí estará la función para comprobar quién es el ganador.

def comprobar_ganador(jugador, tablero):
    color = obtener_color_de_jugador(jugador)
    for f, fila in enumerate(tablero):
        for c, celda in enumerate(fila):
            conteo = obtener_conteo(f, c, color, tablero)
            if conteo >= CONECTA:
                return True
    return False

# Aquí estarán las funciones para seleccionar al jugador y los turnos.

def elegir_jugador_al_azar():
    return random.choice([JUGADOR1, JUGADOR2])


def imprimir_y_solicitar_turno(turno, tablero):
    if not CPU_ON:
        print(f"Jugador 1: {SIMBOLO1} | Jugador 2: {SIMBOLO2}")
    else:
        print(f"Jugador 1: {SIMBOLO1} | CPU: {SIMBOLO2}")
    if turno == JUGADOR1:
        print(f"Turno del jugador 1 ({SIMBOLO1})")
    else:
        if not CPU_ON:
            print(f"Turno del jugador 2 ({SIMBOLO2})")
        else:
            print("Turno de la CPU")
    return solicitar_columna(tablero)

# Aquí estará la función para felicitar al Jugador ganador.


def felicitar_jugador(jugador_actual):
    if not CPU_ON:
        if jugador_actual == JUGADOR1:
            print("Felicidades Jugador 1. Has ganado")
        else:
            print("Felicidades Jugador 2. Has ganado")
    else:
        if jugador_actual == JUGADOR1:
            print("Felicidades Jugador 1. Has ganado")
        else:
            print("Ha ganado el CPU")

# Aquí estarán las funciones en caso de haber un empate.

def es_empate(tablero):
    for columna in range(len(tablero[0])):
        if obtener_fila_valida_en_columna(columna, tablero) != -1:
            return False
    return True


def indicar_empate():
    print("Empate")

# Aquí estarán las funciones para determinar las jugadas restantes.

def obtener_tiradas_faltantes_en_columna(columna, tablero):
    indice = len(tablero) - 1
    tiradas = 0
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            tiradas += 1
        indice -= 1
    return tiradas


def obtener_tiradas_faltantes(tablero):
    tiradas = 0
    for columna in range(len(tablero[0])):
        tiradas += obtener_tiradas_faltantes_en_columna(columna, tablero)
    return tiradas


def imprimir_tiradas_faltantes(tablero):
    print("Tiradas faltantes: " + str(obtener_tiradas_faltantes(tablero)))

# Aquí estará la función para jugador vs jugador.

def jugador_vs_jugador(tablero):
    jugador_actual = elegir_jugador_al_azar()
    while True:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
        ha_ganado = comprobar_ganador(jugador_actual, tablero)
        if ha_ganado:
            imprimir_tablero(tablero)
            felicitar_jugador(jugador_actual)
            break
        elif es_empate(tablero):
            imprimir_tablero(tablero)
            indicar_empate()
            break
        else:
            if jugador_actual == JUGADOR1:
                jugador_actual = JUGADOR2
            else:
                jugador_actual = JUGADOR1

# Aquí estarán las funciones para determinar la mejor jugada y el criterio de la CPU.

def obtener_columna_segun_cpu(jugador, tablero):
    return elegir_columna_ideal(jugador, tablero)


def obtener_jugador_contrario(jugador):
    if jugador == JUGADOR1:
        return JUGADOR2
    return JUGADOR1


def elegir_columna_ideal(jugador, tableroOriginal):
    """
    Reglas:
    1- Si hay un movimiento para ganar, tomarlo
    2- Si el oponente tiene un movimiento para ganar, evitarlo
    3- Si nada de lo de arriba se cumple, buscar columna en donde se obtendría el mayor puntaje
    4- Si lo de arriba no se cumple, buscar columna en donde el adversario obtendría el mayor puntaje
    5- Preferir tomar cosas centrales antes de bordes
    """
    tablero = deepcopy(tableroOriginal)
    # En caso de poder ganar
    columna_ganadora = obtener_columna_ganadora(jugador, tablero)
    if columna_ganadora != -1:
        return columna_ganadora
    # Si el oponente puede ganar, evito la jugada.
    columna_perdedora = obtener_columna_ganadora(obtener_jugador_contrario(jugador), tablero)
    if columna_perdedora != -1:
        return columna_perdedora

    umbral_puntaje = 1
    # Si no, buscaré un lugar en donde colocar mi pieza para tratar de conectar 4.
    puntaje_ganador, columna_mia = obtener_columna_con_mayor_puntaje(jugador, tablero)
    # Pero también necesito el de mi adversario.
    puntaje_ganador_adversario, columna_adversario = obtener_columna_con_mayor_puntaje(
        obtener_jugador_contrario(jugador), tablero)
    if puntaje_ganador > umbral_puntaje and puntaje_ganador_adversario > umbral_puntaje:
        # Aquí se puede elegir entre ataque o defensa. Se prefiere la defensa.
        if puntaje_ganador_adversario > puntaje_ganador:
            return columna_adversario
        else:
            return columna_mia
    # Si lo demás falla, elegir una columna central.
    central = obtener_columna_central(jugador, tablero)
    if central != -1:
        return central
    # Y de últimas, elegir la primer columna que no esté vacía
    columna_disponible = obtener_primera_columna_vacia(jugador, tablero)
    if columna_disponible != -1:
        return columna_disponible
    # Si no, no sé qué más hacer. Esto no debería pasar.
    print("Error. No se debería llegar hasta aquí")


def obtener_primera_columna_vacia(jugador, tableroOriginal):
    tablero = deepcopy(tableroOriginal)
    for indice in range(len(tablero[0])):
        if colocar_pieza(indice, jugador, tablero):
            return indice


def obtener_columna_central(jugador, tableroOriginal):
    tablero = deepcopy(tableroOriginal)
    mitad = int((len(tablero[0]) - 1) / 2)
    if colocar_pieza(mitad, jugador, tablero):
        return mitad
    return -1


def obtener_primera_fila_no_vacia(columna, tablero):
    for indice_fila, fila in enumerate(tablero):
        if fila[columna] != ESPACIO_VACIO:
            return indice_fila
    return -1


def obtener_columna_con_mayor_puntaje(jugador, tableroOriginal):
    conteo_mayor = 0
    indice_columna_mayor = -1
    for indiceColumna in range(len(tableroOriginal)):
        tablero = deepcopy(tableroOriginal)
        pieza_colocada = colocar_pieza(indiceColumna, jugador, tablero)
        if pieza_colocada:
            fila = obtener_primera_fila_no_vacia(indiceColumna, tablero)
            if fila != -1:
                conteo = obtener_conteo(fila, indiceColumna, obtener_color_de_jugador(jugador), tablero)
                if conteo > conteo_mayor:
                    conteo_mayor = conteo
                    indice_columna_mayor = indiceColumna
    return conteo_mayor, indice_columna_mayor


def obtener_columna_ganadora(jugador, tableroOriginal):
    for indiceColumna in range(len(tableroOriginal)):
        tablero = deepcopy(tableroOriginal)
        pieza_colocada = colocar_pieza(indiceColumna, jugador, tablero)
        if pieza_colocada:
            gana = comprobar_ganador(jugador, tablero)
            if gana:
                return indiceColumna
    return -1

# Aquí estarán las funciones en caso de jugar contra la CPU.

def jugador_vs_computadora(tablero):
    global CPU_ON
    CPU_ON = True
    jugador_actual = elegir_jugador_al_azar()
    while True:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        if jugador_actual == JUGADOR1:
            columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        else:
            print("CPU pensando...")
            columna = obtener_columna_segun_cpu(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna.")
        ha_ganado = comprobar_ganador(jugador_actual, tablero)
        if ha_ganado:
            imprimir_tablero(tablero)
            felicitar_jugador(jugador_actual)
            break
        elif es_empate(tablero):
            imprimir_tablero(tablero)
            indicar_empate()
            break
        else:
            if jugador_actual == JUGADOR1:
                jugador_actual = JUGADOR2
            else:
                jugador_actual = JUGADOR1
    CPU_ON = False

# Aquí estará la función en caso de volver a jugar.

def volver_a_jugar():
    while True:
        eleccion = input("¿Quieres volver a jugar? [s/n] ").lower()
        if eleccion == "s":
            return True
        elif eleccion == "n":
            return False

# Aquí estará la función para seleccionar el tipo de juego o salir de este.

def main():
    while True:
        eleccion = input("1- Jugador vs Jugador"
                         "\n"
                         "2- Jugador vs Máquina"
                         "\n"
                         "3- Salir"
                         "\n"
                         "Elige: ")
        if eleccion == "3":
            break

        if eleccion == "1":
            filas, columnas = solicitar_filas(), solicitar_columnas()
            while True:
                tablero = crear_tablero(filas, columnas)
                jugador_vs_jugador(tablero)
                if not volver_a_jugar():
                    break
        if eleccion == "2":
            filas, columnas = solicitar_filas(), solicitar_columnas()
            while True:
                tablero = crear_tablero(filas, columnas)
                jugador_vs_computadora(tablero)
                if not volver_a_jugar():
                    break


main()