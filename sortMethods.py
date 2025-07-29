import time
import random
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing


from insertion import insertion
from selection import selection
from shell import shell
from merge import merge_sort
from heap import heap



def readInput(filename): # lê o arquivo input
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines if line.strip()]


def arrayType(size, typeArray): # verifica no input qual tipo de array é
    if typeArray == "OrdC":
        return list(range(size))
    elif typeArray == "OrdD":
        return list(range(size, 0, -1))
    elif typeArray == "OrdA":
        return random.sample(range(size * 10), size)
    else:
        raise ValueError(f"Tipo de vetor desconhecido: {typeArray}")


def callSortMethod(method, array, timeout_seconds=7200): # chama os métodos importados com base no nome do método
    def run_sort(queue, method, array):
        try:
            if method == "Insert":
                result = insertion(array)
            elif method == "Shell":
                result = shell(array)
            elif method == "Select":
                result = selection(array)
            elif method == "Merge":
                result = merge_sort(array)
            elif method == "Heap":
                result = heap(array)
            else:
                raise ValueError(f"Método desconhecido: {method}")
            queue.put(result)
        except Exception as e:
            queue.put((None, None))
            print(f"[ERRO] {method}: {e}")

    queue = multiprocessing.Queue() # divide numa fila de processos, caso algum passe de 2h rodando, escreve o resultado e pula para o próximo
    process = multiprocessing.Process(target=run_sort, args=(queue, method, array))
    process.start()
    process.join(timeout_seconds)

    if process.is_alive(): # mata o processo, antes gerava erro de freezing do código
        process.terminate()
        process.join()
        print(f"[TIMEOUT] Método {method} com vetor de tamanho {len(array)} excedeu {timeout_seconds} segundos.")
        return None, None

    if not queue.empty():
        return queue.get()
    else:
        return None, None



def writeOutput(results, filename='output.txt'): # escreve o resultado, caso tenha gerado timeout, informações nulas
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


def plotResults(results): # plota os resultados para cada tamanho de vetor
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

    for instruction in inputs:
        if len(instruction) != 3: # input diferente considera inválido
            print(f"Linha inválida: {instruction}")
            continue

        method, size, arrType = instruction
        try:
            size = int(size)
        except ValueError:
            print(f"Tamanho inválido: {size}")
            continue

        print("============================================================================")
        print(f"Executando {method} com tamanho={size} tipo={arrType}")
        array = arrayType(size, arrType)
        start = time.time()
        comparisons, movements = callSortMethod(method, list(array))
        end = time.time()

        if comparisons is None or movements is None:
            results.append({
                'method': method,
                'size': size,
                'vector_type': arrType,
                'time': None,
                'comparisons': '',
                'movements': ''
            })
            continue

        totalTime = end - start

        results.append({
            'method': method,
            'size': size,
            'vector_type': arrType,
            'time': totalTime,
            'comparisons': comparisons,
            'movements': movements
        })
    writeOutput(results)

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