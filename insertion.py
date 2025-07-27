import matplotlib.pyplot as plt
import random
import time


def insertion(arr):
    n = len(arr)
    comparisons = 0
    movements = 0

    start = time.time()

    for i in range(1, n):
        key = arr[i]
        movements += 1
        j = i - 1
        while j >= 0:
            comparisons += 1
            if key < arr[j]:
                arr[j + 1] = arr[j]
                movements += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
        movements += 1

    end = time.time()

    expected_compares = (n * (n - 1)) / 4  
    expected_movements = (n ** 2) / 4 + (11 * n) / 4 - 3

    print("\n== INSERTION SORT ==")
    print(f"Cálculo esperado para comparações: {expected_compares}")
    print(f"Cálculo esperado para movimentos: {expected_movements}")
    print(f"Comparações: {comparisons}")
    print(f"Movimentos: {movements}")
    print(f"Tempo de execução: {end - start:.6f} segundos")

    return comparisons, movements


def plotInsertion():
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 500, 800, 1000]
    comparisonsList = []
    movementsList = []

    for size in sizes:
        arr_random = [random.randint(0, 500) for _ in range(size)]
        qtdeComparisons, qtdeMovements = insertion(list(arr_random))

        comparisonsList.append(qtdeComparisons)
        movementsList.append(qtdeMovements)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    color1 = 'tab:green'
    ax1.set_xlabel('Tamanho da Lista')
    ax1.set_ylabel('Número de Comparações', color=color1)
    line1 = ax1.plot(sizes, comparisonsList, color=color1, marker='o', label='Comparações')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'tab:orange'
    ax2.set_ylabel('Número de Movimentos', color=color2)
    line2 = ax2.plot(sizes, movementsList, color=color2, marker='s', label='Movimentos')
    ax2.tick_params(axis='y', labelcolor=color2)


    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title('Insertion Sort: Comparações e Movimentos vs. Tamanho da Lista')
    plt.tight_layout()
    plt.show()


print("Gerando gráficos para Insertion Sort...")
plotInsertion()
print("Gráficos de Insertion Sort gerados.")