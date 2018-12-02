#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:41:15 2018

@author: ellereyireland1
"""

import system as sys
import run_gravity as g
import numpy as np
import coarse_graining as cg
import numpy as np
import matplotlib.pyplot as plt
import save
from tqdm import tqdm

level_graining = [0]
flows = []

s = g.Gravity()
area_size = []
total_flows =[]

system = sys.System()
system.random_system(100)
s.set_system(system)
s.tuning_function()
s.set_flows()

area_size.append(0)
total_flows.append(np.sum(system.flow_matrix))

for i in range(2, 10):
    coarse_grainer = cg.Coarse_graining(system, i)
    cell_area = coarse_grainer.get_cell_area()

    grained_system = coarse_grainer.generate_new_system()
    area_size.append(cell_area)
    total_flows.append(np.sum(grained_system.flow_matrix))

save.save_object([area_size, total_flows], '[area_size], [total_flow]')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(area_size, total_flows, 'bo')
ax.set_xlabel("Minimum cell size")
ax.set_ylabel("Total flow")
plt.show()
