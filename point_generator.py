import numpy as np

class System:
    def __init__(self, node_number):
        self.nodes = self.generate_nodes(node_number)

    def generate_nodes(self, node_number):
        return np.linspace(0, 100, node_number)
