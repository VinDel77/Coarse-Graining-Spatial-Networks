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

def run_plot():
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

    return distances, cost_values, grained_system, original_flows


#if __name__=="__main__":
#    distances, cost_values, grained_system, original_flows = run_plot()
##save.save_object(cost_values, "Cost value array")
#    fig = plt.figure(1, figsize=(15.0, 9.0))
#    plt.rc('text', usetex=True)
#    ax = fig.add_subplot(111)
#    ax.plot(distances, cost_values, 'r-')
#    ax.set_xlabel("Distance coefficient (length)", fontsize = 15)
#    ax.set_ylabel("Value of cost function (unitless)", fontsize = 15)
#    ax.set_title(r'Cost function value against the parameter d', fontsize = 15)
##plt.savefig('/Users/ellereyireland1/Documents/University/Third_year/BSc_project/Report/Images/cost_function_d')
#    plt.show()
