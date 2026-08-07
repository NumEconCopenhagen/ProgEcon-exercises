import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from A3 import SolowModelGrowth

def run(T=100,t_switch=30,n_new=0.02):
    """ compare a baseline with a permanent fall in population growth

    Args:

        T (int): number of periods
        t_switch (int): the period where population growth falls
        n_new (float): the new growth rate of the population

    """

    # a. baseline: start in the steady state so all movement comes from the shock
    baseline = SolowModelGrowth(T=T)
    k_ss,y_ss,c_ss = baseline.steady_state()
    baseline.K0 = k_ss*baseline.A0*baseline.L0 # K0 such that the economy starts in the steady state

    sim_base = baseline.simulate()

    # b. scenario: population growth falls permanently in period t_switch
    n_path = np.full(T,baseline.n)
    n_path[t_switch:] = n_new

    scenario = SolowModelGrowth(T=T,K0=baseline.K0)
    sim_new = scenario.simulate(n=n_path)

    # c. the new steady state
    k_ss_new = SolowModelGrowth(n=n_new).steady_state()[0]

    gain = sim_new.y_pw[-1]/sim_base.y_pw[-1]-1

    print(f'population growth: {baseline.n:.3f} -> {n_new:.3f} in period {t_switch}')
    print(f'steady state (per effective worker): k* = {k_ss:.4f} -> {k_ss_new:.4f}')
    print(f'output per worker in the last period is {gain*100:.1f} percent higher than in the baseline')

    # d. growth rates of output per worker
    growth_base = sim_base.y_pw[1:]/sim_base.y_pw[:-1]-1
    growth_new = sim_new.y_pw[1:]/sim_new.y_pw[:-1]-1

    # e. figure
    fig = plt.figure(figsize=(13,5))

    # i. capital per effective worker
    ax = fig.add_subplot(1,2,1)
    ax.plot(sim_base.k,lw=2,color=colors[0],label='baseline')
    ax.plot(sim_new.k,lw=2,color=colors[1],label=f'$n$ falls to {n_new:.2f}')
    ax.axhline(k_ss,ls='--',lw=1.5,color='black',label='old steady state')
    ax.axhline(k_ss_new,ls=':',lw=2,color='black',label='new steady state')
    ax.set_title('Capital per effective worker')
    ax.set_ylabel(r'$\tilde{k}_t$')
    ax.legend(loc='lower right',fontsize=11)

    # ii. growth in output per worker
    ax = fig.add_subplot(1,2,2)
    ax.plot(np.arange(1,T),growth_base,lw=2,color=colors[0],label='baseline')
    ax.plot(np.arange(1,T),growth_new,lw=2,color=colors[1],label=f'$n$ falls to {n_new:.2f}')
    ax.axhline(baseline.g,ls='--',lw=1.5,color='black',label=f'$g={baseline.g:.2f}$')
    ax.set_title('Growth in output per worker')
    ax.set_ylabel('growth rate')
    ax.legend(loc='upper right',fontsize=11)

    for ax in fig.axes:
        ax.axvline(t_switch,lw=6,color='black',alpha=0.15,zorder=0)
        ax.set_xlabel('period, $t$')
        ax.set_xlim(0,T-1)

    fig.suptitle('A permanent fall in population growth')
    fig.tight_layout()
    plt.show()

    print('')
    print('the fall in n gives a temporary boost to growth and a permanently higher')
    print('level of output per worker - but in the long run growth is back at g.')
