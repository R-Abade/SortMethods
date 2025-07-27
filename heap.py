import matplotlib.pyplot as plt
import random
import time


def heap(arr):
    n = len(arr)
    comparisons = 0
    movements = 0
    start = time.time()

    def heapify(sub, i, n): # organiza a heap baseando no maxHeap
        nonlocal comparisons, movements
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n: # verifica o filho esquerdo
            comparisons += 1
            if sub[left] > sub[largest]:
                largest = left

        if right < n: # verifica o filho direito
            comparisons += 1
            if sub[right] > sub[largest]:
                largest = right

        if largest != i:
            sub[i], sub[largest] = sub[largest], sub[i]
            movements += 3
            heapify(sub, largest, n)

    # monta a heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, i, n)

    # ordena a heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        movements += 3
        heapify(arr, 0, i)

    end = time.time()

    expected_compares = 2 * n * (n.bit_length() - 1) if n > 1 else 0  # Aproximação O(n log n)
    expected_movements = 3 * n * (n.bit_length() - 1) if n > 1 else 0

    print(f"== HEAP SORT ==")
    print(f"Cálculo esperado para comparações: {expected_compares}")
    print(f"Cálculo esperado para movimentos: {expected_movements}")
    print(f"Tamanho do vetor: (n={len(arr)})")
    print(f"Comparações: {comparisons}")
    print(f"Movimentos: {movements}")
    print(f"Tempo: {end - start:.6f}s")

    return comparisons, movements


def plotHeapSort():
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 500, 800, 1000]
    comparisonsList = []
    movementsList = []

    for size in sizes:
        arr_random = [random.randint(0, 1000) for _ in range(size)]
        qtdeComparisons, qtdeMovements = heap(list(arr_random))

        comparisonsList.append(qtdeComparisons)
        movementsList.append(qtdeMovements)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    color1 = 'tab:red'
    ax1.set_xlabel('Tamanho da Lista')
    ax1.set_ylabel('Número de Comparações', color=color1)
    line1 = ax1.plot(sizes, comparisonsList, color=color1, marker='o', label='Comparações')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.set_ylabel('Número de Movimentos', color=color2)
    line2 = ax2.plot(sizes, movementsList, color=color2, marker='s', label='Movimentos')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title('Heap Sort: Comparações e Movimentos vs. Tamanho da Lista')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Gerando gráficos para Heap Sort...")
    plotHeapSort()
    print("Gráficos de Heap Sort gerados.")