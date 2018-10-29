#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:31:57 2018

@author: ellereyireland1
"""

import point_generator as pg
import numpy as np

class Gravity:
    def __init__(self):
        self.system = pg.System(10)
        self.A = np.full(10, 1)
        self.B = np.full(10, 1)
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

    def tuning_function(self, idx, i=True):
        if i == True:
            metric_slice = self.metric[idx, :]
        else:
            metric_slice = self.metric[:, idx]

        return metric_slice

        print(metric_slice)
