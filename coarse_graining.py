import numpy as np
import point_generator as pg


class Coarse_graining:
    """
    Throw an imaginary grid on the nodes and regroup.
    Then return the new metric and other properties of the
    original system.
    Change the double list comprehension to make it more readable.
    """
    def __init__(self, system, number_of_areas):
        self.system = system
        self.boundaries = np.linspace(0, 100 + 1, number_of_areas + 1)

    def stack(self, indicies, vector):
        return np.vstack((indicies, vector)).T

    def amalgamate(self, bin_vector, func):
        return np.array([func(bin_vector[bin_vector[:, 0] == i, 1]) for i in np.unique(bin_vector[:, 0])])

    def generate_new_system(self):
        distance = self.system.nodes
        bins = self.boundaries
        nodes_bin_indicies = np.digitize(distance, bins)

        bin_number_nodes = self.stack(nodes_bin_indicies, distance)
        bin_number_outflow = self.stack(nodes_bin_indicies, self.system.outflow)
        bin_number_inflow = self.stack(nodes_bin_indicies, self.system.inflow)
        new_nodes = self.amalgamate(bin_number_nodes, np.mean)

        new_outflow = self.amalgamate(bin_number_outflow, np.sum)
        new_inflow = self.amalgamate(bin_number_inflow, np.sum)
        system = pg.System()
        system.set_nodes(new_nodes)
        system.set_distance_matrix()
        system.set_inflow(new_inflow)
        system.set_outflow(new_outflow)
        return system

