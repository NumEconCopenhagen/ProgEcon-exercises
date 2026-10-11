def u_func(x1, x2, alpha=0.5, beta=1.0):
    """CES utility. Requires x1, x2 > 0 and beta > 0.
    Works for single numbers and for NumPy arrays."""
    return (alpha*x1**(-beta) + (1-alpha)*x2**(-beta))**(-1/beta)


def report(x1, x2, alpha=0.5, beta=1.0):
    """Print one evaluation of the utility function."""
    u = u_func(x1, x2, alpha=alpha, beta=beta)
    print(f'u({x1:.1f}, {x2:.1f}) = {u:.3f}')
