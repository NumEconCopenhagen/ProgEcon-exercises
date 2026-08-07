import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from A3 import SolowModelGrowth

def draw_ar1(rng,T,mean,rho,sigma):
    """ draw an AR(1) path fluctuating around mean

    Args:

        rng (Generator): random number generator
        T (int): number of periods
        mean (float): long-run average
        rho (float): persistence of the shocks
        sigma (float): standard deviation of the shocks

    Returns:

        (ndarray): the path with T elements

    """

    eps = rng.normal(0,sigma,size=T) # all the shocks at once

    x = np.empty(T)
    x[0] = mean # start at the long-run average
    for t in range(1,T):
        x[t] = (1-rho)*mean + rho*x[t-1] + eps[t]

    return x

def draw_paths(rng,T,model,rho=0.90,sigma_s=0.07,sigma_g=0.005,sigma_n=0.005):
    """ draw stochastic paths for the savings rate, technology growth and population growth

    The savings rate is drawn in logs, so that it is always positive.

    Returns:

        (ndarray,ndarray,ndarray): paths for s, g and n

    """

    s = np.exp(draw_ar1(rng,T,np.log(model.s),rho,sigma_s))
    g = draw_ar1(rng,T,model.g,rho,sigma_g)
    n = draw_ar1(rng,T,model.n,rho,sigma_n)

    return s,g,n

def run(N=500,T=100,seed=2026):
    """ simulate N economies with stochastic s, g and n and plot the results

    Args:

        N (int): number of economies
        T (int): number of periods
        seed (int): seed for the random number generator

    """

    # a. the deterministic benchmark, starting in the steady state
    model = SolowModelGrowth(T=T)
    k_ss = model.steady_state()[0]
    model.K0 = k_ss*model.A0*model.L0

    sim_det = model.simulate()
    growth_det = (sim_det.y_pw[-1]/sim_det.y_pw[0])**(1/(T-1))-1

    # b. simulate N economies, each with its own draws
    rng = np.random.default_rng(seed)

    k_all = np.empty((N,T)) # capital per effective worker
    growth_all = np.empty(N) # average growth in output per worker

    for i in range(N):

        s_path,g_path,n_path = draw_paths(rng,T,model)
        sim = model.simulate(s=s_path,g=g_path,n=n_path)

        k_all[i,:] = sim.k # copy the result out before the next call overwrites it
        growth_all[i] = (sim.y_pw[-1]/sim.y_pw[0])**(1/(T-1))-1

    # c. percentiles across economies in each period
    k_median = np.percentile(k_all,50,axis=0)
    k_low = np.percentile(k_all,10,axis=0)
    k_high = np.percentile(k_all,90,axis=0)

    print(f'capital per effective worker in the last period:')
    print(f'  mean = {k_all[:,-1].mean():.4f}, std = {k_all[:,-1].std():.4f} (deterministic: {k_ss:.4f})')
    print('')
    print(f'average growth in output per worker:')
    print(f'  mean = {growth_all.mean():.4f}, std = {growth_all.std():.4f} (deterministic: {growth_det:.4f})')
    print(f'  10th-90th percentile: {np.percentile(growth_all,10):.4f} to {np.percentile(growth_all,90):.4f}')

    # d. figure
    fig = plt.figure(figsize=(13,5))

    # i. capital per effective worker over time
    ax = fig.add_subplot(1,2,1)
    ax.plot(k_all[:20,:].T,lw=0.6,color='black',alpha=0.25) # 20 individual economies
    ax.fill_between(np.arange(T),k_low,k_high,color=colors[0],alpha=0.30,label='10th-90th percentile')
    ax.plot(k_median,lw=2,color=colors[0],label='median')
    ax.axhline(k_ss,ls='--',lw=1.5,color='black',label=r'deterministic $\tilde{k}^*$')

    ax.set_title(f'Capital per effective worker in {N:,} economies')
    ax.set_xlabel('period, $t$')
    ax.set_ylabel(r'$\tilde{k}_t$')
    ax.set_xlim(0,T-1)
    ax.legend(loc='upper right',fontsize=11)

    # ii. the distribution of long-run growth
    ax = fig.add_subplot(1,2,2)
    ax.hist(growth_all,bins=40,density=True,color=colors[1],alpha=0.60)
    ax.axvline(growth_det,ls='--',lw=1.5,color='black',label='deterministic growth')
    ax.axvline(growth_all.mean(),lw=2,color=colors[3],label='mean across economies')

    ax.set_title('Average growth in output per worker')
    ax.set_xlabel('average growth rate over the whole simulation')
    ax.set_ylabel('density')
    ax.legend(loc='upper right',fontsize=11)

    fig.tight_layout()
    plt.show()

    print('')
    print('the shocks average out over time, so the growth rates are much less spread out')
    print('than the shocks themselves - but the level of capital keeps moving around.')
