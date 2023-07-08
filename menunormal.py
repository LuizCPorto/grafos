import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import os 

class Grafo:
    def __init__(self, arquivo):
        self.matrizes_adjacencia = self.ler_matrizes_adjacencia(arquivo)

    def ler_matrizes_adjacencia(self, arquivo):
        matrizes = []
        with open(arquivo, 'r') as file:
            linhas = file.readlines()
            matriz_atual = []
            for linha in linhas:
                if linha.strip():  # Verifica se a linha não está em branco
                    valores = [int(x) for x in linha.split()]
                    matriz_atual.append(valores)
                else:
                    if matriz_atual:
                        matrizes.append(matriz_atual)
                        matriz_atual = []
            if matriz_atual:
                matrizes.append(matriz_atual)
        return matrizes

    def adicionar_aresta(self, matriz, origem, destino):
        matriz[origem][destino] = 1
        matriz[destino][origem] = 1

    def plotar_grafo(self, matriz):
        if not self.validar_matriz_adjacencia(matriz):
            print("Matriz de adjacência inválida.")
            return

        G = nx.Graph()

        # Adiciona os vértices ao grafo
        num_vertices = len(matriz)
        G.add_nodes_from(range(num_vertices))

        # Adiciona as arestas ao grafo
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if matriz[i][j] == 1:
                    G.add_edge(i, j)

        # Plota o grafo
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color='skyblue',
            node_size=500,
            edge_color='black',
            linewidths=1,
            font_size=10
        )
        plt.show()

    def verificar_conexo(self, matriz):
        if not self.validar_matriz_adjacencia(matriz):
            print("Matriz de adjacência inválida.")
            return False

        num_vertices = len(matriz)
        visitados = [False] * num_vertices

        # Faz uma busca em profundidade a partir do vértice 0
        self.dfs(matriz, 0, visitados)

        # Verifica se todos os vértices foram visitados
        return all(visitados)

    def dfs(self, matriz, vertice, visitados):
        visitados[vertice] = True
        for i in range(len(matriz)):
            if matriz[vertice][i] == 1 and not visitados[i]:
                self.dfs(matriz, i, visitados)

    def buscar_largura(self, matriz, vertice_inicial):
        if not self.validar_matriz_adjacencia(matriz):
            print("Matriz de adjacência inválida.")
            return

        num_vertices = len(matriz)
        visitados = [False] * num_vertices
        fila = deque()

        # Marca o vértice inicial como visitado e adiciona na fila
        visitados[vertice_inicial] = True
        fila.append(vertice_inicial)

        while fila:
            vertice_atual = fila.popleft()
            print(vertice_atual, end=" ")

            for i in range(num_vertices):
                if matriz[vertice_atual][i] == 1 and not visitados[i]:
                    visitados[i] = True
                    fila.append(i)

    def encontrar_biparticao(self, matriz):
        if not self.validar_matriz_adjacencia(matriz):
            print("Matriz de adjacência inválida.")
            return

        num_vertices = len(matriz)
        cores = [-1] * num_vertices
        bipartido = True

        for vertice in range(num_vertices):
            if cores[vertice] == -1:
                bipartido &= self.bipartir(matriz, vertice, cores)

        if bipartido:
            print("O grafo é bipartido.")
            grupos = {}
            for i in range(num_vertices):
                if cores[i] not in grupos:
                    grupos[cores[i]] = []
                grupos[cores[i]].append(i)
            print("Grupos:", grupos)
        else:
            print("O grafo não é bipartido.")

    def bipartir(self, matriz, vertice, cores):
        cores[vertice] = 1

        fila = deque()
        fila.append(vertice)

        while fila:
            vertice_atual = fila.popleft()

            for i in range(len(matriz)):
                if matriz[vertice_atual][i] == 1 and cores[i] == -1:
                    cores[i] = 1 - cores[vertice_atual]
                    fila.append(i)
                elif matriz[vertice_atual][i] == 1 and cores[i] == cores[vertice_atual]:
                    return False

        return True

    def validar_matriz_adjacencia(self, matriz):
        num_vertices = len(matriz)
        for linha in matriz:
            if len(linha) != num_vertices:
                return False
        return True


# Função para exibir o menu
def exibir_menu():
    print("Escolha uma opção:")
    print("1. Verificar se o grafo é conexo")
    print("2. Aplicar Busca em Largura")
    print("3. Encontrar Bipartição")
    print("0. Sair")


# Exemplo de utilização
arquivo = 'grafos.txt'
grafo = Grafo(arquivo)

# Variável para controle do loop do menu
continuar = True

while continuar:    
    os.system('clear') or None
    exibir_menu()
    opcao = input("Opção: ")

    if opcao == "1":
        for idx, matriz in enumerate(grafo.matrizes_adjacencia, start=1):
            print(f"Matriz {idx}")
        matricula_escolhida = int(input("Digite o número da matriz que deseja utilizar: "))
        if 1 <= matricula_escolhida <= len(grafo.matrizes_adjacencia):
            matriz = grafo.matrizes_adjacencia[matricula_escolhida - 1]
            print(f"Matriz selecionada:{matricula_escolhida}")
            if grafo.verificar_conexo(matriz):
                print("O grafo é conexo.")
            else:
                print("O grafo não é conexo.")
            grafo.plotar_grafo(matriz)
        else:
            print("Número de matriz inválido.")
        input("Pressione Enter para continuar...")

    elif opcao == "2":
        for idx, matriz in enumerate(grafo.matrizes_adjacencia, start=1):
            print(f"Matriz {idx}")
        matricula_escolhida = int(input("Digite o número da matriz que deseja utilizar: "))
        if 1 <= matricula_escolhida <= len(grafo.matrizes_adjacencia):
            matriz = grafo.matrizes_adjacencia[matricula_escolhida - 1]
            print(f"Matriz selecionada: {matricula_escolhida}")
            vertice_inicial = int(input("Digite o vértice inicial: "))
            print("Caminho em largura:")
            grafo.buscar_largura(matriz, vertice_inicial)
            grafo.plotar_grafo(matriz)
        else:
            print("Número de matriz inválido.")
        input("Pressione Enter para continuar...")

    elif opcao == "3":
        for idx, matriz in enumerate(grafo.matrizes_adjacencia, start=1):
            print(f"Matriz {idx}")
        matricula_escolhida = int(input("Digite o número da matriz que deseja utilizar: "))
        if 1 <= matricula_escolhida <= len(grafo.matrizes_adjacencia):
            matriz = grafo.matrizes_adjacencia[matricula_escolhida - 1]
            print(f"Matriz selecionada: {matricula_escolhida}")
            print("Encontrar bipartição:")
            grafo.encontrar_biparticao(matriz)
            grafo.plotar_grafo(matriz)
        else:
            print("Número de matriz inválido.")
        input("Pressione Enter para continuar...")

    elif opcao == "0":
        continuar = False

    else:
        print("Opção inválida. Por favor, digite uma opção válida.")
        input("Pressione Enter para continuar...")
