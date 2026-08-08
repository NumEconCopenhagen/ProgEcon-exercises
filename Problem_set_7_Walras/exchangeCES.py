""" an exchange economy with CES preferences, used in problem 3

Same two consumers, two goods and numeraire p2 = 1 as in the lecture - only the
utility function is changed from Cobb-Douglas to CES. Everything below is written
for you: the preferences, the demand functions and excess demand. What is missing
is the *solvers*, and that is what you write in the problem set.

"""

from types import SimpleNamespace
import numpy as np

import matplotlib.pyplot as plt

class ExchangeEconomyCES:
    """ an exchange economy with two consumers, two goods and CES preferences """

    def __init__(self,**kwargs):
        """ set the default parameters, then overwrite with any keyword arguments """

        # a. A's preferences
        self.alphaA = 1.0 # A's weight on good 1
        self.betaA = (12/37)**3 # A's weight on good 2
        self.rhoA = -2.0 # A's elasticity parameter

        # b. B's preferences (the mirror image of A's)
        self.alphaB = (12/37)**3 # B's weight on good 1
        self.betaB = 1.0 # B's weight on good 2
        self.rhoB = -2.0 # B's elasticity parameter

        # c. endowments: A owns (almost) all of good 1, B (almost) all of good 2
        self.w1A = 1.0-1e-8 # what A owns of good 1
        self.w2A = 1e-8 # what A owns of good 2

        # d. overwrite with keyword arguments, e.g. ExchangeEconomyCES(rhoA=-1.0)
        for key,value in kwargs.items():
            setattr(self,key,value)

        # e. empty container for the solution
        self.sol = SimpleNamespace()

    def __str__(self):
        """ called when using print """

        text = 'Exchange economy with CES preferences:\n'
        text += f'  A: alpha = {self.alphaA:.4f}, beta = {self.betaA:.4f}, rho = {self.rhoA:.2f}\n'
        text += f'  B: alpha = {self.alphaB:.4f}, beta = {self.betaB:.4f}, rho = {self.rhoB:.2f}\n'
        text += f'  wA = ({self.w1A:.4f},{self.w2A:.4f}) (what A owns)\n'
        text += f'  wB = ({1-self.w1A:.4f},{1-self.w2A:.4f}) (what B owns)'

        return text

    ###############################
    # the general CES formulas    #
    ###############################

    def CES_utility(self,x1,x2,alpha,beta,rho):
        """ the CES utility of consuming x1 of good 1 and x2 of good 2 """

        return (alpha*x1**rho + beta*x2**rho)**(1/rho)

    def CES_indifference(self,u,x1,alpha,beta,rho):
        """ the indifference curve for the utility level u, solved for x2

        Returns nan where the utility level u cannot be reached with this x1.

        """

        x1 = np.asarray(x1,dtype=float)
        x2 = np.nan*np.ones_like(x1)

        temp = (u**rho - alpha*x1**rho)/beta
        I = temp >= 0
        x2[I] = temp[I]**(1/rho)

        return x2

    def CES_demand(self,p1,m,alpha,beta,rho):
        """ the demand at the price p1 with income m, returns (x1,x2) """

        sigma = 1/(1-rho)

        fac1 = alpha**sigma*p1**(1-sigma)
        fac2 = beta**sigma
        denom = fac1 + fac2

        x1 = fac1/p1*m/denom
        x2 = fac2*m/denom

        return x1,x2

    ##########################
    # preferences and demand #
    ##########################

    def utility_A(self,x1,x2):
        """ A's utility of consuming x1 of good 1 and x2 of good 2 """

        return self.CES_utility(x1,x2,self.alphaA,self.betaA,self.rhoA)

    def utility_B(self,x1,x2):
        """ B's utility of consuming x1 of good 1 and x2 of good 2 """

        return self.CES_utility(x1,x2,self.alphaB,self.betaB,self.rhoB)

    def demand_A(self,p1):
        """ A's demand at the price p1, returns (x1,x2) """

        m = p1*self.w1A + self.w2A # the value of what A owns

        return self.CES_demand(p1,m,self.alphaA,self.betaA,self.rhoA)

    def demand_B(self,p1):
        """ B's demand at the price p1, returns (x1,x2) """

        m = p1*(1-self.w1A) + (1-self.w2A) # the value of what B owns

        return self.CES_demand(p1,m,self.alphaB,self.betaB,self.rhoB)

    def excess_demand(self,p1):
        """ how much more of each good is wanted than exists, returns (eps1,eps2) """

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        return x1A+x1B-1.0, x2A+x2B-1.0

    def solve(self,p1):
        """ store the price, the allocation and the utilities in self.sol """

        sol = self.sol
        sol.p1 = p1
        sol.x1A,sol.x2A = self.demand_A(p1)
        sol.x1B,sol.x2B = self.demand_B(p1)
        sol.uA = self.utility_A(sol.x1A,sol.x2A)
        sol.uB = self.utility_B(sol.x1B,sol.x2B)

        return sol

def plot_indifference_A(ax,model,x1A,x2A,**kwargs):
    """ plot A's indifference curve through the point (x1A,x2A) """

    uA = model.utility_A(x1A,x2A)

    x1_grid = np.linspace(0.001,0.999,1000)
    x2_grid = model.CES_indifference(uA,x1_grid,model.alphaA,model.betaA,model.rhoA)

    I = (x2_grid > 0) & (x2_grid < 1) # only what is inside the box
    ax.plot(x1_grid[I],x2_grid[I],**kwargs)

def plot_indifference_B(ax,model,x1B,x2B,**kwargs):
    """ plot B's indifference curve through the point (x1B,x2B), flipped into A's coordinates """

    uB = model.utility_B(x1B,x2B)

    x1B_grid = np.linspace(0.001,0.999,1000)
    x2B_grid = model.CES_indifference(uB,x1B_grid,model.alphaB,model.betaB,model.rhoB)

    x1_grid,x2_grid = 1-x1B_grid,1-x2B_grid # flip into A's coordinates

    I = (x2_grid > 0) & (x2_grid < 1)
    ax.plot(x1_grid[I],x2_grid[I],**kwargs)
