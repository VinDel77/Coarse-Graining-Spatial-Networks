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
import scipy as sp
from scipy.optimize import curve_fit
from tqdm import tqdm
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rc
import pickle
import matplotlib

def do_runs():
    test_values = list(range(2, 10))
    repetitions = 10
    system = sys.System()
    s = g.Gravity()
    system.random_system(1000, normal=False)
    results_dict = {0:[]}
    for i in test_values:
        coarse_grainer = cg.Coarse_graining(system, i)
        results_dict[coarse_grainer.get_cell_area()] = []

    for i in tqdm(range(repetitions)):
        system.random_system(1000, normal=False)
        s.set_system(system)
        s.tuning_function()
        s.set_flows()

        initial_flow = np.sum(system.flow_matrix)
        results_dict[0].append(initial_flow - initial_flow)

        for i in range(2, 10):
            coarse_grainer = cg.Coarse_graining(system, i)
            cell_area = coarse_grainer.get_cell_area()

            grained_system = coarse_grainer.generate_new_system()
            flow_loss = np.sum(grained_system.flow_matrix) - initial_flow
            results_dict[cell_area].append(flow_loss)

    save.save_object(results_dict, 'results_dict')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(list(results_dict.values()), positions=list(results_dict.keys()))
    plt.show()

def plot_results(file_name):
    results_dict = pickle.load(open(file_name, 'rb'))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    keys = list(results_dict.keys())
    positions = np.round(keys, 3)
    for key, value in results_dict.items():
        key_array = np.full_like(value, key)
        ax.plot(key_array, value, marker='o', color='grey', alpha=0.5, ls='')
    ax.boxplot(list(results_dict.values()), positions=positions,
               widths=0.01, sym='x')
    ax.set_xlim(min(keys) - 0.007, max(keys) + 0.007)
    ax.set_xticks(np.linspace(min(keys) - 0.01, max(keys) + 0.01, 20))
    ax.set_xticklabels(np.round(np.linspace(min(keys) - 0.01, max(keys) + 0.01, 20), 2))
    ax.set_xlabel('Cell area')
    ax.set_ylabel('Flow loss')
    plt.show()

def plot_results_std(file_name):
    font = {'family' : 'serif',
            'size'   : 18}

    matplotlib.rc('text', usetex=True)
    matplotlib.rc('font', **font)
    results_dict = pickle.load(open(file_name, 'rb'))
    x_vals = np.array(list(results_dict.keys()))

    y_data = np.array(list(results_dict.values()))
    y_vals = np.mean(y_data, axis=1)
    y_err = 2*np.std(y_data, axis=1)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    p = [1, 1]

    ax.errorbar(x_vals[1:], y_vals[1:], yerr=y_err[1:], marker='o', ls='', ecolor='k', color='k', capsize=3)

    popt, pcov = curve_fit(linear_func, x_vals, y_vals, p0=p)
    grad, coef = popt
    e_grad = pcov[0][0] ** 0.5
    e_coef = pcov[1][1] ** 0.5

    residuals = y_vals - linear_func(x_vals, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_vals - np.mean(y_vals))**2)
    r_val = 1.0 - (ss_res/ ss_tot)
    x_range = np.linspace(min(x_vals), max(x_vals), 100)
    y_range = grad * x_range + coef

    ax.plot(x_range, y_range, color='gray', ls='-')
    ax.set_xlabel(r'Cell Area ($S$) (length$^2$)', fontsize=18)
    ax.set_ylabel(r'Flow loss ($L$) (units of flow)', fontsize=18)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    plt.grid(which='both', axis='both')
    rounded_grad = round(grad, 2)
    rounded_coef = -1 * round(coef, 2)
    e_grad = round(e_grad, 1)
    e_coef = round(e_coef, 2)
    label = r'$L(S) = {} \pm {} * S - {} \pm {}$'.format(rounded_grad, e_grad,
                                                         rounded_coef, e_coef)
    ax.text(0.12, -0.5, label)
    ax.text(0.12, -0.7, r'$R^2 = {}$'.format(round(r_val ** 2, 5)))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    y_diff = abs(y_vals - linear_func(x_vals, grad, coef))
    ax.plot(x_vals, y_diff, 'xk')
    ax.set_xlabel(r'Cell Area ($S$)', fontsize=18)
    ax.set_ylabel(r'Error in fit', fontsize=18)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    plt.grid(which='major', axis='both')

    print("Linear function grad: {}".format(grad))
    print("Linear function coef: {}".format(coef))
    plt.show()

def linear_func(x, a , b):
    return x * a + b

plot_results_std('ten_flows_dict.pickle')
