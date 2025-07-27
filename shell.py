import matplotlib.pyplot as plt
import random
import time


def shell(arr):
    n = len(arr)
    h = 1
    comparisons = 0
    movements = 0

    start = time.time()

    # Knuth sequencia h = 3*h + 1
    while h < n // 3:
        h = h * 3 + 1

    while h >= 1: # laço externo que executa enquanto o gap for válido
        for i in range(h, n):
            aux = arr[i]
            movements += 1
            j = i

            while j >= h and arr[j - h] > aux: # laço interno que percorre o array do h até o final
                comparisons += 1
                arr[j] = arr[j - h]
                movements += 1
                j -= h

            if j >= h:
                comparisons += 1

            arr[j] = aux
            movements += 1

        h = h // 3

    end = time.time()

    timeTotal = end - start
    expected_compares = n * (n ** 0.25)  # Knuth sequencia
    expected_movements = n * (n ** 0.5)

    print("\n== SHELL SORT ==")
    print(f"Cálculo esperado para comparações: {expected_compares:.2f}")
    print(f"Cálculo esperado para movimentos: {expected_movements:.2f}")
    print(f"Comparações: {comparisons}")
    print(f"Movimentos: {movements}")
    print(f"Tempo de execução: {timeTotal:.6f} segundos")

    return comparisons, movements


arr1 = [3, 2, 1, 5, 4]
print("Array original:", arr1)
shell(arr1.copy())


def plotShell():
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 500, 800, 1000]
    comparisonsList = []
    movementsList = []

    for size in sizes:
        print(f"Processing size: {size}")
        arr_random = [random.randint(0, 1000) for _ in range(size)]
        qtdeComparisons, qtdeMovements = shell(list(arr_random))

        comparisonsList.append(qtdeComparisons)
        movementsList.append(qtdeMovements)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    color1 = 'tab:cyan'
    ax1.set_xlabel('Tamanho da Lista')
    ax1.set_ylabel('Número de Comparações', color=color1)
    line1 = ax1.plot(sizes, comparisonsList, color=color1, marker='o', label='Comparações')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'tab:pink'
    ax2.set_ylabel('Número de Movimentos', color=color2)
    line2 = ax2.plot(sizes, movementsList, color=color2, marker='s', label='Movimentos')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title('Shell Sort: Comparações e Movimentos vs. Tamanho da Lista')
    plt.tight_layout()
    plt.show()


print("\nGerando gráficos para Shell Sort...")
plotShell()
print("Gráficos de Shell Sort gerados.")