import numpy as np


def grid_search_2d(u_func, alpha, beta, I, p1, p2, N1, N2):
    """2D grid search over the budget set (Lecture 6, Section 2) for CES utility."""

    # a. grids for the two goods
    x1_grid = np.linspace(0.0, I/p1, N1)
    x2_grid = np.linspace(0.0, I/p2, N2)

    # b. initial best bundle and a counter
    best_x1 = 0.0
    best_x2 = 0.0
    best_u = u_func(best_x1, best_x2, alpha, beta)
    n_tried = 0

    # c. try every pair; only affordable pairs can become the best
    for x1 in x1_grid:
        for x2 in x2_grid:
            n_tried += 1
            if p1*x1 + p2*x2 <= I:
                candidate_u = u_func(x1, x2, alpha, beta)
                if candidate_u > best_u:
                    best_x1 = x1
                    best_x2 = x2
                    best_u = candidate_u

    # d. report
    print(f'Pairs tried: {n_tried}')
    print(f'Best grid bundle: ({best_x1:.5f}, {best_x2:.5f})')
    print(f'Utility: {best_u:.5f}')
    print(f'Budget left: {I - p1*best_x1 - p2*best_x2:.5f}')

    return best_x1, best_x2, best_u
