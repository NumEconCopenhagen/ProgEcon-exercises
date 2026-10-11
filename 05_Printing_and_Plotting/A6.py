import numpy as np
import matplotlib.pyplot as plt

import A1, A4


def plot(p1, p2, income, alpha, beta, uvals, N=100, filename=None):
    """Affordable bundles colored by utility, budget line and indifference curves."""

    # a. grid of bundles (start slightly above 0 because u_func needs x > 0)
    x1_vec = np.linspace(0.05, income/p1, N)
    x2_vec = np.linspace(0.05, income/p2, N)
    x1_grid, x2_grid = np.meshgrid(x1_vec, x2_vec, indexing='ij')

    # b. 2-D Boolean mask; indexing with it gives 1-D arrays
    affordable = p1*x1_grid + p2*x2_grid <= income
    x1_aff = x1_grid[affordable]
    x2_aff = x2_grid[affordable]
    u_aff = A1.u_func(x1_aff, x2_aff, alpha=alpha, beta=beta)
    print(f'{x1_aff.size} of {N*N} grid bundles are affordable')

    # c. figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # i. scatter colored by utility
    h = ax.scatter(x1_aff, x2_aff, s=10, c=u_aff)
    fig.colorbar(h, label='utility')

    # ii. budget line
    ax.plot([0, income/p1], [income/p2, 0], color='black', lw=2, label='budget line')

    # iii. indifference curves (x2_func from Task 4, valid x1 only)
    x1_line = np.linspace(0.05, income/p1, 500)
    for uval, ls in zip(uvals, ['-', '--']):
        I = x1_line > uval*alpha**(1/beta)
        x2_line = A4.x2_func(x1_line[I], uval, alpha=alpha, beta=beta)
        ax.plot(x1_line[I], x2_line, color='red', ls=ls, lw=2, label=fr'$u = {uval}$')

    ax.set_title('Affordable bundles colored by utility', pad=10)
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_xlim(0, income/p1)
    ax.set_ylim(0, income/p2)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)  # below the axes

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')
