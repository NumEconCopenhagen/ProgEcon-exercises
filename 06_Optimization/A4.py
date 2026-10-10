from scipy import optimize


def negative_utility(x1, u_func, alpha, beta, I, p1, p2):
    """Negative CES utility when the whole budget is spent."""
    x2 = (I - p1*x1)/p2
    return -u_func(x1, x2, alpha, beta)


def solve_with_minimize_scalar(u_func, alpha, beta, I, p1, p2):
    """Bounded scalar solver along the budget line (Lecture 6, Section 4)."""

    result = optimize.minimize_scalar(
        negative_utility,
        args=(u_func, alpha, beta, I, p1, p2),
        bounds=(0.0, I/p1),
        method='bounded'
    )
    if not result.success:
        raise RuntimeError(result.message)

    x1 = result.x
    x2 = (I - p1*x1)/p2
    print(f'Bundle: ({x1:.5f}, {x2:.5f})')
    print(f'Utility: {-result.fun:.5f}')
    print(f'Budget left: {I - p1*x1 - p2*x2:.5f}')
    print(f'Function evaluations: {result.nfev}')

    return result
