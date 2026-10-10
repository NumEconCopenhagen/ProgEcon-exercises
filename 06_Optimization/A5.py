import numpy as np
from scipy import optimize


def negative_utility_bundle(x, u_func, alpha, beta):
    """Negative CES utility; x[0] and x[1] are the two quantities."""
    return -u_func(x[0], x[1], alpha, beta)


def budget_left(x, I, p1, p2):
    """Nonnegative when the bundle is affordable."""
    return I - p1*x[0] - p2*x[1]


def solve_with_slsqp(u_func, alpha, beta, I, p1, p2):
    """Choose both quantities with SLSQP (Lecture 6, Section 5), from three starts."""

    # a. restrictions
    quantity_bounds = [(0.0, I/p1), (0.0, I/p2)]
    budget_constraint = {'type': 'ineq', 'fun': budget_left, 'args': (I, p1, p2)}

    # b. three affordable starting bundles
    starts = [np.array([1.0, 1.0]), np.array([0.4*I/p1, 0.4*I/p2]), np.array([0.9*I/p1, 0.04*I/p2])]

    for x0 in starts:
        result = optimize.minimize(
            negative_utility_bundle,
            x0=x0,
            args=(u_func, alpha, beta),
            method='SLSQP',
            bounds=quantity_bounds,
            constraints=budget_constraint
        )
        print(f'start {x0} -> bundle ({result.x[0]:.5f}, {result.x[1]:.5f}); '
              f'budget left: {budget_left(result.x, I, p1, p2):.5f}; '
              f'evaluations: {result.nfev}; success: {result.success}')

    return result
