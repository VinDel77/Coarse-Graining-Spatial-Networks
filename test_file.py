#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:41:15 2018

@author: ellereyireland1
"""

import point_generator as pg
import run_gravity as g
import numpy as np 
import coarse_graining as cg
import numpy as np
import matplotlib.pyplot as plt

flows = []
s = g.Gravity(1000)     
level_graining = [0]                                                                                                                        

flows.append(s.total_flow)

for i in np.arange(2,1000,50):
    grained_system = cg.Coarse_graining(s.system, i)
    flows.append(grained_system.system.total_flow)
    level_graining.append(i)

plt.plot(level_graining, flows)
plt.show()
