import matplotlib.pyplot as plt

def plot_nodes(nodes):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(nodes[:, 0], nodes[:, 1], 'bo')
    plt.show()
