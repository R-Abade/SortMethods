import matplotlib.pyplot as plt
import random
import time
import math


def merge_sort(arr):
    n = len(arr)
    comparisons = 0
    movements = 0
    start = time.time()

    def merge(left, right): # junta 2 pedaços em um só
        nonlocal comparisons, movements
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                result.append(left[i])
                movements += 1
                i += 1
            else:
                result.append(right[j])
                movements += 1
                j += 1

        while i < len(left):
            result.append(left[i])
            movements += 1
            i += 1
        while j < len(right):
            result.append(right[j])
            movements += 1
            j += 1

        return result

    def merge_sort_rec(sub): # divide o array em partes menores recursivamente
        if len(sub) <= 1:
            return sub
        m = len(sub) // 2
        left = merge_sort_rec(sub[:m])
        right = merge_sort_rec(sub[m:])
        return merge(left, right)

    sorted_arr = merge_sort_rec(arr)
    # Copia o array ordenado de volta para o original
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]
        movements += 1

    end = time.time()

    n = len(arr)
    expected_compares = n * math.ceil(math.log2(n)) if n > 1 else 0
    expected_movements = n * math.ceil(math.log2(n)) if n > 1 else 0

    print(f"== MERGE SORT ==")
    print(f"Cálculo esperado para comparações: {expected_compares}")
    print(f"Cálculo esperado para movimentos: {expected_movements}")
    print(f"Tamanho do vetor: (n={len(arr)})")
    print(f"Comparações: {comparisons}")
    print(f"Movimentos: {movements}")
    print(f"Tempo: {end - start:.6f}s")

    return comparisons, movements


def plotMergeSort():
    sizes = [10, 50, 100, 150, 200, 300, 500, 800, 1000]
    comps, movs = [], []
    for n in sizes:
        arr = [random.randint(0, 1000) for _ in range(n)]
        c, m = merge_sort(arr)
        comps.append(c);
        movs.append(m)

    fig, ax1 = plt.subplots(figsize=(12, 8))

    color1 = 'tab:blue'
    ax1.set_xlabel('Tamanho da Lista')
    ax1.set_ylabel('Número de Comparações', color=color1)
    line1 = ax1.plot(sizes, comps, color=color1, marker='o', label='Comparações')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Número de Movimentos', color=color2)
    line2 = ax2.plot(sizes, movs, color=color2, marker='s', label='Movimentos')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title('Merge Sort: Comparações e Movimentos vs. Tamanho da Lista')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Gerando gráficos para Merge Sort...")
    plotMergeSort()
    print("Gráficos de Merge Sort gerados.")