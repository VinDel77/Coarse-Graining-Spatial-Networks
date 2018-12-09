import matplotlib.pyplot as plt
from matplotlib import rc

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

def plot_nodes_weighted(nodes, masses, fig=None, colour='k'):
    if fig is None:
        fig = plt.figure(1)

    ax = fig.add_subplot(111)
    min_masses = min(masses)
    max_masses = max(masses)
    print(max_masses)
    print(min_masses)

    marker_size = (masses - min_masses) / (max_masses -  min_masses)
    marker_size *= 50
    marker_size += 1
    ax.scatter(nodes[:, 0], nodes[:, 1], color=colour, s=marker_size)

#    ax.grid(True)
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

    ax.set_xlabel(r'Value of $\gamma$')
    ax.set_ylabel(r'Cost')
    plt.show()
