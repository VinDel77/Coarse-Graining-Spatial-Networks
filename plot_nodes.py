import matplotlib.pyplot as plt

def plot_nodes(nodes, fig=None, fmt='bo'):
    if fig is None:
        fig = plt.figure(1)

    ax = fig.add_subplot(111)

    ax.plot(nodes[:, 0], nodes[:, 1], fmt)
    return fig

def plot_gridlines(boundaries, fig):
    ax = fig.add_subplot(111)
    for b in boundaries:
        ax.axvline(b, color='gray', alpha=0.5)
        ax.axhline(b, color='gray', alpha=0.5)
    return fig

def plot_nodes_weighted(nodes, masses, fig=None, colour='b'):
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

    return fig
