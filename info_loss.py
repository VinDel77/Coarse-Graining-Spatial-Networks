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
from scipy.stats import linregress
import pickle

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
    results_dict = pickle.load(open(file_name, 'rb'))
    x_vals = np.array(list(results_dict.keys()))

    y_data = np.array(list(results_dict.values()))
    y_vals = np.mean(y_data, axis=1)
    y_err = 2*np.std(y_data, axis=1)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(x_vals, y_vals, yerr=y_err, marker='o', ls='', ecolor='k', capsize=3)

    grad, coef, r_val, p_val, stderr = linregress(x_vals, y_vals)
    x_range = np.linspace(min(x_vals), max(x_vals), 100)
    y_range = grad * x_range + coef

    ax.plot(x_range, y_range, 'r-')
    ax.set_xlabel('Cell Area')
    ax.set_ylabel('Flow loss')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    y_diff = abs(y_vals - linear_func(x_vals, grad, coef))
    ax.plot(x_vals, y_diff, 'xk')
    ax.set_xlabel('Cell Area')
    ax.set_ylabel('Error in fit')

    plt.show()

def linear_func(x, grad, coef):
    return x * grad - coef
plot_results_std('ten_flows_dict.pickle')
