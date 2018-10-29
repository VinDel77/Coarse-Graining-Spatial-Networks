#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:31:57 2018

@author: ellereyireland1 & vinul_wimalaweera
"""

import point_generator as pg
import numpy as np
import matplotlib.pyplot as plt

class Gravity:
    def __init__(self):
        node_number = 20
        self.system = pg.System(node_number)
        self.A = np.full(node_number, 1)
        self.B = np.full(node_number, 1)
        self.metric = self.metric_function()

    def metric_function(self):
        matrix = np.zeros_like(self.system.distance_matrix)
        index_range = range(len(self.system.nodes))
        for i in index_range:
            for j in index_range[i:]:
                metric_ij = np.exp(-self.system.distance_matrix[i,j])
                matrix[i,j] = metric_ij
                matrix[j, i] = metric_ij

        return matrix

    def tuning_function(self):
        a_values = []
        b_values = []
        for i in range(100):
            new_a = self.calculate_new_a_b(a=True)
            self.A = new_a
            a_values.append(new_a)

            new_b = self.calculate_new_a_b(a=False)
            self.B = new_b
            b_values.append(new_b)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        print(len(a_values))
        print(len(b_values))
        x_axis = range(len(a_values))
        ax.plot(x_axis, a_values, 'ro')
        ax.plot(x_axis, b_values, 'bo')

        plt.show()

    def calculate_new_a_b(self, a=True):
        index_range = range(len(self.A))
        for idx in index_range:
            if a == True:
                metric_slice = self.metric[idx, :]
            else:
                metric_slice = self.metric[:, idx]

            a_dot_b = np.dot(self.A, self.B)
            inverse_a_b =  a_dot_b * metric_slice
        return 1.0/inverse_a_b
