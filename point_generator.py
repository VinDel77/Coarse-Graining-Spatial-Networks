import numpy as np

class System:
    def __init__(self, node_number):
        self.nodes = self.generate_nodes(node_number)
        self.distance_matrix = self.calculate_distance_matrix()

    def generate_nodes(self, node_number):
        return np.linspace(0, 100, node_number)

    def calculate_distance_matrix(self):
        self.distance_matrix = calculate_1d_dist_matrix(self.nodes)


def calculate_1d_dist_matrix(positions):
    """
    Calculate the distance matrix in 1d.

    For 2D  think about using:
        scipy.spatial.distance_matrix
    """
    len_indices = len(positions)
    distance_matrix = np.zeroes((len_indices, len_indices))

    index_range = range(len_indices)

    for i in index_range:
        for j in index_range[i,]:
            dist = abs(positions[i] - positions[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist

