import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy import optimize

plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size': 12})

from A2 import x2_from_x1

def solve_numerically(u_func, I, p1, p2, alpha, beta):
    """Numerically solve the consumer problem along the budget line.

    Minimizes -u over x1 in (0, I/p1) with minimize_scalar (as in section 3.4).
    Returns (x1_star, x2_star, u_star).
    """

    obj = lambda x1: -u_func(x1, (I - p1*x1)/p2, alpha, beta)
    res = optimize.minimize_scalar(obj, bounds=(0, I/p1), method='bounded')
    x1 = res.x
    x2 = (I - p1*x1)/p2
    u  = -res.fun
    return x1, x2, u

def price_shock_sensitivity(u_func, alpha, I, p1, p2, betas=None):
    """Double p1 and report how the optimum changes across CES curvatures beta."""

    if betas is None:
        betas = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    betas = np.asarray(betas, dtype=float)

    # a. baseline vs. shock (p1 doubles), solved numerically for each beta
    base = np.array([solve_numerically(u_func, I, p1,     p2, alpha, b) for b in betas]).T
    shck = np.array([solve_numerically(u_func, I, 2.0*p1, p2, alpha, b) for b in betas]).T
    x1_b, x2_b, u_b = base[0], base[1], base[2]
    x1_s, x2_s, u_s = shck[0], shck[1], shck[2]

    # b. percentage changes relative to baseline
    pct  = lambda new, old: 100.0*(new - old)/old
    d_x1 = pct(x1_s, x1_b)
    d_x2 = pct(x2_s, x2_b)
    d_u  = pct(u_s,  u_b)

    # c. table of results
    print(f"{'beta':>6}{'%dx1':>10}{'%dx2':>10}{'%du':>10}")
    print('-'*36)
    for k in range(len(betas)):
        print(f'{betas[k]:>6.2f}{d_x1[k]:>10.2f}{d_x2[k]:>10.2f}{d_u[k]:>10.2f}')

    # d. plots
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))

    # Panel A: quantities
    axs[0].plot(betas, d_x1, marker='o', label=r'$x_1^\star$ (good whose price rose)')
    axs[0].plot(betas, d_x2, marker='s', label=r'$x_2^\star$ (the other good)')
    axs[0].axhline(0, color='black', linewidth=0.8)
    axs[0].set_title('Panel A: quantities after $p_1$ doubles')
    axs[0].set_xlabel(r'$\beta$  (higher $\beta$ = more curvature)')
    axs[0].set_ylabel('% change from baseline')
    axs[0].yaxis.set_major_formatter(PercentFormatter())
    axs[0].set_xticks(betas)
    axs[0].legend(frameon=True)

    # Panel B: utility (welfare loss)
    axs[1].plot(betas, d_u, marker='o', color='C3', label=r'$u^\star$')
    axs[1].axhline(0, color='black', linewidth=0.8)
    axs[1].set_title('Panel B: utility (welfare) after $p_1$ doubles')
    axs[1].set_xlabel(r'$\beta$  (higher $\beta$ = more curvature)')
    axs[1].set_ylabel('% change from baseline')
    axs[1].yaxis.set_major_formatter(PercentFormatter())
    axs[1].set_xticks(betas)
    axs[1].legend(frameon=True)

    fig.suptitle(r'Sensitivity to a doubling of $p_1$ across CES curvatures $\beta$')
    fig.tight_layout()
    plt.show()
