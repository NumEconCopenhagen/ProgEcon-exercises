import numpy as np

from solow import SolowModel # the model from the lecture

def k_star(alpha,s,delta,g,n):
    """ steady-state capital per effective worker

    Args:

        alpha (float): capital share in production
        s (float): savings rate
        delta (float): depreciation rate
        g (float): growth rate of technology
        n (float): growth rate of the population

    Returns:

        (float): capital per effective worker in the steady state

    """

    break_even = (1+g)*(1+n)-(1-delta) # what investment must cover in the steady state

    return (s/break_even)**(1/(1-alpha))

def run(alpha=1/3,s=0.20,delta=0.30,g=0.03,n=0.04):
    """ print the steady state and test the special case without growth """

    # a. the steady state with growth
    print(f'parameters: alpha = {alpha:.2f}, s = {s:.2f}, delta = {delta:.2f}, g = {g:.2f}, n = {n:.2f}')
    print(f'steady state: k* = {k_star(alpha,s,delta,g,n):.4f} (per effective worker)')

    # b. test: without growth we must get exactly the model from the lecture
    k_star_no_growth = k_star(alpha,s,delta,0.0,0.0)
    k_star_lecture = SolowModel(alpha=alpha,s=s,delta=delta).steady_state()[0]

    print('')
    print(f'without growth (g=n=0): k* = {k_star_no_growth:.4f}')
    print(f'the model from lecture 9: k* = {k_star_lecture:.4f}')

    assert np.isclose(k_star_no_growth,k_star_lecture), 'the special case g=n=0 is wrong'
    print('test passed')

    # c. how much does growth cost in terms of capital?
    loss = k_star(alpha,s,delta,g,n)/k_star_no_growth-1
    print('')
    print(f'growth in A and L lowers k* by {-loss*100:.1f} percent')
