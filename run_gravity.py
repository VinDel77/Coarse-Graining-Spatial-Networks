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
    def __init__(self, iterations, node_number):
        self.iterations = iterations
        self.system = pg.System(node_number)
        self.metric = self.metric_function()
        self.A = np.random.normal(np.mean(self.metric), np.std(self.metric), node_number)
        self.B = np.random.normal(np.mean(self.metric), np.std(self.metric), node_number)

    def metric_function(self):
        matrix = np.zeros_like(self.system.distance_matrix)
        index_range = range(len(self.system.nodes))
        average_distance = np.mean(self.system.distance_matrix)
        for i in index_range:
            for j in index_range[i:]:
                metric_ij = np.exp(-self.system.distance_matrix[i,j] / average_distance)
                matrix[i,j] = metric_ij
                matrix[j, i] = metric_ij
        return matrix

    def tuning_function(self):
        a_values = []
        b_values = []
        x_axis = []
        for _ in range(self.iterations):
            new_a = self.calculate_new_a_b(self.B, self.system.inflow, self.metric, sum_over='i')
            a_values.append(new_a[0])

            new_b = self.calculate_new_a_b(self.A, self.system.outflow, self.metric, sum_over='j')
            b_values.append(new_b[0])
            x_axis.append(_)

            self.B = new_b
            self.A = new_a

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x_axis, a_values, 'ro', label='A values')
        ax.plot(x_axis, b_values, 'bo', label='B values')

        plt.legend()

        plt.show()

    def calculate_new_a_b(self, x, f, metric, sum_over='i'):
        """
        Calculate the iterated x where x is either A, B .
        args:
            x = either A or B as a 1d array
            f = inflow or outflow as a 1d array
            metric = metric as a 2D symmetric array
            sum_over = Sum over row (i) or column (j) of metric
        """
        return 1.0 / np.einsum('ij,{}'.format(sum_over), metric, x * f)
