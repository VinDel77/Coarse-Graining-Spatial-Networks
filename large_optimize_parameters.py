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
from tqdm import tqdm
from scipy.optimize import curve_fit
import save
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def quadratic(x, a, b, c):
    return a*x**2 + b * x + c

p0 = [1, 1, 1]

norm_cell_areas = p.load( open( "pickle/all_norm_cell_areas.pickle", "rb"))
norm_optimized_d = p.load( open( "pickle/all_norm_optimized_d.pickle", "rb"))
zipf_optimized_d = p.load( open( "pickle/all_zipf_optimized_d.pickle", "rb"))

norm_cell_areas = np.array(norm_cell_areas)
norm_optimized_d= np.array(norm_optimized_d)
zipf_optimized_d = np.array(zipf_optimized_d)

mean_cell_areas = norm_cell_areas[0,]
norm_mean_optimized_d = []
norm_std_optimized_d = []
zipf_mean_optimized_d = []
zipf_std_optimized_d = []

no_points = len(mean_cell_areas)

for i in range(no_points):
    coloumn = norm_optimized_d[:,i]
    norm_mean_optimized_d.append(np.mean(coloumn))
    norm_std_optimized_d.append(np.std(coloumn))
    coloumn = zipf_optimized_d[ :,i]
    zipf_mean_optimized_d.append(np.mean(coloumn))
    zipf_std_optimized_d.append(np.std(coloumn))

popt, pcov = curve_fit(quadratic, mean_cell_areas, norm_mean_optimized_d, p0=p0, sigma=norm_std_optimized_d)

sigma_a = pcov[0][0] ** 0.5
sigma_b = pcov[1][1] ** 0.5
sigma_c= pcov[2][2] ** 0.5

x_value = np.linspace(0, max(mean_cell_areas), 1000)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=18)
fig = plt.figure(1, figsize=(15, 12))
ax = fig.add_subplot(111)
ax.errorbar(mean_cell_areas, norm_mean_optimized_d, yerr=norm_std_optimized_d, fmt= 'k+')

plt.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)
ax.set_xlabel(r'Grained cell area $S$ (length$^2$)', fontsize = 20)
label = r'$d_0(S) =(%.2E \pm %.0E)S^2 + (%.1E \pm %.0E)S + (%.2E \pm %.0E)$' % ( popt[0], sigma_a, popt[1], sigma_b, popt[2], sigma_c)
ax.text(0.0, 2.35, label, fontsize=20 )
ax.set_ylabel(r'Optimum parameter $d_0$ (length)', fontsize = 20)
ax.set_title(r'Normal distribution of optimum $d_0$ against the grained cell area $S$', fontsize = 20)
ax.grid(True)


axins = zoomed_inset_axes(ax, 3, loc = 6)
axins.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,
    right=False,     # ticks along the top edge are off
    labelbottom=False,
    labelleft=False)
axins.errorbar(mean_cell_areas, norm_mean_optimized_d, yerr=norm_std_optimized_d, fmt= 'k+')

axins.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)
axins.set_xlim(0, 0.05) # apply the x-limits
axins.set_ylim(0.45, 0.55)

mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5")

#plt.savefig('/Users/ellereyireland1/Documents/University/Third_year/BSc_project/Report/Images/norm_min_d_parameter')

popt, pcov = curve_fit(quadratic, mean_cell_areas, zipf_mean_optimized_d, p0=p0, sigma=zipf_std_optimized_d)

sigma_a = pcov[0][0] ** 0.5
sigma_b = pcov[1][1] ** 0.5
sigma_c= pcov[2][2] ** 0.5

fig = plt.figure(2, figsize=(15, 12))
ax = fig.add_subplot(111)
ax.errorbar(mean_cell_areas, zipf_mean_optimized_d, yerr=zipf_std_optimized_d, fmt= 'k+')

plt.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)
ax.set_xlabel(r'Grained cell area $S$ (length$^2$)', fontsize = 20)
label = r'$d_0(S) =(%.2E \pm %.0E)S^2 + (%.0E \pm %.0E)S + (%.2E \pm %.0E)$' % ( popt[0], sigma_a, popt[1], sigma_b, popt[2], sigma_c)
ax.text(0.0, 2.35, label, fontsize=20 )
ax.set_ylabel(r'Optimum parameter $d_0$ (length)', fontsize = 20)
ax.set_title(r'Zipf distribution of optimum $d_0$ against the grained cell area $S$', fontsize = 20)
ax.grid(True)

axins = zoomed_inset_axes(ax, 3, loc=6)
axins.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,
    right=False,     # ticks along the top edge are off
    labelbottom=False,
    labelleft=False)
axins.errorbar(mean_cell_areas, zipf_mean_optimized_d, yerr=zipf_std_optimized_d, fmt= 'k+')

axins.plot(x_value, quadratic(x_value, *popt), c='k', linewidth=1.0)
axins.set_xlim(0, 0.05) # apply the x-limits
axins.set_ylim(0.45, 0.6)

mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5")

#plt.savefig('/Users/ellereyireland1/Documents/University/Third_year/BSc_project/Report/Images/zipf_min_d_parameter')
plt.show()
