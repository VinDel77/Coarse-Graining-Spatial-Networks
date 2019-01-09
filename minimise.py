import numpy as np
import run_gravity as g
import optimize_parameter as op
import matplotlib.pyplot as plt
import system as sys
import coarse_graining as cg
from scipy.optimize import minimize

import cProfile

def find_minimum_mc(grained_system, s, original_flows):
    cost_values = []
    mean_dist = np.mean(grained_system.distance_matrix)
    bound = np.sqrt(mean_dist)
    distances = list(np.linspace(0.01, mean_dist + 3*bound, 100))
    for d in distances:
        s.set_system(grained_system, distance =d)
        s.tuning_function()
        s.set_flows()
        grained_flows = grained_system.flow_matrix
        s.cost_function(original_flows, grained_flows)
        cost_values.append(s.cost)
    return distances[np.argmin(cost_values)]

def func(d, s, grained_system, original_flows):
    s.set_system(grained_system, distance = d)
    s.tuning_function()
    s.set_flows()
    grained_flows = grained_system.flow_matrix
    s.cost_function(original_flows, grained_flows)
    return s.cost

def find_minimum_sp(grained_system, s, original_flows):
    intial_guess = np.mean(grained_system.distance_matrix)
    opt = minimize(func, intial_guess, (s, grained_system, original_flows), bounds=[(0.000000001, np.inf)])
    return opt.x[0]

def run():
    distances, cost_values, grained_system, original_flows = op.run_plot()
    s = g.Gravity()
    min_dist = find_minimum_mc(grained_system, s, original_flows )
    min_dist_sp = find_minimum_sp(grained_system, s, original_flows)

    fig = plt.figure(1, figsize=(10, 8))
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=18)
    ax = fig.add_subplot(111)
    ax.plot(distances, cost_values, 'k-')
    ax.axvline(min_dist_sp, color='k', ls='--')
    ax.set_xlabel(r"Distance coefficient ($d_0$)", fontsize = 18)
    ax.set_ylabel(r"Error in flow matrix ($E$)", fontsize = 18)
    ax.grid(True)
    plt.show()

def time_start():
    system = sys.System()
    system.random_system(1000, normal=False)

    s = g.Gravity()
    s.set_system(system)
    s.tuning_function()
    s.set_flows()

    coarse_grainer = cg.Coarse_graining(system, 5)
    grained_system = coarse_grainer.generate_new_system()
    original_flows = grained_system.flow_matrix

    return s, grained_system, original_flows

def time_mc():
    for i in range(3):
        s, grained_system, original_flows = time_start()
        find_minimum_mc(grained_system, s, original_flows)
    return 0

def time_sp():
    for i in range(3):
        s, grained_system, original_flows = time_start()
        find_minimum_sp(grained_system, s, original_flows)
    return 0

if __name__=="__main__":
    run()
