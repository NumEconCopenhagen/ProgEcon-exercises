import numpy as np
import matplotlib.pyplot as plt


def summary(income):
    """Print mean and median (thousands separator with :,)."""
    print(f'mean income:   {np.mean(income):>10,.0f} DKK')
    print(f'median income: {np.median(income):>10,.0f} DKK')


def plot(income, filename=None):
    """Histogram of income (in 1,000 DKK) with vertical lines at the mean and the median."""

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    income_k = income/1000  # thousand DKK keeps the axis readable

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.hist(income_k, bins=40, color='lightgrey', edgecolor='black')
    ax.axvline(np.mean(income_k), color=colors[3], lw=2, label='mean')
    ax.axvline(np.median(income_k), color=colors[0], lw=2, ls='--', label='median')

    ax.set_title('Distribution of annual income', pad=10)
    ax.set_xlabel('income (1,000 DKK per year)')
    ax.set_ylabel('number of households')
    ax.legend()

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')
