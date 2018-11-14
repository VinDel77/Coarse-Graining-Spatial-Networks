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
