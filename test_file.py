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
from tqdm import tqdm

level_graining = [0]
flows = []

s = g.Gravity()

system = sys.System()
system.random_system(10)
s.set_system(system)
s.tuning_function()
s.set_flows()

flows.append(s.total_flow)
print(s.flow_matrix)
print(flows)
#
#for i in tqdm(np.arange(2,100,10)):
#    grained_system = cg.Coarse_graining(s.system, i)
#    new_system = grained_system.generate_new_system()
#    s.set_system(new_system)
#    s.tuning_function()
#    s.set_flows()
#    flows.append(s.total_flow)
#    level_graining.append(i)
#
#plt.plot(level_graining, flows)
#plt.show()
