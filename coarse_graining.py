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
        self.total_flow = self.system.total_flow

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

    def centre_of_mass(self, nodes, masses):
        return np.dot(masses, nodes) / np.sum(masses)

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

