import numpy as np

from grid_solve import print_solution
from A2 import x2_from_x1

def make_foc(alpha,beta,I,p1,p2):
    """Return the FOC f(x1) and its analytic derivative fprime(x1) for the CES problem.

    FOC (interior):  f(x1) = alpha/(1-alpha) * (x2/x1)^(beta+1) - p1/p2 = 0,
    with x2 = (I - p1*x1)/p2.
    """

    def f(x1):
        x2 = x2_from_x1(x1,I,p1,p2)
        return (alpha/(1.0 - alpha)) * ((x2/x1)**(beta + 1.0)) - (p1/p2)

    def fprime(x1):
        x2 = x2_from_x1(x1,I,p1,p2)
        s = alpha/(1.0 - alpha)
        return -s * (beta + 1.0) * (I / (p2 * x1**2)) * ((x2/x1)**beta)

    return f, fprime

def newton(f, df, x0, I, p1, tol=1e-12, max_iter=200):
    """Minimal Newton root-finder, kept inside the interior (0, I/p1)."""

    x = float(x0)
    for it in range(1, max_iter+1):
        
        fx, dfx = f(x), df(x)

        x_new = x - fx/dfx
        x_new = 0.5*(x + 0.5*I/p1)
        
        if abs(x_new - x) < tol:
            return x_new, it
        
        x = x_new

    return x, max_iter

def solve_with_newton(alpha,beta,I,p1,p2,x0=None,do_print=True):
    """Solve the CES FOC with Newton using the analytic derivative and print the result."""

    f, fprime = make_foc(alpha,beta,I,p1,p2)
    if x0 is None: x0 = 0.4*(I/p1)

    x1, it = newton(f, fprime, x0, I, p1)
    x2 = x2_from_x1(x1,I,p1,p2)
    
    if do_print:
        print_solution(x1,x2,f(x1),I,p1,p2)
        print(f'iterations = {it}')

def solve_with_newton_numderiv(alpha,beta,I,p1,p2,x0=None,Delta=1e-8,do_print=True):
    """Solve the CES FOC with Newton using a forward-difference derivative and print the result."""
    
    f, _ = make_foc(alpha,beta,I,p1,p2)
    fprime_num = lambda x1: (f(x1+Delta) - f(x1))/Delta
    
    if x0 is None: x0 = 0.4*(I/p1)
    
    x1, it = newton(f, fprime_num, x0, I, p1)
    x2 = x2_from_x1(x1,I,p1,p2)
    
    if do_print:
        print_solution(x1,x2,f(x1),I,p1,p2)
        print(f'iterations = {it}')
