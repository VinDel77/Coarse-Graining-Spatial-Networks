import numpy as np

class System:
    def __init__(self, node_number):
        self.nodes = self.generate_nodes(node_number)
        self.distance_matrix = self.calculate_distance_matrix()
        self.inflow = self.add_inflow()
        self.outflow = self.add_outflow()

    def generate_nodes(self, node_number):
        return np.linspace(0, 100, node_number)

    def calculate_distance_matrix(self):
        return calculate_1d_dist_matrix(self.nodes)
        
    def add_inflow(self):
        return np.full(len(self.nodes), 10)
    
    def add_outflow(self):
        return np.full(len(self.nodes), 10)


def calculate_1d_dist_matrix(positions):
    """
    Calculate the distance matrix in 1d.

    For 2D  think about using:
        scipy.spatial.distance_matrix
    """
    len_indices = len(positions)
    distance_matrix = np.zeros((len_indices, len_indices))

    index_range = range(len_indices)

    for i in index_range:
        for j in index_range[i:]:
            dist = abs(positions[i] - positions[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
            
    return distance_matrix

