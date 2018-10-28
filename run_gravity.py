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
        index_range = len(self.system.nodes)
        for i in index_range:
            for j in index_range[i:]:
                matrix[i, j] = np.exp(-self.system.distance_matrix[i,j])
            
    def tuning_function(self):
        pass