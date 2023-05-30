import json
import random
import uuid
import os

class Generator:

    def __init__(self, size=1):
        self.write_path = ''
        self.size = size
        self.graph = {}
        self.ids = set()
        self.rd = random.Random()

    def set_path(self, write_path=''):
        if not write_path:
            self.write_path = './project/test_bank/'
        
    def generate_tsp(self):
        self.generate_ids()
        self.initialize_graph_keys()
        self.generate_complete_connections()

    def write_graph(self):
        latest_version = self.get_latest_version()
        latest_version = str(int(latest_version) + 1)
        file_name = 'size_' + str(self.size) + '_version_' + latest_version + '.json'
        with open(self.write_path + file_name, 'w') as file:
            json.dump(self.graph, file)


    def get_latest_version(self):
        latest_version = 0
        for path, dirnames, filenames in os.walk(self.write_path):
            for file in filenames:
                if 'json' not in file:
                    continue
            if 'size_' + str(self.size) in file:
                latest_version = file.split('version_')[-1].split('.')[0]
        return latest_version


    def generate_ids(self):
        self.rd.seed(0)
        for i in range(self.size):
            id = uuid.UUID(int=self.rd.getrandbits(128), version=4)
            hex_id = id.hex[:8]
            if hex_id in self.ids:
                print('Duplicate:', hex_id)
                continue
            self.ids.add(hex_id)

    def initialize_graph_keys(self):
        for i in self.ids:
            self.graph[i] = {}
    
    def generate_complete_connections(self):
        for idx_i, i in enumerate(self.ids):
            for idx_j, j in enumerate(self.ids):
                if idx_i <= idx_j:
                    continue
                if j not in self.graph[i]:
                    self.graph[i][j] = 0
                self.graph[i][j] = self.get_random_rounded_distance()
                self.graph[j][i] = self.graph[i][j]
                
    def get_random_rounded_distance(self):
        return round(self.rd.random() * 100, 2)

if __name__ == '__main__':
    size = 5
    generator = Generator(size)
    generator.set_path()
    generator.generate_tsp()
    generator.write_graph()

