import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # needed for projection='3d' in older matplotlib
from matplotlib import cm

import A1, A4


def plot(x1_vec, x2_vec, alpha, beta, uvals, filename=None):
    """Utility surface with indifference curves (black) drawn at height u."""

    # a. utility on the grid
    x1_grid, x2_grid = np.meshgrid(x1_vec, x2_vec, indexing='ij')
    u_grid = A1.u_func(x1_grid, x2_grid, alpha=alpha, beta=beta)

    # b. plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    # i. surface with colorbar
    h = ax.plot_surface(x1_grid, x2_grid, u_grid, cmap=cm.jet)
    fig.colorbar(h, shrink=0.6, pad=0.12)

    # ii. indifference curves: points (x1, x2(x1,u), u), drawn on top of the surface
    for uval in uvals:
        I = x1_vec > uval*alpha**(1/beta)                 # valid x1
        x1_line = x1_vec[I]
        x2_line = A4.x2_func(x1_line, uval, alpha=alpha, beta=beta)
        J = x2_line < x2_vec[-1]                          # stay inside the grid
        z_line = uval*np.ones_like(x2_line[J])            # constant height u
        ax.plot(x1_line[J], x2_line[J], z_line, lw=2, color='black', zorder=99)

    # c. labels; invert the x axis to bring the origin to the front
    ax.set_title(fr'Utility, $\beta = {beta}$')
    ax.set_xlabel('$x_1$', labelpad=10)
    ax.set_ylabel('$x_2$', labelpad=10)
    ax.set_zlabel('$u$')
    ax.invert_xaxis()
    fig.tight_layout(pad=0.1)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')
