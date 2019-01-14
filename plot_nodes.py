import matplotlib.pyplot as plt
from matplotlib import rc
import system as s
import run_gravity as g
import coarse_graining as cg

def plot_nodes(nodes, fig=None, colour='b', size=15.0):
    if fig is None:
        fig = plt.figure(1)

    ax = fig.add_subplot(111)

    ax.scatter(nodes[:, 0], nodes[:, 1], marker='o', color=colour, s=size)
    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))
#    ax.grid(True)
    return fig

def plot_gridlines(boundaries, fig):
    ax = fig.add_subplot(111)
    for b in boundaries:
        ax.axvline(b, color='gray', alpha=0.5)
        ax.axhline(b, color='gray', alpha=0.5)
    return fig

def plot_nodes_weighted(nodes, masses, fig=None, colour='k', size_multiplier=50, grid=True, cg=False):
    if fig is None:
        fig = plt.figure(1)

    ax = fig.add_subplot(111)
    min_masses = min(masses)
    max_masses = max(masses)
    print(max_masses)
    print(min_masses)

    marker_size = (masses - min_masses) / (max_masses -  min_masses)
    marker_size *= size_multiplier
    marker_size += 1
    if cg:
        ax.scatter(nodes[:, 0], nodes[:, 1], facecolor=colour, s=500, edgecolor='k', lw=1, alpha=0.75)
    else:
        ax.scatter(nodes[:, 0], nodes[:, 1], color=colour, s=marker_size)
    if grid:
        ax.grid(True)
    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))

    return fig

def plot_cost_distance(costs, distances):
    rc('text', usetex=True)
    rc('font', **{'family':'sans-serif', 'size':18})
    plt.rc('font', family='sans-serif')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(distances, costs, 'k-')

    ax.set_xlabel(r'Value of $\overline{d}$', fontsize = 24)
    ax.set_ylabel(r'Cost', fontsize=24)
    ax.grid(True)
    plt.show()

def plot_norm_zipf():
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=18)
    norm_system = s.System()
    zipf_system = s.System()

    norm_system.random_system(500)
    zipf_system.random_system(500, normal=False)

    fig = plt.figure(1)
    plot_nodes_weighted(norm_system.nodes, norm_system.inflow +
                        norm_system.outflow, fig=fig, colour='k')

    fig = plt.figure(2)
    plot_nodes_weighted(zipf_system.nodes, zipf_system.inflow +
                        zipf_system.outflow, fig=fig, colour='k', size_multiplier=75)

    plt.show()

def plot_tuning():
    system = s.System()
    system.random_system(1000, normal=False)

    gravity = g.Gravity()
    gravity.set_system(system)

    gravity.tuning_function(plot=True)

def plot_coarse_graining():
    system = s.System()
    system.random_system(100)

    gravity = g.Gravity()
    gravity.set_system(system)
    gravity.set_flows()

    coarse_grainer = cg.Coarse_graining(system, 3)
    boundaries = coarse_grainer.boundaries
    new_system = coarse_grainer.generate_new_system()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=22)
    fig = plt.figure(1, figsize=(10, 10))
    plot_nodes_weighted(system.nodes, system.inflow + system.outflow, fig=fig,
                        colour='k', grid=False)

    plot_nodes_weighted(new_system.nodes, system.inflow+system.outflow,
                        fig=fig, colour='gray', grid=False, size_multiplier=200, cg=True)

    plot_gridlines(boundaries, fig=fig)
    plt.show()

if __name__=="__main__":
    plot_coarse_graining()
