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

#Make the system
s = g.Gravity()
system = sys.System()
# set normal to False to use zipf distribution for city size
system.random_system(1000, normal=False)

#set the lists that will contain the data points
distances = []
cost_values =[]

#set up the original system
s.set_system(system)
s.tuning_function()
s.set_flows()

#Coarse grain the system
coarse_grainer = cg.Coarse_graining(system, 5)
#cell_area = coarse_grainer.get_cell_area()
grained_system = coarse_grainer.generate_new_system()
original_flows = grained_system.flow_matrix
#get the mean value from the distance matrix and set the bounds
mean_dist = np.mean(grained_system.distance_matrix)
bound = np.sqrt(mean_dist)
distances = list(np.linspace(0.01, mean_dist + 5*bound, 1000))

# for each value of distance chosen, rerun the tuning on grained system

for d in tqdm(distances):
    s.set_system(grained_system, distance =d)
    s.tuning_function()
    s.set_flows()
    grained_flows = grained_system.flow_matrix
    s.cost_function(original_flows, grained_flows)
    cost_values.append(s.cost)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(distances, cost_values, 'ro')
ax.set_xlabel("Distance coefficient")
ax.set_ylabel("Value of cost function")
plt.show()
