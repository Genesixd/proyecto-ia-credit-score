import random
import math
from typing import List, Tuple


# =========================
#  Representación del problema N-Reinas
# =========================

def generar_estado_inicial(n: int) -> List[int]:
    """
    Genera un estado inicial para N-Reinas.
    Representación: lista de longitud n, donde estado[columna] = fila de la reina.
    """
    # Versión simple: colocar una reina en una fila aleatoria por columna
    return [random.randint(0, n - 1) for _ in range(n)]


def costo(estado: List[int]) -> int:
    """
    Función de costo: número de pares de reinas que se atacan.
    Menor costo = mejor solución. Costo 0 = solución válida.
    """
    n = len(estado)
    conflictos = 0

    for i in range(n):
        for j in range(i + 1, n):
            # Mismas filas
            if estado[i] == estado[j]:
                conflictos += 1
            # Mismas diagonales
            if abs(estado[i] - estado[j]) == abs(i - j):
                conflictos += 1

    return conflictos


def vecino(estado: List[int]) -> List[int]:
    """
    Genera un vecino moviendo una reina a otra fila en una columna aleatoria.
    """
    n = len(estado)
    nuevo = estado.copy()

    col = random.randint(0, n - 1)  # columna a modificar
    fila_actual = nuevo[col]

    # Elegir una fila distinta a la actual
    posibles_filas = [f for f in range(n) if f != fila_actual]
    nueva_fila = random.choice(posibles_filas)

    nuevo[col] = nueva_fila
    return nuevo


# =========================
#   Algoritmo de Simulated Annealing
# =========================

def simulated_annealing(
    n: int,
    temperatura_inicial: float = 1.0,
    temperatura_min: float = 1e-3,
    alfa: float = 0.99,
    max_iter: int = 100000
) -> Tuple[List[int], int]:
    """
    Ejecuta Recocido Simulado para el problema de N-Reinas.

    Parámetros:
        n: tamaño del tablero (N).
        temperatura_inicial: temperatura inicial T0.
        temperatura_min: temperatura mínima para detener el proceso.
        alfa: factor de enfriamiento (T = alfa * T).
        max_iter: número máximo de iteraciones.

    Retorna:
        mejor_estado: configuración final encontrada.
        mejor_costo: costo (número de conflictos) del mejor_estado.
    """
    # Estado inicial
    estado_actual = generar_estado_inicial(n)
    costo_actual = costo(estado_actual)

    mejor_estado = estado_actual[:]
    mejor_costo = costo_actual

    T = temperatura_inicial
    iteracion = 0

    while T > temperatura_min and iteracion < max_iter and mejor_costo > 0:
        iteracion += 1

        # Generar vecino
        estado_vecino = vecino(estado_actual)
        costo_vecino = costo(estado_vecino)

        delta = costo_vecino - costo_actual

        # Si mejora, aceptamos directo
        if delta <= 0:
            estado_actual = estado_vecino
            costo_actual = costo_vecino
        else:
            # Si empeora, aceptamos con cierta probabilidad
            prob = math.exp(-delta / T)
            if random.random() < prob:
                estado_actual = estado_vecino
                costo_actual = costo_vecino

        # Actualizar mejor solución conocida
        if costo_actual < mejor_costo:
            mejor_estado = estado_actual[:]
            mejor_costo = costo_actual

        # Enfriamiento
        T *= alfa

    return mejor_estado, mejor_costo


def imprimir_tablero(estado: List[int]) -> None:
    """
    Muestra el tablero de N-Reinas en consola.
    'Q' = reina, '.' = vacío.
    """
    n = len(estado)
    for fila in range(n):
        linea = ""
        for col in range(n):
            if estado[col] == fila:
                linea += " Q"
            else:
                linea += " ."
        print(linea)
    print()


# =========================
#   Pruebas rápidas
# =========================

if __name__ == "__main__":
    random.seed(42)

    for n in [8, 10]:
        print(f"\n=== N-REINAS con Simulated Annealing (N={n}) ===")
        mejor_estado, mejor_costo = simulated_annealing(
            n=n,
            temperatura_inicial=1.0,
            temperatura_min=1e-4,
            alfa=0.99,
            max_iter=200000
        )

        print(f"Mejor costo encontrado: {mejor_costo}")
        print(f"Estado (posiciones de reinas por columna): {mejor_estado}")

        if mejor_costo == 0:
            print("Se encontró una solución SIN conflictos:")
        else:
            print("No se logró eliminar todos los conflictos, pero se minimizó el costo.")

        imprimir_tablero(mejor_estado)
