import numpy as np

def grid_search():
    """Find the x in [0.01,10] (100 points) for which u(x)=sqrt(x) is closest to 2."""

    x = np.linspace(0.01,10,100) # grid of candidate x values
    u = np.sqrt(x) # utility at each grid point

    i = np.argmin(np.abs(u-2)) # index of the x with utility closest to 2
    x_best = x[i]

    print(f'x = {x_best:.4f} gives u(x) = {u[i]:.4f} (closest to 2)')
    return x_best
