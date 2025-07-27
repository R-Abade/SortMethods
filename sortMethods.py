import time
import random
import matplotlib.pyplot as plt
import numpy as np

from insertion import insertion
from selection import selection
from shell import shell
from merge import merge_sort
from heap import heap


def generate_vector(size, vector_type): # verifica o input procurando o tipo de ordenação
    if vector_type == "OrdC":
        return list(range(size))
    elif vector_type == "OrdD":
        return list(range(size, 0, -1))
    elif vector_type == "OrdA":
        return random.sample(range(size * 10), size)
    else:
        raise ValueError(f"Tipo de vetor desconhecido: {vector_type}")


def read_input_file(filename): # lê o input
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines if line.strip()]


def format_method_name(name):
    return {
        "Insert": "Insertion Sort",
        "Shell": "Shell Sort",
        "Select": "Selection Sort",
        "Merge": "Merge Sort",
        "Heap": "Heap Sort"
    }.get(name, "Unknown")


def call_sort_function(method, array): # chama os métodos
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


def write_output_file(results, filename='output.txt'): # gera a tabela com os resultados
    with open(filename, 'w') as f:
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")
        f.write("|     Method     |   Size  | Vector Type | Time (s) | Comparisons | Movements |\n")
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")
        for result in results:
            f.write("| {:14} | {:7} | {:11} | {:8.2e} | {:11} | {:9} |\n".format(
                result['method'],
                result['size'],
                result['vector_type'],
                result['time'],
                result['comparisons'],
                result['movements']
            ))
        f.write("+----------------+---------+-------------+----------+-------------+-----------+\n")


def plot_comparison_results(results): # gráfico de comparações
    # Organizar dados por tamanho
    sizes = [100, 1000, 10000, 1000000]
    vector_types = ['OrdA', 'OrdC', 'OrdD']
    methods = ['Insertion Sort', 'Shell Sort', 'Selection Sort', 'Merge Sort', 'Heap Sort']

    # organiza a plotagem entre comparações e movimentos
    data = {}
    for size in sizes:
        data[size] = {}
        for vtype in vector_types:
            data[size][vtype] = {'comparisons': {}, 'movements': {}}

    # preenche os dados dos resultados na plotagem
    for result in results:
        size = result['size']
        vtype = result['vector_type']
        method = result['method']
        if size in sizes and vtype in vector_types:
            data[size][vtype]['comparisons'][method] = result['comparisons']
            data[size][vtype]['movements'][method] = result['movements']

    for size in sizes:
        if not any(data[size][vtype]['comparisons'] for vtype in vector_types):
            continue

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'Comparações e Movimentações por Algoritmo (Tamanho: {size})', fontsize=14)

        # Preparar dados para o gráfico
        available_methods = []
        comparisons_data = []
        movements_data = []

        # monta os gráficos se baseando no ordenamento aleatório, caso não tenha isso no input, considera o ordenamento crescente
        preferred_type = 'OrdA' if data[size]['OrdA']['comparisons'] else 'OrdC'

        for method in methods:
            if method in data[size][preferred_type]['comparisons']:
                available_methods.append(method.replace(' Sort', ''))
                comparisons_data.append(data[size][preferred_type]['comparisons'][method])
                movements_data.append(data[size][preferred_type]['movements'][method])

        if not available_methods:
            continue

        x_pos = np.arange(len(available_methods))

        # gráfico de comparações
        bars1 = ax1.bar(x_pos, comparisons_data, color='blue', alpha=0.7)
        ax1.set_title('Comparações')
        ax1.set_xlabel('Método')
        ax1.set_ylabel('Quantidade')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(available_methods)
        ax1.grid(True, alpha=0.3)

        # adicionar valores nas barras
        for bar, value in zip(bars1, comparisons_data):
            height = bar.get_height()
            ax1.annotate(f'{value:,}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom',
                         fontsize=8)

        # gráfico de movimentações
        bars2 = ax2.bar(x_pos, movements_data, color='red', alpha=0.7)
        ax2.set_title('Movimentações')
        ax2.set_xlabel('Método')
        ax2.set_ylabel('Quantidade')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(available_methods)
        ax2.grid(True, alpha=0.3)

        # adicionar valores nas barras
        for bar, value in zip(bars2, movements_data):
            height = bar.get_height()
            ax2.annotate(f'{value:,}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom',
                         fontsize=8)

        # legenda com o tipo de array
        fig.text(0.02, 0.02,
                 f'Tipo de vetor: {preferred_type} ({"Aleatório" if preferred_type == "OrdA" else "Crescente"})',
                 fontsize=10, style='italic')

        plt.tight_layout()
        plt.savefig(f'sorting_comparison_{size}.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    input_file = 'input.txt'
    instructions = read_input_file(input_file)
    results = []

    print("Executando algoritmos de ordenação...")
    for instruction in instructions:
        # verifica se o input tem 3 instruções
        if len(instruction) != 3:
            print(f"Linha inválida: {instruction}")
            continue

        method, size, vector_type = instruction
        try: # verifica se o tamanho está conforme solicitado na prova 100 1000 10000 1000000
            size = int(size)
        except ValueError:
            print(f"Tamanho inválido: {size}")
            continue

        print(f"Executando {method} com tamanho={size} tipo={vector_type}")
        array = generate_vector(size, vector_type)
        start = time.time()
        comparisons, movements = call_sort_function(method, list(array))
        end = time.time()
        elapsed_time = end - start

        results.append({
            'method': format_method_name(method),
            'size': size,
            'vector_type': vector_type,
            'time': elapsed_time,
            'comparisons': comparisons,
            'movements': movements
        })

    write_output_file(results)
    print("Resultados salvos em output.txt")

    print("Gerando gráficos comparativos...")
    plot_comparison_results(results)

    # Criar gráfico de escalabilidade
    sizes = [100, 1000, 10000, 1000000]
    vector_types = ['OrdA', 'OrdC', 'OrdD']
    methods = ['Insertion Sort', 'Shell Sort', 'Selection Sort', 'Merge Sort', 'Heap Sort']

    # Organizar dados
    data = {}
    for size in sizes:
        data[size] = {}
        for vtype in vector_types:
            data[size][vtype] = {'comparisons': {}, 'movements': {}}

    for result in results:
        size = result['size']
        vtype = result['vector_type']
        method = result['method']
        if size in sizes and vtype in vector_types:
            data[size][vtype]['comparisons'][method] = result['comparisons']
            data[size][vtype]['movements'][method] = result['movements']

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    method_colors = {method: colors[i] for i, method in enumerate(methods)}

    print("Gráficos salvos como:")
    print("- sorting_comparison_100.png")
    print("- sorting_comparison_1000.png")
    print("- sorting_comparison_10000.png")
    print("- sorting_comparison_1000000.png")
    print("################ CONFIGS DO PC ################")
    print("SO: Fedora")
    print("CPU: Intel Core i5-12450HX")
    print("RAM: 16GB")
    print("Python: 3.10.1")
    print("################################################")

if __name__ == "__main__":
    main()