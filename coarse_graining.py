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
        self.boundaries = np.linspace(0, 1.01, number_of_areas + 1)

    def stack(self, indicies, vector):
        return np.vstack((indicies, vector)).T

    def amalgamate(self, bin_vector, func):
        return np.array([func(bin_vector[bin_vector[:, 0] == i, 1]) for i in np.unique(bin_vector[:, 0])])

    def elements_in_bin(self, nodes_bin_indices, bin_indices, com=False):
        indices_filter = [np.array_equal(i, bin_indices) for i in nodes_bin_indices]
        nodes_in_bin = self.system.nodes[indices_filter]
        inflow_in_bin = self.system.inflow[indices_filter]
        outflow_in_bin = self.system.outflow[indices_filter]

        inflow = np.sum(inflow_in_bin)
        outflow = np.sum(outflow_in_bin)

        if com:
            node_position = self.centre_of_mass(nodes_in_bin, inflow_in_bin + outflow_in_bin)
        else:
            node_position = np.mean(nodes_in_bin, axis=0)

        return node_position, inflow, outflow

    def centre_of_mass(nodes, masses):
        return np.sum(nodes * masses, axis=0) / np.sum(masses)

    def generate_new_system_old(self):
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

    def generate_new_system(self, com=True):
        nodes = self.system.nodes
        bins = self.boundaries

        nodes_bin_indices = np.digitize(nodes, bins)
        unique_bins = np.unique(nodes_bin_indices, axis=0)

        new_nodes = []
        new_inflows = []
        new_outflows = []

        for uniq in unique_bins:
            node, inflow, outflow = self.elements_in_bin(nodes_bin_indices, uniq, com=com)
            new_nodes.append(node)
            new_inflows.append(inflow)
            new_outflows.append(outflow)

        system = pg.System()
        system.set_nodes(np.array(new_nodes))
        system.set_distance_matrix()
        system.set_inflow(np.array(new_inflows))
        system.set_outflow(np.array(new_outflows))
        return system

