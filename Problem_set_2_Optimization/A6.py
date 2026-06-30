from scipy import optimize

from grid_solve import print_solution
from A2 import x2_from_x1
from A5 import make_foc

def value_of_choice_ces(u_func,x1,alpha,beta,I,p1,p2):
    """Utility along the budget line (choose x1, spend the rest on x2)."""
    
    x2 = x2_from_x1(x1,I,p1,p2)
    
    return u_func(x1,x2,alpha=alpha,beta=beta)

def solve_with_scipy_minimize(u_func,alpha,beta,I,p1,p2,do_print=True):
    """Solve by minimizing -u along the budget line with minimize_scalar and print the result."""
    
    obj = lambda x1: -value_of_choice_ces(u_func,x1,alpha,beta,I,p1,p2)
    res = optimize.minimize_scalar(obj, bounds=(0,I/p1), method='bounded')
    x1 = res.x
    x2 = x2_from_x1(x1,I,p1,p2)
    u  = -res.fun
    
    if do_print:
        print_solution(x1,x2,u,I,p1,p2)
        print(f'iterations = {res.nit}')
        print(f'function_calls = {res.nfev}')

def solve_with_scipy_root_scalar(u_func,alpha,beta,I,p1,p2,do_print=True):
    """Solve the FOC f(x1)=0 with Brent's method (brentq) and print the result."""
    
    f, _ = make_foc(alpha,beta,I,p1,p2)
    eps = 1e-8
    res = optimize.root_scalar(f, bracket=[eps, I/p1-eps], method='brentq')
    x1 = res.root
    x2 = x2_from_x1(x1,I,p1,p2)
    
    if do_print:
        u = value_of_choice_ces(u_func,x1,alpha,beta,I,p1,p2)
        print_solution(x1,x2,u,I,p1,p2)
        print(f'iterations = {res.iterations}')
        print(f'function_calls = {res.function_calls}')
