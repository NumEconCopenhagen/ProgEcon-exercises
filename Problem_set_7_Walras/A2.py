import numpy as np

import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from exchange import ExchangeEconomy # the model from the lecture

class QuasiLinearEconomy(ExchangeEconomy):
    """ the exchange economy from the lecture, but with quasi-linear preferences

    Only the five methods that actually change are written here. Everything else -
    excess_demand, solve, solve_equilibrium_price and tatonnement - is inherited
    from ExchangeEconomy and works unchanged.

    """

    def __init__(self,**kwargs):
        """ set the new parameters, then let the parent class do the rest """

        # a. the new preference parameters
        self.aA = 1.0 # A's taste for good 1
        self.aB = 1.5 # B's taste for good 1

        # b. everything else, including the keyword arguments
        super().__init__(**kwargs)

    def __str__(self):
        """ called when using print """

        text = 'Exchange economy with quasi-linear preferences:\n'
        text += f'  aA = {self.aA:.2f} (A\'s taste for good 1)\n'
        text += f'  aB = {self.aB:.2f} (B\'s taste for good 1)\n'
        text += f'  wA = ({self.w1A:.2f},{self.w2A:.2f}) (what A owns)\n'
        text += f'  wB = ({1-self.w1A:.2f},{1-self.w2A:.2f}) (what B owns)'

        return text

    ##########################
    # preferences and demand #
    ##########################

    def utility_A(self,x1,x2):
        """ A's utility of consuming x1 of good 1 and x2 of good 2 """

        return self.aA*np.sqrt(x1) + x2

    def utility_B(self,x1,x2):
        """ B's utility of consuming x1 of good 1 and x2 of good 2 """

        return self.aB*np.sqrt(x1) + x2

    def demand_A(self,p1):
        """ A's demand at the price p1, returns (x1,x2) """

        m = p1*self.w1A + self.w2A # the value of what A owns
        x1 = (self.aA/(2*p1))**2 # does not depend on m!

        return x1, m-p1*x1

    def demand_B(self,p1):
        """ B's demand at the price p1, returns (x1,x2) """

        m = p1*(1-self.w1A) + (1-self.w2A) # the value of what B owns
        x1 = (self.aB/(2*p1))**2 # does not depend on m!

        return x1, m-p1*x1

    #########################
    # the equilibrium price #
    #########################

    def equilibrium_price(self):
        """ the analytical equilibrium price of good 1 """

        return np.sqrt(self.aA**2 + self.aB**2)/2

def run():
    """ solve the quasi-linear economy and compare it with the lecture model """

    model = QuasiLinearEconomy()
    lecture = ExchangeEconomy()

    print(model)

    # a. the price, by hand and numerically
    p_hand = model.equilibrium_price()
    p_root = model.solve_equilibrium_price() # inherited, and it still works

    print('')
    print(f'p1* (by hand)     = {p_hand:.10f}')
    print(f'p1* (root-finder) = {p_root:.10f}')
    assert np.isclose(p_hand,p_root), 'the root-finder does not agree with the formula'

    # b. test: Walras' law at every price
    p1_grid = np.linspace(0.2,3.0,500)
    eps1_grid,eps2_grid = model.excess_demand(p1_grid) # also inherited
    assert np.allclose(p1_grid*eps1_grid+eps2_grid,0.0), "Walras' law is violated"

    # c. test: both markets clear in equilibrium
    sol = model.solve()
    assert np.isclose(sol.x1A+sol.x1B,1.0), 'good 1 does not add up'
    assert np.isclose(sol.x2A+sol.x2B,1.0), 'good 2 does not add up'

    print('')
    print('all tests passed')

    # d. the allocation
    uA_w = model.utility_A(model.w1A,model.w2A)
    uB_w = model.utility_B(1-model.w1A,1-model.w2A)

    print('')
    print(f'A consumes ({sol.x1A:.4f},{sol.x2A:.4f}) and had ({model.w1A:.2f},{model.w2A:.2f})')
    print(f'B consumes ({sol.x1B:.4f},{sol.x2B:.4f}) and had ({1-model.w1A:.2f},{1-model.w2A:.2f})')
    print(f'A: {uA_w:.4f} -> {sol.uA:.4f}, B: {uB_w:.4f} -> {sol.uB:.4f}')

    # e. the price for a whole grid of endowments, here and in the lecture model
    w1A_grid = np.linspace(0.01,0.99,200)

    p1_quasi = np.array([QuasiLinearEconomy(w1A=w1A).equilibrium_price() for w1A in w1A_grid])
    p1_lecture = np.array([ExchangeEconomy(w1A=w1A).equilibrium_price() for w1A in w1A_grid])

    # f. figure
    fig = plt.figure(figsize=(13,5))

    # i. excess demand
    ax = fig.add_subplot(1,2,1)

    ax.plot(p1_grid,eps1_grid,lw=2,color=colors[0],label=r'good 1, $\varepsilon_1(p_1)$')
    ax.plot(p1_grid,eps2_grid,lw=2,color=colors[1],label=r'good 2, $\varepsilon_2(p_1)$')
    ax.axhline(0,lw=1.5,color='black')
    ax.axvline(p_hand,ls='--',lw=1.5,color='black',label=f'$p_1^*={p_hand:.4f}$')

    ax.set_title('Excess demand')
    ax.set_xlabel('price of good 1, $p_1$')
    ax.set_ylabel('wanted minus available')
    ax.set_xlim(p1_grid[0],p1_grid[-1])
    ax.set_ylim(-1,2)
    ax.legend(loc='upper right',fontsize=12)

    # ii. the price against A's endowment
    ax = fig.add_subplot(1,2,2)

    ax.plot(w1A_grid,p1_quasi,lw=2,color=colors[0],label='quasi-linear')
    ax.plot(w1A_grid,p1_lecture,lw=2,ls='--',color=colors[1],label='Cobb-Douglas (the lecture)')

    ax.set_title('The equilibrium price and who owns what')
    ax.set_xlabel('what A owns of good 1, $\\omega_1^A$')
    ax.set_ylabel('$p_1^*$')
    ax.set_xlim(0,1)
    ax.set_ylim(0,None)
    ax.legend(loc='upper right',fontsize=12)

    fig.tight_layout()
    plt.show()

    print('')
    print('the whole point of the new functional form is in the formula for the demand for')
    print('good 1: it contains no m at all. Whatever A is given, she wants exactly the same')
    print('amount of good 1 - the endowment only changes how much of good 2 is left over.')
    print('')
    print('so the equilibrium price is a flat line: it depends on the two tastes and on')
    print(f'nothing else. In the lecture model it falls from {p1_lecture[0]:.2f} to'
          f' {p1_lecture[-1]:.2f} across the same')
    print('grid. Note that we did not have to change a single line of the machinery to find')
    print('this out - excess_demand, solve, solve_equilibrium_price and tatonnement were all')
    print('inherited and worked unchanged, because they only ever call demand_A and demand_B.')
