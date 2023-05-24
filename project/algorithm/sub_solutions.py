import hashlib

class Fragment:

    def __init__(self):
        self.starting_node = None
        self.ending_node = None
        self.nodes = []
        self.cost = 0
        self.name = ''

    def add_node(self, node):
        self.nodes.append(node)

    def set_starting_node(self, node):
        self.starting_node = node

    def set_ending_node(self, node):
        self.ending_node = node

    def set_cost(self, cost):
        self.cost = cost

    def set_name(self):
        path_as_string = ''.join(self.nodes)
        hash_object = hashlib.sha256(path_as_string.encode())
        self.name = hash_object.hexdigest()

if __name__ == '__main__':
    fragment = Fragment()
    fragment.add_node('A')
    fragment.add_node('B')
    fragment.set_name()
    print(fragment.name)


    