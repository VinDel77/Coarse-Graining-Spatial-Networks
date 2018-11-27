import coarse_graining as cg
import system as s
import numpy as np
import matplotlib.pyplot as plt
import run_gravity as g

def test_inflow():
    np.random.seed(1)
    system = s.System()
    nodes = np.array([(1, 1), (4, 2), (6, 6), (9, 7), (2, 6), (3, 8), (8, 3), (7, 1)])

    system.set_nodes(nodes)
    system.set_inflow(system.add_inflow(1))
    system.set_outflow(system.add_outflow(1))
    system.set_distance_matrix()

    flow_matrix = np.random.random(system.distance_matrix.shape)*10
    print(flow_matrix)
    print("\n")
    print(system.distance_matrix)

    coarse_grainer = cg.Coarse_graining(system, 2)
    new_system = coarse_grainer.generate_new_system()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(system.nodes[:, 0], system.nodes[:, 1] ,'ro')
    ax.plot(new_system.nodes[:, 0], new_system.nodes[:, 1], 'bo')
    plt.show()
    return system
