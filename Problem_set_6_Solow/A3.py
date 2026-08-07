from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from solow import SolowModel # the model from the lecture, used for testing

class SolowModelGrowth:
    """ the Solow model with technology growth and population growth """

    def __init__(self,**kwargs):
        """ set the default parameters, then overwrite with any keyword arguments """

        # a. parameters
        self.alpha = 1/3 # capital share in production
        self.s = 0.20 # savings rate
        self.delta = 0.30 # depreciation rate
        self.g = 0.03 # growth rate of technology
        self.n = 0.04 # growth rate of the population

        # b. simulation settings
        self.K0 = 0.05 # initial capital
        self.A0 = 1.00 # initial technology
        self.L0 = 1.00 # initial population
        self.T = 100 # number of periods

        # c. overwrite with keyword arguments, e.g. SolowModelGrowth(n=0.02)
        for key,value in kwargs.items():
            setattr(self,key,value) # same as self.key = value

        # d. empty container for simulation results
        self.sim = SimpleNamespace()

    def __str__(self):
        """ called when using print """

        text = 'Solow model with growth:\n'
        text += f'  alpha = {self.alpha:.2f} (capital share)\n'
        text += f'  s     = {self.s:.2f} (savings rate)\n'
        text += f'  delta = {self.delta:.2f} (depreciation rate)\n'
        text += f'  g     = {self.g:.2f} (growth rate of technology)\n'
        text += f'  n     = {self.n:.2f} (growth rate of the population)\n'
        text += f'  T     = {self.T} (number of periods)'

        return text

    def f(self,k):
        """ output per effective worker, y = f(k) = k**alpha """

        return k**self.alpha

    def steady_state(self):
        """ analytical steady state per effective worker, returns (k,y,c) """

        break_even = (1+self.g)*(1+self.n)-(1-self.delta)

        k = (self.s/break_even)**(1/(1-self.alpha))
        y = self.f(k)
        c = (1-self.s)*y

        return k,y,c

    def as_path(self,x,T):
        """ turn a number or an array into an array with T elements """

        path = np.full(T,x) if np.ndim(x) == 0 else np.asarray(x,dtype=float)
        assert path.size == T, f'the path must have {T} elements, but has {path.size}'

        return path

    def simulate(self,s=None,g=None,n=None):
        """ simulate the model forward in time

        Args:

            s (float or ndarray,optional): savings rate, self.s is used if None
            g (float or ndarray,optional): growth rate of technology, self.g is used if None
            n (float or ndarray,optional): growth rate of the population, self.n is used if None

        Returns:

            (SimpleNamespace): the simulated paths, also stored in self.sim

        """

        T = self.T

        # a. the parameters in each period (a number or one value per period)
        s_vec = self.as_path(self.s if s is None else s,T)
        g_vec = self.as_path(self.g if g is None else g,T)
        n_vec = self.as_path(self.n if n is None else n,T)

        # b. allocate memory for the levels
        K = np.empty(T) # capital
        A = np.empty(T) # technology
        L = np.empty(T) # population
        Y = np.empty(T) # output
        C = np.empty(T) # consumption

        # c. loop forward in time
        K[0],A[0],L[0] = self.K0,self.A0,self.L0
        for t in range(T):

            Y[t] = K[t]**self.alpha*(A[t]*L[t])**(1-self.alpha) # production
            C[t] = (1-s_vec[t])*Y[t] # consumption

            if t < T-1:
                K[t+1] = s_vec[t]*Y[t] + (1-self.delta)*K[t] # capital accumulation
                A[t+1] = (1+g_vec[t])*A[t] # technology grows
                L[t+1] = (1+n_vec[t])*L[t] # the population grows

        # d. store the levels
        self.sim.K = K
        self.sim.A = A
        self.sim.L = L
        self.sim.Y = Y
        self.sim.C = C

        # e. store per effective worker (divide by A*L)
        self.sim.k = K/(A*L)
        self.sim.y = Y/(A*L)
        self.sim.c = C/(A*L)

        # f. store per worker (divide by L)
        self.sim.k_pw = K/L
        self.sim.y_pw = Y/L
        self.sim.c_pw = C/L

        # g. store the realized parameter paths
        self.sim.s = s_vec
        self.sim.g = g_vec
        self.sim.n = n_vec

        return self.sim

def test():
    """ test the simulator on cases where we know the answer """

    # test 1: an economy that starts in the steady state stays there
    model = SolowModelGrowth(T=20)
    k_ss = model.steady_state()[0]
    model.K0 = k_ss*model.A0*model.L0 # start in the steady state

    sim = model.simulate()
    assert np.allclose(sim.k,k_ss), 'the economy does not stay in the steady state'

    # test 2: without growth the model must be exactly the model from the lecture
    model_no_growth = SolowModelGrowth(T=20,g=0.0,n=0.0,K0=0.05,A0=1.0,L0=1.0)
    sim_no_growth = model_no_growth.simulate()

    model_lecture = SolowModel(alpha=model_no_growth.alpha,s=model_no_growth.s,
                               delta=model_no_growth.delta,k0=0.05,T=20)
    sim_lecture = model_lecture.simulate()

    assert np.allclose(sim_no_growth.k,sim_lecture.k), 'g=n=0 does not give the model from the lecture'

    # test 3: the accounting adds up, Y = C + investment
    assert np.allclose(sim.Y,sim.C+sim.s*sim.Y), 'output is not consumption plus investment'

    # test 4: the population grows exactly at the rate n
    assert np.allclose(sim.L[1:]/sim.L[:-1]-1,model.n), 'the population does not grow at the rate n'

    print('all tests passed')

def run():
    """ test the model, then simulate it and plot the convergence and the growth rate """

    # a. test first, then simulate
    test()
    print('')

    model = SolowModelGrowth(T=60)
    sim = model.simulate()

    k_ss,y_ss,c_ss = model.steady_state()

    print(model)
    print('')
    print(f'steady state (per effective worker): k* = {k_ss:.4f}, y* = {y_ss:.4f}')
    print(f'last period of the simulation:       k  = {sim.k[-1]:.4f}, y  = {sim.y[-1]:.4f}')

    # b. growth rate of output per worker
    growth = sim.y_pw[1:]/sim.y_pw[:-1]-1

    print('')
    print(f'growth in output per worker: first period = {growth[0]:.4f}, last period = {growth[-1]:.4f}')
    print(f'the growth rate of technology is g = {model.g:.4f}')

    # c. figure
    fig = plt.figure(figsize=(13,5))

    # i. capital per effective worker
    ax = fig.add_subplot(1,2,1)
    ax.plot(sim.k,lw=2,color=colors[0],label=r'$\tilde{k}_t$')
    ax.axhline(k_ss,ls='--',lw=1.5,color='black',label=r'steady state, $\tilde{k}^*$')
    ax.set_title('Capital per effective worker')
    ax.set_ylabel(r'$\tilde{k}_t$')
    ax.legend(loc='lower right',fontsize=12)

    # ii. growth in output per worker
    ax = fig.add_subplot(1,2,2)
    ax.plot(np.arange(1,model.T),growth,lw=2,color=colors[1],label='growth in $Y_t/L_t$')
    ax.axhline(model.g,ls='--',lw=1.5,color='black',label=f'$g={model.g:.2f}$')
    ax.set_title('Growth in output per worker')
    ax.set_ylabel('growth rate')
    ax.legend(loc='upper right',fontsize=12)

    for ax in fig.axes:
        ax.set_xlabel('period, $t$')
        ax.set_xlim(0,model.T-1)

    fig.tight_layout()
    plt.show()

    print('')
    print('in the steady state output per worker grows at the rate of technology, g:')
    print('only technology makes us richer in the long run.')
