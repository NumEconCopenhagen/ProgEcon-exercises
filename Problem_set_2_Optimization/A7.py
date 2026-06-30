import numpy as np, time
from scipy import optimize

from grid_solve import print_solution
from A2 import x2_from_x1

def compare_optimizers(u_func,alpha,beta,I,p1,p2,eps=1e-10):
    """Solve the consumer problem with SLSQP and Nelder-Mead and compare them."""

    # a. objective along the budget line (penalize infeasible points)
    def obj(x, alpha, beta):
        
        x1 = float(x[0])
        x2 = x2_from_x1(x1, I, p1, p2)
        if x1 <= 0 or x1 >= I/p1 or x2 <= 0:
            return 1e12
        
        return -u_func(x1, x2, alpha, beta)

    x0 = np.array([I/(2*p1)])

    # b. SLSQP (bounded)
    print("\nSLSQP (bounded)")
    t0 = time.perf_counter()
    res_slsqp = optimize.minimize(obj, x0=x0, args=(alpha, beta),
                                  bounds=[(eps, I/p1 - eps)], method='SLSQP')
    t1 = time.perf_counter()
    
    x1_s = float(res_slsqp.x[0]); x2_s = x2_from_x1(x1_s, I, p1, p2)
    
    print_solution(x1_s, x2_s, u_func(x1_s, x2_s, alpha, beta), I, p1, p2)
    print(f'iterations = {res_slsqp.nit}  function_calls = {res_slsqp.nfev}')
    print(f'time = {(t1-t0)*1e3:.1f} ms')

    # d. Nelder-Mead (unconstrained; same penalized objective)
    print("\nNelder-Mead (unconstrained)")
    t0 = time.perf_counter()
    res_nm = optimize.minimize(obj, x0=x0, args=(alpha, beta), method='Nelder-Mead')
    t1 = time.perf_counter()
    
    x1_n = float(res_nm.x[0]); x2_n = x2_from_x1(x1_n, I, p1, p2)
    
    print_solution(x1_n, x2_n, u_func(x1_n, x2_n, alpha, beta), I, p1, p2)
    print(f'iterations = {res_nm.nit}  function_calls = {res_nm.nfev}')
    print(f'time = {(t1-t0)*1e3:.1f} ms')