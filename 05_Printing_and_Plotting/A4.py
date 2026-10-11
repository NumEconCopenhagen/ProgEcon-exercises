import numpy as np
import matplotlib.pyplot as plt


def x2_func(x1, u, alpha=0.5, beta=1.0):
    """Indifference curve of the CES function: the x2 that gives utility u at x1.
    Valid only for x1 > u*alpha**(1/beta); elsewhere the base is negative."""
    return ((u**(-beta) - alpha*x1**(-beta))/(1-alpha))**(-1/beta)


def plot(alpha, betas, uvals, x1_vec, line45=False, filename=None):
    """Indifference curves: one color per utility level, one line style per beta."""

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    linestyles = ['-', '--', ':']

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for i, beta in enumerate(betas):
        for j, uval in enumerate(uvals):

            # Boolean mask: keep only the x1 where the curve is defined
            I = x1_vec > uval*alpha**(1/beta)
            x2_vec = x2_func(x1_vec[I], uval, alpha=alpha, beta=beta)

            # colors are labelled once (first beta), line styles are labelled below
            label = fr'$u = {uval}$' if i == 0 else None
            ax.plot(x1_vec[I], x2_vec, ls=linestyles[i], color=colors[j], label=label)

    # one black legend entry per line style (only needed when betas are compared)
    if len(betas) > 1:
        for i, beta in enumerate(betas):
            ax.plot([], [], ls=linestyles[i], color='black', label=fr'$\beta = {beta}$')

    # 45-degree line
    if line45:
        ax.plot([0, 4], [0, 4], color='grey', lw=1, zorder=0, label='45-degree line')

    ax.set_title(fr'Indifference curves, $\alpha = {alpha}$', pad=10)
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), prop={'size': 10})  # outside, so no curve is hidden

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')
