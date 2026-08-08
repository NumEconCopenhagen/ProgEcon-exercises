from types import SimpleNamespace

import numpy as np
from scipy import optimize

import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from exchange import ExchangeEconomy # the model from the lecture

# the economy used in question 3
ALPHAS = [0.20,0.30,0.60,0.80]
W1 = [0.90,0.60,0.30,0.10]
W2 = [0.10,0.30,0.60,0.90]

class ExchangeEconomyN:
    """ an exchange economy with N consumers, two goods and Cobb-Douglas preferences """

    def __init__(self,alphas,w1,w2,**kwargs):
        """ set the parameters, then overwrite with any keyword arguments

        Args:

            alphas (array_like): the share of her income each consumer spends on good 1
            w1 (array_like): what each consumer owns of good 1
            w2 (array_like): what each consumer owns of good 2

        """

        # a. parameters, all with one element per consumer
        self.alphas = np.asarray(alphas,dtype=float)
        self.w1 = np.asarray(w1,dtype=float)
        self.w2 = np.asarray(w2,dtype=float)

        # b. useful sizes
        self.N = self.alphas.size # number of consumers
        self.W1 = self.w1.sum() # how much of good 1 exists
        self.W2 = self.w2.sum() # how much of good 2 exists

        # c. overwrite with keyword arguments
        for key,value in kwargs.items():
            setattr(self,key,value)

        # d. empty container for the solution
        self.sol = SimpleNamespace()

    def __str__(self):
        """ called when using print """

        text = f'Exchange economy with {self.N} consumers:\n'
        text += f'   i   alpha     w1     w2\n'
        for i in range(self.N):
            text += f'  {i+1:2d}   {self.alphas[i]:5.2f}  {self.w1[i]:5.2f}  {self.w2[i]:5.2f}\n'
        text += f'  total of good 1 = {self.W1:.2f}, of good 2 = {self.W2:.2f}'

        return text

    ##########################
    # preferences and demand #
    ##########################

    def utility(self,x1,x2):
        """ the utility of every consumer, returns an array with N elements """

        return x1**self.alphas * x2**(1-self.alphas)

    def demand(self,p1):
        """ the demand of every consumer at the price p1, returns two arrays with N elements """

        m = p1*self.w1 + self.w2 # the value of what each consumer owns

        return self.alphas*m/p1, (1-self.alphas)*m

    def excess_demand(self,p1):
        """ how much more of each good is wanted than exists, returns (eps1,eps2) """

        x1,x2 = self.demand(p1)

        return x1.sum()-self.W1, x2.sum()-self.W2

    #########################
    # the equilibrium price #
    #########################

    def equilibrium_price(self):
        """ the analytical equilibrium price of good 1 """

        top = (self.alphas*self.w2).sum()
        bottom = ((1-self.alphas)*self.w1).sum()

        return top/bottom

    def solve_equilibrium_price(self,bracket=[0.01,100.0]):
        """ the equilibrium price, found numerically as the root of excess demand """

        obj = lambda p1: self.excess_demand(p1)[0]
        result = optimize.root_scalar(obj,bracket=bracket,method='brentq')

        return result.root

    def solve(self,p1=None):
        """ store the price, the allocation and the utilities in self.sol """

        if p1 is None: p1 = self.equilibrium_price()

        sol = self.sol
        sol.p1 = p1
        sol.x1,sol.x2 = self.demand(p1)
        sol.u = self.utility(sol.x1,sol.x2) # utility after trading
        sol.u_w = self.utility(self.w1,self.w2) # utility of just keeping the endowment
        sol.gain = sol.u/sol.u_w-1 # the relative gain from trading

        return sol

def run(alphas=ALPHAS,w1=W1,w2=W2):
    """ solve the N-consumer economy and test it against the model from the lecture """

    # a. the economy
    model = ExchangeEconomyN(alphas,w1,w2)
    print(model)

    # b. the price, by hand and numerically
    p_hand = model.equilibrium_price()
    p_root = model.solve_equilibrium_price()

    print('')
    print(f'p1* (by hand)     = {p_hand:.10f}')
    print(f'p1* (root-finder) = {p_root:.10f}')
    assert np.isclose(p_hand,p_root), 'the root-finder does not agree with the formula'

    # c. test 1: with N = 2 we must reproduce the model from the lecture
    lecture = ExchangeEconomy()
    same = ExchangeEconomyN([lecture.alpha,lecture.beta],
                            [lecture.w1A,1-lecture.w1A],
                            [lecture.w2A,1-lecture.w2A])

    sol_same = same.solve()
    sol_lecture = lecture.solve()

    print('')
    print(f'the lecture model:  p1* = {sol_lecture.p1:.10f}, x1 of consumer 1 = {sol_lecture.x1A:.10f}')
    print(f'this class, N = 2:  p1* = {sol_same.p1:.10f}, x1 of consumer 1 = {sol_same.x1[0]:.10f}')
    assert np.isclose(sol_same.p1,sol_lecture.p1), 'N = 2 is not the lecture model'
    assert np.isclose(sol_same.x1[0],sol_lecture.x1A), 'the allocation is not the same either'

    # d. test 2: Walras' law at every price
    p1_grid = np.linspace(0.2,3.0,500)
    eps1 = np.array([model.excess_demand(p1)[0] for p1 in p1_grid])
    eps2 = np.array([model.excess_demand(p1)[1] for p1 in p1_grid])
    assert np.allclose(p1_grid*eps1+eps2,0.0), "Walras' law is violated"

    print('')
    print('all tests passed')

    # e. the allocation
    sol = model.solve()

    print('')
    print('   i   alpha     w1     w2  ->     x1     x2   gain')
    for i in range(model.N):
        print(f'  {i+1:2d}   {model.alphas[i]:5.2f}  {model.w1[i]:5.2f}  {model.w2[i]:5.2f}  ->'
              f'  {sol.x1[i]:5.2f}  {sol.x2[i]:5.2f}  {sol.gain[i]*100:5.1f}%')

    # f. figure: who buys and who sells good 1?
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_subplot(1,1,1)

    i_grid = np.arange(model.N)
    ax.bar(i_grid-0.2,model.w1,width=0.4,color=colors[0],label='owned, $\\omega_{1i}$')
    ax.bar(i_grid+0.2,sol.x1,width=0.4,color=colors[1],label='consumed, $x_{1i}$')

    ax.set_title(f'Good 1: who buys and who sells? ($p_1^*={sol.p1:.3f}$)')
    ax.set_xlabel('consumer, $i$')
    ax.set_ylabel('good 1')
    ax.set_xticks(i_grid)
    ax.set_xticklabels([f'{i+1}\n' + r'$\alpha=$' + f'{a:.1f}' for i,a in enumerate(model.alphas)])
    ax.legend(loc='upper right',fontsize=12)

    fig.tight_layout()
    plt.show()

    print('')
    print('consumers 1 and 2 own a lot of good 1 but do not care much for it, so they sell.')
    print('consumers 3 and 4 are the other way around, so they buy. The price settles where')
    print('what the sellers offer is exactly what the buyers want.')
