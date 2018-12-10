#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:33:30 2018

@author: ellereyireland1
"""

import pickle as p
import numpy as np
import system as sys
import run_gravity as g
import numpy as np
import scipy as sp
import coarse_graining as cg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm
from scipy.optimize import curve_fit
import save

def quadratic(x, a, b, c):
    return a*x**2 + b*x + c

p0 = [1, 1, 1]

norm_cell_areas = p.load( open( "all_norm_cell_areas.pickle", "rb"))
norm_optimized_d = p.load( open( "all_norm_optimized_d.pickle", "rb"))
zipf_cell_areas = p.load( open( "all_zipf_cell_areas.pickle", "rb"))
zipf_optimized_d = p.load( open( "all_zipf_optimized_d.pickle", "rb"))

mean_cell_areas = norm_cell_areas[0,]
norm_mean_optimized_d = []
norm_std_optimized_d = []
zipf_mean_optimized_d = []
zipf_std_optimized_d = []

for i in range(20):
    coloumn = norm_optimized_d[:,i]
    norm_mean_optimized_d.append(np.mean(coloumn))
    norm_std_optimized_d.append(np.std(coloumn))
    coloumn = zipf_optimized_d[ :,i]
    zipf_mean_optimized_d.append(np.mean(coloumn))
    zipf_std_optimized_d.append(np.std(coloumn))

popt, pcov = curve_fit(quadratic, mean_cell_areas, norm_mean_optimized_d, p0=p0)

sigma_a = pcov[0][0] ** 0.5
sigma_b = pcov[1][1] ** 0.5
sigma_c= pcov[2][2] ** 0.5

x_value = np.linspace(0, max(mean_cell_areas), 1000)
plt.rc('text', usetex=True)
matplotlib.rcParams.update({'font.size':18})
fig = plt.figure(1, figsize=(15.0, 9.0))
ax = fig.add_subplot(111)
ax.errorbar(mean_cell_areas, norm_mean_optimized_d, yerr=norm_std_optimized_d, fmt= 'k+')

legend_size = 18
axes_label_size = 26

plt.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)
label=r'$\overline{d}(S) =(%.2E \pm %.2E)S^2 + (%.2E \pm %.2E)S + (%.2E \pm%.2E)$' % ( popt[0], sigma_a, popt[1], sigma_b, popt[2], sigma_c)
ax.text(0.0, 2.35, label)
ax.set_xlabel(r'Grained cell area $S$ (length$^2$)', fontsize = axes_label_size)
plt.legend(fontsize=legend_size)
ax.set_ylabel(r'Optimum parameter $\overline{d}$ (length)', fontsize = axes_label_size)
ax.set_title(r'Optimum $\overline{d}$ against the grained cell area for normally distributed sizes', fontsize = axes_label_size)
ax.grid(True)

popt, pcov = curve_fit(quadratic, mean_cell_areas, zipf_mean_optimized_d, p0=p0)

sigma_a = pcov[0][0] ** 0.5
sigma_b = pcov[1][1] ** 0.5
sigma_c= pcov[2][2] ** 0.5

fig = plt.figure(2, figsize=(15.0, 9.0))
ax = fig.add_subplot(111)
ax.errorbar(mean_cell_areas, zipf_mean_optimized_d, yerr=zipf_std_optimized_d, fmt= 'k+', capsize=3)

plt.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)

label=r'$\overline{d}(S) =(%.2E \pm %.2E)S^2 + (%.2E \pm %.2E)S + (%.2E \pm%.2E)$' % ( popt[0], sigma_a, popt[1], sigma_b, popt[2], sigma_c)
ax.text(0.0, 2.35, label)

ax.set_xlabel(r'Grained cell area $S$ (length$^2$)', fontsize = axes_label_size)
plt.legend(fontsize = legend_size)
ax.set_ylabel(r'Optimum $\overline{d}$ (length)', fontsize = axes_label_size)
ax.set_title(r'Optimum $\overline{d}$ against the grained cell area for zipf distributed sizes', fontsize = axes_label_size)
ax.grid(True)
plt.show()
