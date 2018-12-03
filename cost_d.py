#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:05:18 2018

@author: ellereyireland1
"""

import system as sys
import run_gravity as g
import numpy as np
import coarse_graining as cg
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

s = g.Gravity()
system = sys.System()
system.random_system(100, normal=False)

distances = []
cost_values =[]

s.set_system(system)
s.tuning_function()
s.set_flows()
s.cost_function()


mean_dist = np.mean(s.system.distance_matrix)
bound = np.sqrt(mean_dist)

distances = list(np.linspace(0.01, mean_dist + 0.5*bound, 1000))

distances.append(mean_dist)
bound = np.sqrt(mean_dist)

for d in tqdm(distances):
    s.set_system(system, distance =d)
    s.set_flows()
    s.cost_function()
    cost_values.append(s.cost)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(distances, cost_values, 'ro')
ax.set_xlabel("Distance coefficient")
ax.set_ylabel("Value of cost function")
plt.show()
