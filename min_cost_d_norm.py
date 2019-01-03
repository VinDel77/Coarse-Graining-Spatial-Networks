#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 18:28:29 2018

@author: ellereyireland1
"""

import system as sys
import run_gravity as g
import numpy as np
import coarse_graining as cg
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import save

for i in tqdm(range(1,5)):
    #Make the system
    s = g.Gravity()
    system = sys.System()
    # set normal to False to use zipf distribution for city size
    system.random_system(1000, normal=True)

    #set the lists that will contain the data points
    cell_areas = []
    min_cost_values =[]

    #set up the original system
    s.set_system(system)
    s.tuning_function()
    s.set_flows()

    #Coarse grain the system
    for level in tqdm(range(2,22)):
        distances = []
        cost_values = []
        coarse_grainer = cg.Coarse_graining(system, level)
        cell_area = coarse_grainer.get_cell_area()
        cell_areas.append(cell_area)
        grained_system = coarse_grainer.generate_new_system()
        original_flows = grained_system.flow_matrix
        #get the mean value from the distance matrix and set the bounds
        mean_dist = np.mean(grained_system.distance_matrix)
        bound = np.sqrt(mean_dist)
        distances = list(np.linspace(0.01, mean_dist + 3*bound, 100))

        # for each value of distance chosen, rerun the tuning on grained system

        for d in distances:
            s.set_system(grained_system, distance =d)
            s.tuning_function()
            s.set_flows()
            grained_flows = grained_system.flow_matrix
            s.cost_function(original_flows, grained_flows)
            cost_values.append(s.cost)
        min_cost_values.append(distances[np.argmin(cost_values)])

    save.save_object(min_cost_values, "cost_value_array_norm_{}".format(i), skip_dialogue = True)
    save.save_object(cell_areas, "cell_area_array_norm_{}".format(i), skip_dialogue = True)
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.plot(cell_areas, min_cost_values, 'ro')
    #ax.set_xlabel("Cell area")
    #ax.set_ylabel("Value of minimum cost function")
    #plt.show()
