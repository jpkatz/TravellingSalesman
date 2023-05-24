class Generator2:

    def __init__(self, graph) -> None:
        self.graph = graph

    def generate_2_combo(self):
        for city_i, connections in self.graph.items():
            for city_j, distance in connections.items():
                print('Create Fragment class consisting of city_i and city_j')
