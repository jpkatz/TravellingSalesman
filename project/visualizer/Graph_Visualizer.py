import networkx as nx
import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self, graph: dict):
        self.graph = graph
        self.nxG = self.create_graph()
        self.edges = self.create_edges()

    def create_graph(self):
        return nx.DiGraph()

    def build_graph(self):
        self.add_nodes()
        self.add_edges()

    def add_nodes(self):
        self.nxG.add_nodes_from(self.graph.keys())

    def create_edges(self):
        edges = []
        for source, destination in self.graph.items():
            edge = (source, destination)
            edges.append(edge)
        return edges

    def add_edges(self):
        self.nxG.add_edges_from(self.edges)

    def plot_graph(self):
        plt.figure(figsize=(12,12))
        nx.draw_networkx(
            self.nxG,
            with_labels=True,
            font_weight='bold'
        )
        plt.show()


if __name__ == '__main__':
    graph = {'A': 'B',
             'B': 'C',
             'C': 'A'
             }
    visualizer = Visualizer(graph)
    visualizer.build_graph()
    visualizer.plot_graph()


