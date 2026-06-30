import numpy as np

from grid_solve import print_solution
from A2 import x2_from_x1
from A1 import utility_ces

def bisection(f, a, b, tol=1e-10, max_iter=500):
    """Find a root of f on [a,b] by bisection. Returns (root, iterations)."""

    fa, fb = f(a), f(b)

    if np.isnan(fa) or np.isnan(fb):
        raise ValueError('f(a) or f(b) is NaN.')

    if fa == 0.0: return a, 0
    if fb == 0.0: return b, 0

    if fa*fb > 0:
        raise ValueError('Bisection: root not bracketed. Choose a,b with opposite signs.')

    it = 0
    while (b - a) > tol and it < max_iter:

        m  = 0.5*(a + b)
        fm = f(m)

        if fm == 0.0:
            a = b = m
            break

        if fa*fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
        it += 1

    return 0.5*(a + b), it

def solve_with_bisection(alpha,beta,I,p1,p2,do_print=True):
    """Solve the CES first-order condition f(x1)=0 with bisection."""

    # a. the FOC written as a single equation in x1
    def f(x1):
        x2 = x2_from_x1(x1, I, p1, p2)
        return (alpha/(1.0 - alpha)) * ((x2/x1)**(beta + 1.0)) - (p1/p2)

    # c. bracket around the interior, tolerance and iteration cap
    eps  = 1e-8
    a    = eps
    b    = I/p1 - eps
    tol  = 1e-12
    max_iter = 500

    # d. solve, compute x2 and print
    x1, it = bisection(f, a, b, tol=tol, max_iter=max_iter)
    x2 = x2_from_x1(x1, I, p1, p2)
    u  = utility_ces(x1, x2, alpha, beta)

    if do_print:
        print_solution(x1, x2, u, I, p1, p2)
        print(f'iterations = {it}')