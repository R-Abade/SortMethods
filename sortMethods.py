import time
import random
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures

from insertion import insertion
from selection import selection
from shell import shell
from merge import merge_sort
from heap import heap


def arrayType(size, typeArray):
    if typeArray == "OrdC":
        return list(range(size))
    elif typeArray == "OrdD":
        return list(range(size, 0, -1))
    elif typeArray == "OrdA":
        return random.sample(range(size * 10), size)
    else:
        raise ValueError(f"Tipo de vetor desconhecido: {typeArray}")


def readInput(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines if line.strip()]


def callSortMethod(method, array, timeout_seconds=7200):
    def run():
        if method == "Insert":
            return insertion(array)
        elif method == "Shell":
            return shell(array)
        elif method == "Select":
            return selection(array)
        elif method == "Merge":
            return merge_sort(array)
        elif method == "Heap":
            return heap(array)
        else:
            raise ValueError(f"Método desconhecido: {method}")

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=1) as executor:  # pula o algoritmo depois de passar de 2h rodando
        future = executor.submit(run)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            print(f"[TIMEOUT] Método {method} com vetor de tamanho {len(array)} excedeu {timeout_seconds} segundos.")
            return None, None


def writeOutput(results, filename='output.txt'):
    with open(filename, 'w') as f:
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")
        f.write("|     Method     |   Size  | Vector Type | Time (s) | Comparisons | Movements |\n")
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")
        for result in results:
            f.write("| {:14} | {:7} | {:11} | {:>8} | {:>11} | {:>9} |\n".format(
                result['method'],
                result['size'],
                result['vector_type'],
                f"{result['time']:.10f}" if result['time'] is not None else "TIMEOUT",
                result['comparisons'] if result['comparisons'] != '' else 'N/A',
                result['movements'] if result['movements'] != '' else 'N/A'
            ))
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")


def plotResults(results):
    sizes = [100, 1000, 10000, 1000000]
    arrayTypes = ['OrdA', 'OrdC', 'OrdD']
    methods = ['Insert', 'Shell', 'Select', 'Merge', 'Heap']

    data = {}
    for size in sizes:
        data[size] = {}
        for vtype in arrayTypes:
            data[size][vtype] = {'comparisons': {}, 'movements': {}}

    for result in results:
        size = result['size']
        vtype = result['vector_type']
        method = result['method']

        # só processar se tem dados válidos (não timeout)
        if (size in sizes and vtype in arrayTypes and
                result['comparisons'] != '' and result['movements'] != ''):
            data[size][vtype]['comparisons'][method] = result['comparisons']
            data[size][vtype]['movements'][method] = result['movements']



    for size in sizes:
        # verificar se há dados válidos para este tamanho
        has_data = False
        for vtype in arrayTypes:
            if data[size][vtype]['comparisons']:
                has_data = True
                break

        if not has_data:
            continue

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'Comparações e Movimentações por Algoritmo (Tamanho: {size})', fontsize=14)

        for vtype in ['OrdA', 'OrdC', 'OrdD']:
            if data[size][vtype]['comparisons']:
                break

        available_methods = []
        comparisons_data = []
        movements_data = []

        for method in methods:
            if method in data[size][vtype]['comparisons']:
                available_methods.append(method)
                comparisons_data.append(data[size][vtype]['comparisons'][method])
                movements_data.append(data[size][vtype]['movements'][method])

        if not available_methods:
            continue

        x_pos = np.arange(len(available_methods))

        # Gráfico de Comparações
        bars1 = ax1.bar(x_pos, comparisons_data, color='blue', alpha=0.7)
        ax1.set_title('Comparações')
        ax1.set_xlabel('Método')
        ax1.set_ylabel('Quantidade')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(available_methods)
        ax1.grid(True, alpha=0.3)

        for bar, value in zip(bars1, comparisons_data):
            height = bar.get_height()
            ax1.annotate(f'{value:,}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom',
                         fontsize=8)

        # Gráfico de Movimentações
        bars2 = ax2.bar(x_pos, movements_data, color='red', alpha=0.7)
        ax2.set_title('Movimentações')
        ax2.set_xlabel('Método')
        ax2.set_ylabel('Quantidade')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(available_methods)
        ax2.grid(True, alpha=0.3)

        for bar, value in zip(bars2, movements_data):
            height = bar.get_height()
            ax2.annotate(f'{value:,}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom',
                         fontsize=8)

        fig.text(0.02, 0.02,
                 f'Tipo de vetor: {vtype}',
                 fontsize=10, style='italic')

        plt.tight_layout()
        plt.savefig(f'sorting_comparison_{size}.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    file = 'input.txt'
    inputs = readInput(file)
    results = []

    print("Executando algoritmos de ordenação...")
    for instruction in inputs:
        if len(instruction) != 3:
            print(f"Linha inválida: {instruction}")
            continue

        method, size, vector_type = instruction
        try:
            size = int(size)
        except ValueError:
            print(f"Tamanho inválido: {size}")
            continue

        print("============================================================================")
        print(f"Executando {method} com tamanho={size} tipo={vector_type}")
        array = arrayType(size, vector_type)
        start = time.time()
        comparisons, movements = callSortMethod(method, list(array))
        end = time.time()

        if comparisons is None or movements is None:
            results.append({
                'method': method,
                'size': size,
                'vector_type': vector_type,
                'time': None,
                'comparisons': '',
                'movements': ''
            })
            continue

        elapsed_time = end - start

        results.append({
            'method': method,
            'size': size,
            'vector_type': vector_type,
            'time': elapsed_time,
            'comparisons': comparisons,
            'movements': movements
        })

    writeOutput(results)
    print("Resultados salvos em output.txt")

    print("Gerando gráficos comparativos...")
    plotResults(results)

    print("################ CONFIGS DO PC ################")
    print("SO: Fedora")
    print("CPU: Intel Core i5-12450HX")
    print("RAM: 16GB")
    print("Python: 3.13")
    print("################################################")


if __name__ == "__main__":
    main()