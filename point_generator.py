#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:31:57 2018

@author: ellereyireland1 & vinul_wimalaweera
"""

import numpy as np


class System:
    def __init__(self):
        self.nodes = None
        self.distance_matrix = None
        self.inflow = None
        self.outflow = None

    def random_system(self, node_number):
        self.nodes = self.generate_nodes(node_number)
        self.distance_matrix = self.calculate_distance_matrix()
        self.inflow = self.add_inflow(10)
        self.outflow = self.add_outflow(10)

    def set_nodes(self, nodes):
        """
        Set nodes as 1D numpy array
        """
        self.nodes = nodes

    def set_distance_matrix(self):
        """
        Set distance matrix using nodes
        """
        self.distance_matrix = self.calculate_distance_matrix()

    def set_inflow(self, inflow):
        """
        Set inflow (1D numpy array)
        """
        self.inflow = inflow

    def set_outflow(self, outflow):
        """
        Set outflow (1D numpy array)
        """
        self.outflow = outflow

    def generate_nodes(self, node_number):
        return np.linspace(0, 100, node_number)

    def calculate_distance_matrix(self):
        return calculate_1d_dist_matrix(self.nodes)

    def add_inflow(self, avg_value):
        """
        Generate inflow as a random sample averaging on avg_value
        avg_value : float
        """
        return np.random.normal(avg_value, avg_value / 10.0, len(self.nodes))

    def add_outflow(self, avg_value):
        """
        Generate outflow as a random sample averaging on avg_value
        avg_value : float
        """
        return np.random.normal(avg_value, avg_value / 10.0, len(self.nodes))


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
