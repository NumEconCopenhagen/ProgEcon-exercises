import numpy as np

import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from exchangeCES import ExchangeEconomyCES

# the three equilibria, found with pen and paper
P1_EQS = [27/64,1.0,64/27]

##############
# algorithms #
##############

def tatonnement(model,p1_guess,nu=50.0,tol=1e-8,maxiter=5000):
    """ the auction algorithm from the lecture

    Args:

        model (ExchangeEconomyCES): the economy
        p1_guess (float): the first price called
        nu (float): step size
        tol (float): stop when excess demand is this close to zero
        maxiter (int): give up after this many rounds

    Returns:

        (float): the last price called
        (bool): True if excess demand got below tol
        (ndarray): the price called in each round
        (ndarray): excess demand in each round

    """

    p1 = p1_guess
    p1_path = []
    eps1_path = []

    for k in range(maxiter):

        # a. excess demand at the price called
        eps1 = model.excess_demand(p1)[0]

        p1_path.append(p1)
        eps1_path.append(eps1)

        # b. done?
        if np.abs(eps1) < tol:
            return p1,True,np.array(p1_path),np.array(eps1_path)

        # c. call a new price
        p1 = p1 + nu*eps1

        # d. a price can never be negative
        if p1 <= 0: return p1,False,np.array(p1_path),np.array(eps1_path)

    return p1,False,np.array(p1_path),np.array(eps1_path)

def newton_raphson(model,p1_guess,phi=0.1,iota=0.99,h=1e-6,tol=1e-8,maxiter=5000):
    """ the dampened Newton-Raphson algorithm

    Instead of stepping with excess demand itself, we step with excess demand
    divided by its slope - i.e. with the distance to where the *straight line*
    through the current point crosses zero.

    Args:

        model (ExchangeEconomyCES): the economy
        p1_guess (float): the first price tried
        phi (float): dampening, only phi of the full Newton step is taken
        iota (float): the price is multiplied by this if the step goes negative
        h (float): step size in the numerical derivative
        tol (float): stop when excess demand is this close to zero
        maxiter (int): give up after this many rounds

    Returns:

        (float): the last price tried
        (bool): True if excess demand got below tol
        (ndarray): the price tried in each round
        (ndarray): excess demand in each round

    """

    p1 = p1_guess
    p1_path = []
    eps1_path = []

    for k in range(maxiter):

        # a. excess demand at the current price
        eps1 = model.excess_demand(p1)[0]

        p1_path.append(p1)
        eps1_path.append(eps1)

        # b. done?
        if np.abs(eps1) < tol:
            return p1,True,np.array(p1_path),np.array(eps1_path)

        # c. the slope of excess demand, found numerically
        deps1 = (model.excess_demand(p1+h)[0]-eps1)/h

        # d. the dampened Newton step
        p1_new = p1 - phi*eps1/deps1

        # e. never allow a negative price
        p1 = iota*p1 if p1_new <= 0 else p1_new

    return p1,False,np.array(p1_path),np.array(eps1_path)

#############
# questions #
#############

def question_1(model):
    """ demand and excess demand on a grid of prices """

    p1_grid = np.linspace(0.25,5,100)

    x1A_grid,_ = model.demand_A(p1_grid)
    x1B_grid,_ = model.demand_B(p1_grid)
    eps1_grid = x1A_grid + x1B_grid - 1.0

    fig = plt.figure(figsize=(13,5))

    # a. demand
    ax = fig.add_subplot(1,2,1)

    ax.plot(p1_grid,x1A_grid,lw=2,color=colors[0],label='$x_1^{A}(p_1)$')
    ax.plot(p1_grid,x1B_grid,lw=2,color=colors[1],label='$x_1^{B}(p_1)$')
    ax.plot(p1_grid,x1A_grid+x1B_grid,lw=2,ls='--',color='black',label='together')

    ax.set_title('Demand for good 1')
    ax.set_ylabel('$x_1$')
    ax.legend(loc='center right',fontsize=12)

    # b. excess demand
    ax = fig.add_subplot(1,2,2)

    ax.plot(p1_grid,eps1_grid,lw=2,color=colors[0])
    ax.axhline(0,lw=1.5,color='black')

    for p1_eq in P1_EQS:
        ax.axvline(p1_eq,ls='--',lw=1.5,color='gray')

    ax.set_title(r'Excess demand for good 1, $\varepsilon_1(p_1)$')
    ax.set_ylabel('wanted minus available')

    for ax in fig.axes:
        ax.set_xlabel('price of good 1, $p_1$')
        ax.set_xlim(p1_grid[0],p1_grid[-1])

    fig.tight_layout()
    plt.show()

    print('excess demand is *tiny* everywhere - never more than'
          f' {np.abs(eps1_grid).max():.4f} in absolute value - and it crosses zero three times.')
    print('there are three equilibria:')
    for p1_eq in P1_EQS:
        print(f'  p1* = {p1_eq:.6f} with excess demand {model.excess_demand(p1_eq)[0]:.2e}')
    print('')
    print('note that you have to look closely to see this: on a figure where the y-axis ran')
    print('from -1 to 1 the whole curve would look like a flat line lying on top of zero.')

def question_2(model):
    """ the auction algorithm from two different starting points """

    p_guesses = [0.9,1.1]

    fig = plt.figure(figsize=(13,5))
    ax_p = fig.add_subplot(1,2,1)
    ax_e = fig.add_subplot(1,2,2)

    for i,p_guess in enumerate(p_guesses):

        p1,converged,p1_path,eps1_path = tatonnement(model,p_guess)

        print(f'from p1 = {p_guess:.2f}: converged = {converged} after {p1_path.size:3d} rounds'
              f' -> p1* = {p1:.8f}')

        ax_p.plot(p1_path,'-o',ms=3,lw=1.5,color=colors[i],label=f'$p_1^0={p_guess:.1f}$')
        ax_e.plot(np.fmax(np.abs(eps1_path),1e-16),'-o',ms=3,lw=1.5,color=colors[i],
                  label=f'$p_1^0={p_guess:.1f}$')

    for p1_eq in P1_EQS:
        ax_p.axhline(p1_eq,ls='--',lw=1.5,color='gray')

    ax_p.set_title('The price called by the auctioneer')
    ax_p.set_ylabel('$p_1^k$')

    ax_e.set_title('Distance from equilibrium')
    ax_e.set_ylabel(r'$|\varepsilon_1^k|$')
    ax_e.set_yscale('log')

    for ax in fig.axes:
        ax.set_xlabel('round, $k$')
        ax.legend(loc='upper right',fontsize=12)

    fig.tight_layout()
    plt.show()

    print('')
    print('yes - the guess decides everything. Starting just below 1 the auctioneer walks')
    print('down to 27/64, starting just above it he walks up to 64/27. The algorithm always')
    print('moves the price in the direction excess demand points, and around p1 = 1 that')
    print('direction is *away* from the equilibrium.')

def question_3(model):
    """ the auction algorithm from many different starting points """

    p_guesses = np.linspace(0.25,5.0,50)

    p1_eqs = np.empty(p_guesses.size)
    for i,p_guess in enumerate(p_guesses):
        p1_eqs[i],converged,_,_ = tatonnement(model,p_guess)
        assert converged, f'no convergence from p1 = {p_guess:.2f}'

    plot_guesses(p_guesses,p1_eqs,'Tâtonnement')

    print(f'the algorithm ends in {np.unique(np.round(p1_eqs,4)).size} different places:')
    for p1_eq in np.unique(np.round(p1_eqs,4)):
        print(f'  p1* = {p1_eq:.4f} from {np.sum(np.isclose(np.round(p1_eqs,4),p1_eq))} of the 50 guesses')

    print('')
    print('no - the middle equilibrium, p1* = 1, is never found. Every single guess ends in')
    print('one of the two outer ones.')

def question_4(model):
    """ the dampened Newton-Raphson algorithm from many different starting points """

    p_guesses = np.linspace(0.25,5.0,50)

    p1_eqs = np.empty(p_guesses.size)
    for i,p_guess in enumerate(p_guesses):
        p1_eqs[i],converged,_,_ = newton_raphson(model,p_guess)
        assert converged, f'no convergence from p1 = {p_guess:.2f}'

    plot_guesses(p_guesses,p1_eqs,'Dampened Newton-Raphson')

    print(f'the algorithm ends in {np.unique(np.round(p1_eqs,4)).size} different places:')
    for p1_eq in np.unique(np.round(p1_eqs,4)):
        print(f'  p1* = {p1_eq:.4f} from {np.sum(np.isclose(np.round(p1_eqs,4),p1_eq))} of the 50 guesses')

    print('')
    print('yes - now all three are found, the middle one included.')
    print('')
    print('why? Because Newton-Raphson does not care which *way* excess demand points, only')
    print('where the straight line through the current point crosses zero. Dividing by the')
    print('slope flips the step whenever the slope is positive, and that is exactly what goes')
    print('wrong for the auctioneer around p1 = 1.')
    print('')
    print('note what all this means: "the" equilibrium is not always a single point. Which one')
    print('your code reports can depend on the algorithm and on where you started it - so a')
    print('number that comes out of a solver is not automatically *the* answer.')

def plot_guesses(p_guesses,p1_eqs,title):
    """ the starting guess against the equilibrium it leads to """

    fig = plt.figure(figsize=(7,5))
    ax = fig.add_subplot(1,1,1)

    for p1_eq in P1_EQS:
        ax.axhline(p1_eq,ls='--',lw=1.5,color='gray')

    ax.plot(p_guesses,p1_eqs,'-o',ms=5,lw=1.5,color=colors[0])

    ax.set_title(title)
    ax.set_xlabel('starting guess, $p_1^0$')
    ax.set_ylabel('equilibrium found, $p_1^*$')
    ax.set_yticks(P1_EQS)
    ax.set_yticklabels(['27/64','1','64/27'])

    fig.tight_layout()
    plt.show()

def run():
    """ all four questions """

    model = ExchangeEconomyCES()
    print(model)

    for i,question in enumerate([question_1,question_2,question_3,question_4]):
        print('')
        print(f'--- question {i+1} ---')
        print('')
        question(model)
