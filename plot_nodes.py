import matplotlib.pyplot as plt

def plot_nodes(nodes, fig=None, fmt='bo'):
    if fig is None:
        fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(nodes[:, 0], nodes[:, 1], fmt)
    return fig
