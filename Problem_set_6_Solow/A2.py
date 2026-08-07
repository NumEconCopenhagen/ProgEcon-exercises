import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'-'})
plt.rcParams.update({'font.size':14})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

from A1 import k_star

def run(alpha=1/3,s=0.20,delta=0.30,g=0.03,n=0.04,k_max=1.0):
    """ plot the steady-state diagram with and without growth in A and L """

    # a. the two steady states
    k_star_0 = k_star(alpha,s,delta,0.0,0.0) # without growth
    k_star_gn = k_star(alpha,s,delta,g,n) # with growth

    # b. grid and curves
    k_grid = np.linspace(0,k_max,500)

    invest = s*k_grid**alpha # investment, the same in both cases
    break_even_0 = delta*k_grid # break-even without growth
    break_even_gn = ((1+g)*(1+n)-(1-delta))*k_grid # break-even with growth

    # c. figure
    fig = plt.figure(figsize=(9,5.5))
    ax = fig.add_subplot(1,1,1)

    ax.plot(k_grid,invest,lw=2,color=colors[1],label=r'investment, $s f(\tilde{k})$')
    ax.plot(k_grid,break_even_0,lw=2,color=colors[3],label=r'break-even without growth, $\delta \tilde{k}$')
    ax.plot(k_grid,break_even_gn,lw=2,ls='--',color=colors[4],
            label=r'break-even with growth, $[(1+g)(1+n)-(1-\delta)]\tilde{k}$')

    # d. mark the two steady states
    for k_now,color,txt in [(k_star_0,colors[3],'without growth'),(k_star_gn,colors[4],'with growth')]:
        ax.plot(k_now,s*k_now**alpha,'o',ms=8,color=color,zorder=3)
        ax.axvline(k_now,ls=':',lw=1.5,color=color,alpha=0.8,zorder=0,
                   label=fr'$\tilde{{k}}^*={k_now:.2f}$ ({txt})')

    # e. labels
    ax.set_title('The steady state with and without growth')
    ax.set_xlabel(r'capital per effective worker, $\tilde{k}$')
    ax.set_ylabel('per effective worker')
    ax.set_xlim(0,k_max)
    ax.set_ylim(0,1.05*max(invest.max(),break_even_gn.max()))
    ax.legend(loc='upper left',fontsize=11)

    fig.tight_layout()
    plt.show()

    print(f'k* without growth: {k_star_0:.4f}')
    print(f'k* with growth:    {k_star_gn:.4f}')
    print('')
    print('growth in A and L works exactly like a higher depreciation rate:')
    print('the capital stock has to be spread out over more and more effective workers.')
