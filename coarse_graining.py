import numpy as np
import system as sys


class Coarse_graining:
    """
    Throw an imaginary grid on the nodes and regroup.
    Then return the new metric and other properties of the
    original system.
    Change the double list comprehension to make it more readable.
    """
    def __init__(self, system, number_of_areas):
        self.system = system
        self.boundaries = _calculate_boundaries(number_of_areas)

    def set_system(self, new_sytem):
        self.system = new_sytem

    def get_cell_area(self):
        return (self.boundaries[1] - self.boundaries[0]) ** 2

    def set_number_of_segments(self, number_areas):
        self.boundaries = __calculate_boundaries(number_areas)

    def get_node_positions(self):
        return np.digitize(self.system.nodes, self.boundaries)

    def group_node_positions(self, node_positions):
        """
        Group the nodes by the common positions in the new coarse grained system.

        Note they are grouped by their index in system.nodes.
        """
        unique_positions = np.unique(node_positions, axis=0)
        indices = []

        for i, unique in enumerate(unique_positions):
            indices.append(np.where((node_positions == unique).all(axis=1))[0])
        return np.array(indices)

    def get_new_nodes(self, grouped_indices):
        new_nodes = np.empty(len(grouped_indices), dtype=np.ndarray)

        for i, indices in enumerate(grouped_indices):
            nodes = self.system.nodes[indices]
            mass = self.system.inflow[indices] + self.system.outflow[indices]
            new_nodes[i] = _combined_position(nodes, mass)
        return new_nodes

    def get_new_flow(self, grouped_indices):
        sys_length = len(grouped_indices)
        new_flow = np.zeros((sys_length, sys_length))
        for i, indices in enumerate(grouped_indices):
            for j, other_indices in enumerate(grouped_indices):
                if i == j:
                    new_flow[i, j] == 0.0
                else:
                    new_flow[i, j] = np.sum(self.system.flow_matrix[indices][:, other_indices])
        return new_flow

    def get_new_inflow(self, new_flow):
        return np.sum(new_flow, axis=1)

    def get_new_outlfow(self, new_flow):
        return np.sum(new_flow, axis=0)

    def generate_new_system(self):
        node_positions = self.get_node_positions()
        grouped_indices = self.group_node_positions(node_positions)

        new_nodes = self.get_new_nodes(grouped_indices)
        new_flow = self.get_new_flow(grouped_indices)
        new_inflows = self.get_new_inflow(new_flow)
        new_outflows = self.get_new_outlfow(new_flow)

        system = sys.System()
        system.set_nodes(np.array(new_nodes))
        system.set_distance_matrix()
        system.set_inflow(np.array(new_inflows))
        system.set_outflow(np.array(new_outflows))
        system.set_flow_matrix(new_flow)
        return system


def _calculate_boundaries(number_areas, box_size=1.01):
        return np.linspace(0, box_size, number_areas + 1)


def _combined_position(nodes, masses=None):
    if masses is None:
        return np.mean(nodes, axis=0)
    return np.dot(masses, nodes) / np.sum(masses)

def combine_flow_matrix(system, indices_bins):
    sys_length = len(indices_bins)
    new_flow = np.zeros((sys_length, sys_length))
    for i, indices in enumerate(indices_bins):
        for j, other_indices in enumerate(indices_bins):
            if i == j:
                new_flow[i, j] == 0.0
            else:
                new_flow[i, j] = np.sum(system.flow_matrix[indices][:, other_indices])
    return new_flow
