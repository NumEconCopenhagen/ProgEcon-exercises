import numpy as np
from scipy import optimize

import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

def demand(p,a=10.0,b=1.0):
    """ how much the buyers want at the price p """

    return a-b*p

def supply(p,c=2.0,d=1.0):
    """ how much the sellers offer at the price p """

    return c+d*p

def excess_demand(p,**kwargs):
    """ wanted minus offered """

    return demand(p,**kwargs)-supply(p,**kwargs)

def tatonnement(p_guess,nu,tol=1e-8,maxiter=200):
    """ the auction algorithm from the lecture

    Args:

        p_guess (float): the first price called
        nu (float): step size
        tol (float): stop when excess demand is this close to zero
        maxiter (int): give up after this many rounds

    Returns:

        (ndarray): the price called in each round
        (bool): True if excess demand got below tol

    """

    p = p_guess
    path = [p]

    for k in range(maxiter):

        Z = excess_demand(p)

        if np.abs(Z) < tol: return np.array(path),True

        p = p + nu*Z
        path.append(p)

    return np.array(path),False

def run(a=10.0,b=1.0,c=2.0,d=1.0):
    """ solve the market by hand, with a root-finder and with the auction algorithm """

    # a. by hand
    p_hand = (a-c)/(b+d)
    q_hand = demand(p_hand,a=a,b=b)

    print(f'by hand      : p* = {p_hand:.8f}, q* = {q_hand:.4f}')

    # b. with a root-finder
    result = optimize.root_scalar(excess_demand,bracket=[0.0,20.0],method='brentq')
    p_root = result.root

    print(f'root-finder  : p* = {p_root:.8f} ({result.iterations} iterations)')
    assert np.isclose(p_hand,p_root), 'the root-finder does not agree with the formula'

    # c. with the auction algorithm
    print('')
    for nu in [0.05,0.10,0.50,1.10]:
        path,converged = tatonnement(p_guess=5.0,nu=nu)
        print(f'nu = {nu:.2f}: converged = {str(converged):5s} after {path.size:3d} prices, last price = {path[-1]:12.4f}')

    # d. figure
    fig = plt.figure(figsize=(13,5))

    # i. supply and demand
    ax = fig.add_subplot(1,2,1)

    p_grid = np.linspace(0,10,100)
    ax.plot(demand(p_grid,a=a,b=b),p_grid,lw=2,color=colors[0],label='demand, $D(p)$')
    ax.plot(supply(p_grid,c=c,d=d),p_grid,lw=2,color=colors[1],label='supply, $S(p)$')

    ax.plot(q_hand,p_hand,'o',ms=9,color='black',zorder=3)
    ax.annotate(f'$p^*={p_hand:.1f}$, $q^*={q_hand:.1f}$',xy=(q_hand,p_hand),xytext=(1.0,7.5),
                arrowprops=dict(arrowstyle='->'),fontsize=13,backgroundcolor='white')

    ax.set_title('The market')
    ax.set_xlabel('quantity, $q$')
    ax.set_ylabel('price, $p$')
    ax.set_xlim(0,12)
    ax.set_ylim(0,10)
    ax.legend(loc='upper right',fontsize=12)

    # ii. the auction: distance to the equilibrium price
    ax = fig.add_subplot(1,2,2)

    for i,nu in enumerate([0.05,0.10,0.50,1.10]):
        path,converged = tatonnement(p_guess=5.0,nu=nu)
        distance = np.fmax(np.abs(path-p_hand),1e-16) # a log scale cannot show an exact zero
        ax.plot(distance,'-o',ms=3,lw=1.5,color=colors[i],label=fr'$\nu={nu:.2f}$')

    ax.set_title('Distance to $p^*$ in the auction')
    ax.set_xlabel('round, $k$')
    ax.set_ylabel('$|p_k-p^*|$')
    ax.set_yscale('log')
    ax.set_xlim(0,40)
    ax.legend(loc='lower left',fontsize=12)

    fig.tight_layout()
    plt.show()

    print('')
    print('the auction only works when the step size is small enough:')
    print('here the new price is p + nu*(8-2p), so the distance to p* = 4 is')
    print('multiplied by 1-2*nu in every round. It only shrinks when |1-2*nu| < 1,')
    print('that is for nu < 1. With nu = 0.50 the factor is exactly 0, so the very')
    print('first round lands on p* - and with nu = 1.10 the price explodes.')
