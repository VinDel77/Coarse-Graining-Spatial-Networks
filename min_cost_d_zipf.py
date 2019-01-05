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
import minimise as m
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
import save

cell_areas_full = []
min_cost_values_full =[]
for i in tqdm(range(50)):
    cell_areas = []
    min_cost_values = []
    #Make the system
    s = g.Gravity()
    system = sys.System()
    # set normal to False to use zipf distribution for city size
    system.random_system(1000, normal=False)

    #set the lists that will contain the data points

    #set up the original system
    s.set_system(system)
    s.tuning_function()
    s.set_flows()

    #Coarse grain the system
    levels = [3, 4, 5, 6, 8, 13, 16, 20, 22, 30]
    for level in levels:
        distances = []
        cost_values = []
        coarse_grainer = cg.Coarse_graining(system, level)
        cell_area = coarse_grainer.get_cell_area()
        cell_areas.append(cell_area)
        grained_system = coarse_grainer.generate_new_system()
        original_flows = grained_system.flow_matrix
        #get the mean value from the distance matrix and set the bounds
        min_cost_value = m.find_minimum_sp(grained_system, s, original_flows)
        min_cost_values.append(min_cost_value)

    cell_areas_full.append(cell_areas)
    min_cost_values_full.append(min_cost_values)

#    save.save_object(min_cost_values, "cost_value_array_norm_{}".format(i), skip_dialogue = True)
#    save.save_object(cell_areas, "cell_area_array_norm_{}".format(i), skip_dialogue = True)

now = datetime.now().strftime('%d%m%H%M%S')
save.save_object(min_cost_values_full, "cost_value_zipf"+now, skip_dialogue=True)
save.save_object(cell_areas_full, "cell_area_zipf"+now, skip_dialogue=True)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(cell_areas, min_cost_values, 'ro')
ax.set_xlabel("Cell area")
ax.set_ylabel("Value of minimum cost function")
plt.show()
