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
    def __init__(self, node_number):
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

    def tuning_function(self, iterations=1000, tolerance=0.0000001):
        a_values = []
        b_values = []
        products = []
        for _ in range(iterations):
            new_a = self.calculate_new_a_b(self.B, self.system.inflow, self.metric, sum_over='i')
            a_values.append(new_a)
            self.A = new_a

            new_b = self.calculate_new_a_b(self.A, self.system.outflow, self.metric, sum_over='j')
            b_values.append(new_b)
            self.B = new_b

            products.append(new_a * new_b)
            if self.converging(np.array(products), tolerance):
                break

        a_values = np.array(a_values)
        b_values = np.array(b_values)
        products = np.array(products)

#        self.plot_results(a_values, b_values, products)
        return a_values, b_values, products


    def plot_results(self, a_values, b_values, products):
        x_axis = range(len(a_values))
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x_axis, a_values[:, 0], 'ro', label='A values')
        ax.plot(x_axis, b_values[:, 0], 'bo', label='B values')

        plt.legend()

        ax2 = ax.twinx()
        ax2.plot(x_axis, products[:, 0], 'ko', label='Ratio of A*B')

        plt.legend()

        plt.show()

    def converging(self, product_ab_list, tolerance):
        if len(product_ab_list) < 5:
            return False

        value_range = np.ptp(product_ab_list[-5:, :], axis=0)
        if np.any(value_range > tolerance):
            return False
        return True

    def normalise_vector(self, vector):
        return vector / np.linalg.norm(vector)

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


class Coarse_graining:
    """
    Throw an imaginary grid on the nodes and regroup. 
    Then return the new metric and other properties of the
    original system.
    """
    def __init__(self, system, number_of_areas):
        self.system = system
        self.boundaries = np.linspace(0, 100 + 1, number_of_areas + 1)
        
    def generate_new_system(self):
        distance = self.distance
        bins = self.boundaries
        a = np.digitize(distance, bins)
        bin_number_to_position = np.vstack((np.digitize(distance, bins), distance)).T
        bin_number_to_outflow = np.vstack((np.digitize(distance, bins), self.outflow)).T
        bin_number_to_inflow = np.vstack((((np.digitize(distance, bins), self.inflow)).T))
        new_mean_distances = np.array([np.mean(A[A[:, 0] == i, 1]) for i in np.unique(A[:, 0])])
        
        

    
    
        
    
