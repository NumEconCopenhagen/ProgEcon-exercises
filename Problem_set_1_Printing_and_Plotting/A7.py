import numpy as np
import matplotlib.pyplot as plt
import A1

def plot(p1,p2,income,alpha,beta,N=100):

    # a. grid of bundles (start slightly above 0 to avoid division by zero in u_func)
    x1_vec = np.linspace(0.01,income/p1,N)
    x2_vec = np.linspace(0.01,income/p2,N)
    x1_grid,x2_grid = np.meshgrid(x1_vec,x2_vec,indexing='ij')

    # b. keep only affordable bundles
    affordable = p1*x1_grid + p2*x2_grid <= income
    x1_aff = x1_grid[affordable]
    x2_aff = x2_grid[affordable]
    u_aff = A1.u_func(x1_aff,x2_aff,alpha=alpha,beta=beta)

    # c. utility-maximizing affordable bundle (more is better -> lies on the budget line)
    j = np.argmax(u_aff)
    x1_star = x1_aff[j]
    x2_star = x2_aff[j]

    # d. plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # i. scatter of affordable bundles colored by utility
    h = ax.scatter(x1_aff,x2_aff,s=10,c=u_aff)
    fig.colorbar(h)

    # ii. budget line
    ax.plot([0,income/p1],[income/p2,0],color='black',lw=2,label='budget line')

    # iii. optimum
    ax.scatter(x1_star,x2_star,color='red',s=80,zorder=5,label='optimum')

    # labels
    ax.set_title('Affordable bundles colored by utility',pad=10)
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.legend(loc='upper right')

    fig.savefig('A7_budget_set.png')

    print(f'optimal bundle: x1 = {x1_star:.3f}, x2 = {x2_star:.3f} -> u = {u_aff[j]:.3f}')
