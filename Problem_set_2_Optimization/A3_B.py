import numpy as np

from grid_solve import print_solution
from A2 import x2_from_x1

def find_best_choice_monotone(u_func,alpha,beta,I,p1,p2,N,do_print=True):
    """1D grid search on the budget line (exploits monotonicity of CES utility)."""

    # a. grid for x1 on the budget line, x2 is the rest of the budget
    x1_values = np.linspace(0,I/p1,N)
    x2_values = x2_from_x1(x1_values, I, p1, p2)

    # b. utility at each point (endpoints have x1=0 or x2=0 -> not allowed)
    u_values = np.empty(N)
    for i in range(N):
        x1 = x1_values[i]
        x2 = x2_values[i]
        if x1 > 0 and x2 > 0:
            u_values[i] = u_func(x1,x2,alpha=alpha,beta=beta)
        else:
            u_values[i] = -np.inf

    # c. find the best point
    i_best  = np.argmax(u_values)
    x1_best = x1_values[i_best]
    x2_best = x2_values[i_best]
    u_best  = u_values[i_best]

    # d. print
    if do_print:
        print_solution(x1_best,x2_best,u_best,I,p1,p2)
