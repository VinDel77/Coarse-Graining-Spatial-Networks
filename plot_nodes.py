import matplotlib.pyplot as plt
from matplotlib import rc
import system as s
import run_gravity as g

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

def plot_nodes_weighted(nodes, masses, fig=None, colour='k', size_multiplier=50):
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
    ax.scatter(nodes[:, 0], nodes[:, 1], color=colour, s=marker_size)

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


if __name__=="__main__":
    plot_tuning()
