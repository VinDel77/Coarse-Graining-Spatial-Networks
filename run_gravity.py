#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:31:57 2018

@author: ellereyireland1 & vinul_wimalaweera
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class Gravity:
    def __init__(self):
        self.system = None
        self.metric = None
        self.A = None
        self.B = None
        self.cost = None

    def set_system(self, system, distance = None):
        self.system = system
        self.metric = self.metric_function(distance)
        node_number = len(system.nodes)
        self.A = np.random.normal(np.mean(self.metric), np.std(self.metric),
                                  node_number)
        self.B = np.random.normal(np.mean(self.metric), np.std(self.metric),
                                  node_number)


    def set_flows(self):
        self.system.flow_matrix = self.calculate_flow_matrix()
        self.total_flow = self.calculate_total_flow()

    def metric_function(self, mean_distance = None, func = None):
        matrix = np.zeros_like(self.system.distance_matrix)
        index_range = range(len(self.system.nodes))
        if func == None:
            if mean_distance == None:
                average_distance = np.mean(self.system.distance_matrix)
            else:
                average_distance = mean_distance
            for i in index_range:
                for j in index_range[i:]:
                    metric_ij = np.exp(-self.system.distance_matrix[i, j] /
                                       average_distance)
                    matrix[i, j] = metric_ij
                    matrix[j, i] = metric_ij
            return matrix
        else:
            if mean_distance == None:
                average_distance = np.mean(self.system.distance_matrix)
            else:
                average_distance = mean_distance
            for i in index_range:
                for j in index_range[i:]:
                    metric_ij = func(-self.system.distance_matrix[i, j] /
                                       average_distance)
                    matrix[i, j] = metric_ij
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
        self.A = a_values[-1]
        self.B = b_values[-1]

#        self.plot_results(a_values, b_values, products)
        return a_values, b_values, products


    def calculate_flow_matrix(self):
        matrix = np.zeros_like(self.system.distance_matrix)
        index_range = range(len(self.system.nodes))
        for i in index_range:
            for j in index_range:
                if i == j:
                    flow_ij = 0.0
                else:
                    flow_ij = self.A[i]*self.B[j]*self.system.outflow[i]*self.system.inflow[j]*self.metric[i,j]
                matrix[i,j] = flow_ij
        return matrix

    def calculate_total_flow(self):
        return 0.5*np.sum(self.system.flow_matrix)


    def plot_results(self, a_values, b_values, products):
        matplotlib.rcParams.update({'font.size':18})
        x_axis = range(len(a_values))
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x_axis, a_values[:, 0], '--', color='grey', lw=2.5, label='A values')
        ax.plot(x_axis, b_values[:, 0], ':', color='grey', lw=2.5, label='B values')
        ax.set_ylabel("Constant Value")
        ax.set_xlabel('Iteration')

        plt.legend(loc=(0.7, 0.5))

        ax2 = ax.twinx()
        ax2.plot(x_axis, products[:, 0], 'kx-', lw=2.5, label='Ratio of A*B')
        ax2.set_ylabel("Product Value")
        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        plt.legend(loc=(0.7, 0.40))

        plt.show()

    def converging(self, product_ab_list, tolerance):
        if len(product_ab_list) < 10:
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

    def total_flow(self):
        """
        returns the value of the total flow across the entire system
        """
        return 0.5* np.sum(self.total_flow)

    def cost_function(self, original_flows, new_flows):
        sum_of_costs = 0
        index_range = range(original_flows.shape[0])
        for i in index_range:
            for j in index_range:
                sum_of_costs += (original_flows[i,j] - new_flows[i,j])**2
        self.cost = sum_of_costs
