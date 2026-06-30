import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size': 12})

def draw_pareto(b=2.0, size=10_000, seed=2026):
    """Draw `size` numbers from a classic Pareto distribution.

    Shape (tail) parameter `b` and minimum value x_m = 1. NumPy's
    rng.pareto draws from the distribution shifted to start at 0, so we
    add 1.0 to obtain the classic Pareto with support x >= 1.
    """
    
    rng = np.random.default_rng(seed)
    x = rng.pareto(b, size=size) + 1.0
    
    return x


def plot_pareto(b=2.0, size=10_000, seed=2026):
    """Draw Pareto numbers and plot (1) a histogram and (2) the tail.

    The tail plots the empirical fraction of draws above x, P(X > x), on
    log-log axes; for a Pareto distribution this is (close to) a straight line.
    """
    x = draw_pareto(b, size, seed)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # a. histogram of the draws
    axes[0].hist(np.log(x), bins=100, density=True)
    axes[0].set_title(f'Pareto histogram (b={b})')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('density')

    # b. tail: empirical fraction of draws above x, P(X > x), on log-log axes
    xs = np.sort(x)
    frac_above = 1.0 - np.arange(1, xs.size + 1) / xs.size
    axes[1].loglog(xs, frac_above, label='stochastic draws')
    axes[1].loglog(xs, (xs ** -b), 'r--', label=f'theoretical: x^-{b}')
    axes[1].legend()
    axes[1].set_title('Tail: P(X > x), log-log')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('P(X > x)')

    fig.tight_layout()
    plt.show()

    print(f'mean = {x.mean():.3f}, max = {x.max():.1f}, share > 10 = {(x > 10).mean():.4f}')
