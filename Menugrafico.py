import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import os

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, source, destination):
        self.adj_matrix[source][destination] = 1
        self.adj_matrix[destination][source] = 1

    def bfs(self, start_vertex):
        visited = [False] * self.num_vertices
        queue = deque([start_vertex])
        visited[start_vertex] = True

        while queue:
            vertex = queue.popleft()
            print(vertex, end=" ")

            for adjacent_vertex in range(self.num_vertices):
                if self.adj_matrix[vertex][adjacent_vertex] == 1 and not visited[adjacent_vertex]:
                    queue.append(adjacent_vertex)
                    visited[adjacent_vertex] = True

    def is_connected(self):
        visited = [False] * self.num_vertices
        self.dfs(0, visited)

        return all(visited)

    def dfs(self, vertex, visited):
        visited[vertex] = True

        for adjacent_vertex in range(self.num_vertices):
            if self.adj_matrix[vertex][adjacent_vertex] == 1 and not visited[adjacent_vertex]:
                self.dfs(adjacent_vertex, visited)

    def is_bipartite(self):
        color = [-1] * self.num_vertices
        queue = deque()

        for start_vertex in range(self.num_vertices):
            if color[start_vertex] == -1:
                queue.append(start_vertex)
                color[start_vertex] = 0

                while queue:
                    vertex = queue.popleft()

                    for adjacent_vertex in range(self.num_vertices):
                        if self.adj_matrix[vertex][adjacent_vertex] == 1 and color[adjacent_vertex] == -1:
                            color[adjacent_vertex] = 1 - color[vertex]
                            queue.append(adjacent_vertex)
                        elif self.adj_matrix[vertex][adjacent_vertex] == 1 and color[adjacent_vertex] == color[vertex]:
                            return False

        return True


# Função para ler as matrizes de adjacência de um arquivo
def read_adjacency_matrices(file_path):
    matrices = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_matrix = []

        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                current_matrix.append(list(map(int, stripped_line.split())))
            elif current_matrix:
                matrices.append(current_matrix)
                current_matrix = []

        if current_matrix:
            matrices.append(current_matrix)

    return matrices


# Função auxiliar para construir um grafo a partir de uma matriz de adjacência
def build_graph(adj_matrix):
    num_vertices = len(adj_matrix)
    graph = Graph(num_vertices)
    for i in range(num_vertices):
        for j in range(num_vertices):
            if adj_matrix[i][j] == 1:
                graph.add_edge(i, j)
    return graph


def is_connected_action():
    selected_matrix = matrices[matrix_listbox.curselection()[0]]
    selected_graph = build_graph(selected_matrix)
    is_connected = selected_graph.is_connected()
    message = "O grafo é conexo." if is_connected else "O grafo não é conexo."
    messagebox.showinfo("Verificar Conectividade", message)
    plot_graph(selected_graph.adj_matrix)


def bfs_action():
    os.system('clear') or None
    selected_matrix = matrices[matrix_listbox.curselection()[0]]
    selected_graph = build_graph(selected_matrix)

    # Obter o vértice inicial da busca em largura a partir do usuário
    vertice_inicial = int(entry_vertice_inicial.get())

    # Verificar se o vértice inicial é válido
    if 0 <= vertice_inicial < selected_graph.num_vertices:
        # Realizar a busca em largura
        selected_graph.bfs(vertice_inicial)
        plot_graph(selected_graph.adj_matrix)
    else:
        messagebox.showerror("Vértice Inicial Inválido", "O vértice inicial fornecido é inválido.")


def is_bipartite_action():
    selected_matrix = matrices[matrix_listbox.curselection()[0]]
    selected_graph = build_graph(selected_matrix)
    is_bipartite = selected_graph.is_bipartite()
    message = "O grafo é bipartido." if is_bipartite else "O grafo não é bipartido."
    messagebox.showinfo("Verificar Bipartição", message)
    plot_graph(selected_graph.adj_matrix)


def plot_graph(adj_matrix):
    G = nx.Graph()

    for i in range(len(adj_matrix)):
        G.add_node(i)

    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='orange')
    plt.show()


# Exemplo de uso
if __name__ == "__main__":
    matrices = read_adjacency_matrices("grafos.txt")

    root = tk.Tk()
    root.title("Menu de Opções")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    label = tk.Label(frame, text="Selecione uma matriz de adjacência:")
    label.pack()

    matrix_listbox = tk.Listbox(frame, width=30)
    matrix_listbox.pack(pady=10)

    for i, matrix in enumerate(matrices):
        matrix_listbox.insert(tk.END, f"Matriz {i + 1}")

    def select_matrix(event):
        selection = matrix_listbox.curselection()
        if selection:
            matrix_index = selection[0]
            selected_matrix = matrices[matrix_index]
            selected_graph_label.config(text=f"Matriz Selecionada: Matriz {matrix_index + 1}")

    matrix_listbox.bind("<<ListboxSelect>>", select_matrix)

    selected_graph_label = tk.Label(frame, text="Matriz Selecionada: ")
    selected_graph_label.pack()

    vertice_inicial_label = tk.Label(frame, text="Vértice Inicial:")
    vertice_inicial_label.pack()

    entry_vertice_inicial = tk.Entry(frame)
    entry_vertice_inicial.pack()

    def show_is_connected():
        if matrix_listbox.curselection():
            is_connected_action()

    def show_bfs():
        if matrix_listbox.curselection():
            bfs_action()

    def show_is_bipartite():
        if matrix_listbox.curselection():
            is_bipartite_action()

    is_connected_button = tk.Button(root, text="Verificar Conectividade", command=show_is_connected)
    is_connected_button.pack()

    bfs_button = tk.Button(root, text="Aplicar Busca em Largura", command=show_bfs)
    bfs_button.pack()

    is_bipartite_button = tk.Button(root, text="Verificar Bipartição", command=show_is_bipartite)
    is_bipartite_button.pack()

    root.mainloop()
