import numpy as np


def grid_search_line(u_func, alpha, beta, I, p1, p2, N):
    """Grid search along the budget line (Lecture 6, Section 3) for CES utility."""

    # a. candidates on the budget line: spend the rest of the budget on good 2
    x1_values = np.linspace(0.0, I/p1, N)
    x2_values = (I - p1*x1_values)/p2

    # b. the CES function uses `if`, so evaluate one bundle at a time
    u_values = np.empty(N)
    for i in range(N):
        u_values[i] = u_func(x1_values[i], x2_values[i], alpha, beta)

    # c. best grid point
    best_index = np.argmax(u_values)
    best_x1 = x1_values[best_index]
    best_x2 = x2_values[best_index]
    best_u = u_values[best_index]

    # d. report
    print(f'Utility evaluations: {N}')
    print(f'Best budget-line bundle: ({best_x1:.5f}, {best_x2:.5f})')
    print(f'Utility: {best_u:.5f}')
    print(f'Budget left: {I - p1*best_x1 - p2*best_x2:.5f}')

    return best_x1, best_x2, best_u
