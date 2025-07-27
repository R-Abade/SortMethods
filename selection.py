import matplotlib.pyplot as plt
import random
import time


def selection(arr):
    n = len(arr)
    comparisons = 0
    movements = 0

    start = time.time()

    for i in range(n - 1):
        min = i  
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min]:
                min = j
        if min != i:
            arr[i], arr[min] = arr[min], arr[i]  
            movements += 3  

    end = time.time()

    expected_compares = (n * (n - 1)) / 2
    expected_movements = 3 * (n - 1)

    print("\n== SELECTION SORT ==")
    print(f"Cálculo esperado para comparações: {expected_compares}")
    print(f"Cálculo esperado para movimentos: {expected_movements}")
    print(f"Comparações: {comparisons}")
    print(f"Movimentos: {movements}")
    print(f"Tempo de execução: {end - start:.6f} segundos")

    return comparisons, movements


arr1 = [3, 2, 1, 5, 4]
selection(arr1.copy())


def plotSelection():
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 500, 800, 1000]
    comparisonsList = []
    movementsList = []

    for size in sizes:
        arr_random = [random.randint(0, 20) for _ in range(size)]
        qtdeComparisons, qtdeMovements = selection(list(arr_random))

        comparisonsList.append(qtdeComparisons)
        movementsList.append(qtdeMovements)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    color1 = 'tab:purple'
    ax1.set_xlabel('Tamanho da Lista')
    ax1.set_ylabel('Número de Comparações', color=color1)
    line1 = ax1.plot(sizes, comparisonsList, color=color1, marker='o', label='Comparações')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'tab:brown'
    ax2.set_ylabel('Número de Movimentos', color=color2)
    line2 = ax2.plot(sizes, movementsList, color=color2, marker='s', label='Movimentos')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title('Selection Sort: Comparações e Movimentos vs. Tamanho da Lista')
    plt.tight_layout()
    plt.show()


print("Gerando gráficos para Selection Sort...")
plotSelection()
print("Gráficos de Selection Sort gerados.")
