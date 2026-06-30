import numpy as np
import matplotlib.pyplot as plt

def portfolio_std(rng, eta, mu, sigma, n_worlds, w=0.5):
    """Monte Carlo mean and std of an equal-weighted 2-stock portfolio with correlation eta."""

    # a. two independent standard normals per world
    z1 = rng.normal(size=n_worlds)
    z2 = rng.normal(size=n_worlds)

    # b. build correlated returns from the independent draws
    rA = mu + sigma*z1
    rB = mu + sigma*(eta*z1 + np.sqrt(1-eta**2)*z2)

    # c. portfolio return in each world (vectorized over worlds)
    rP = w*rA + (1-w)*rB
    return rP.mean(), rP.std()

def run(mu=0.08, sigma=0.20, n_worlds=100_000, w=0.5, seed=2026):
    """Show the value of diversification: a few representative correlations,
    then sweep eta and compare the Monte Carlo volatility with the single-stock level."""

    rng = np.random.default_rng(seed)

    # a. a few representative correlations
    print(f"single stock: mean={mu:.4f}, std={sigma:.4f}")
    for eta in [-0.5, 0.0, 0.5, 1.0]:
        m, sd = portfolio_std(rng, eta, mu, sigma, n_worlds, w)
        print(f"eta={eta:+.1f}: portfolio mean={m:.4f}, std={sd:.4f}")

    # b. sweep correlation and compare with the analytical formula
    rhos = np.linspace(-1.0, 1.0, 21)
    sim_std = np.array([portfolio_std(rng, eta, mu, sigma, n_worlds, w)[1] for eta in rhos])

    # c. plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(rhos, sim_std, 'o', alpha=0.7, label='Monte Carlo')
    ax.axhline(sigma, ls='--', color='black', label='single-stock std')
    ax.set_xlabel(r'correlation $\eta$')
    ax.set_ylabel('portfolio volatility (std)')
    ax.set_title('Diversification: portfolio risk vs. correlation')
    ax.legend()
    plt.show()
