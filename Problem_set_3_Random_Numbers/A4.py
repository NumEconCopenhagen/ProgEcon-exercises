import numpy as np
import matplotlib.pyplot as plt

def simulate_many_workers_shocks(T, N, s, f, s0=0, seed=42):
    """Simulate N workers in parallel (one uniform draw per worker per period).

    States: 0=E, 1=U. Returns the (T+1, N) state array, the draws, and the
    unemployment rate (cross-sectional mean) in each period.
    """

    rng = np.random.default_rng(seed)
    states = np.full((T + 1, N), s0, dtype=np.int8)
    U = rng.random((T, N))  # one draw per worker per period

    for t in range(T):
        in_E = (states[t] == 0)
        in_U = ~in_E

        # start from "stay", then apply the shocks
        states[t+1] = states[t]
        states[t+1, in_E] = np.where(U[t, in_E] < s, 1, 0)   # E -> U with prob s
        states[t+1, in_U] = np.where(U[t, in_U] < f, 0, 1)   # U -> E with prob f

    u_rate = states.mean(axis=1)  # share unemployed each period
    return states, U, u_rate

def plot_unemployment_rate(u_rate, s, f, burn_in=0):
    """Plot the cross-sectional unemployment rate over time.

    All workers start in the same state s0, so the early periods are not
    representative of the long-run behaviour: this initial transient is
    called the "burn-in" period and is shaded in the plot. It is typically
    discarded before computing time averages used to estimate steady state.
    """
    
    t = np.arange(u_rate.size)
    pi_star = s / (s + f)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, u_rate, label="cross-sectional unemployment rate")
    ax.axhline(pi_star, ls="--", color="black", label=r"theoretical $s/(s+f)$")
    if burn_in > 0:
        ax.axvspan(0, burn_in, color="grey", alpha=0.2, label="burn-in")
    ax.set_xlabel("period t")
    ax.set_ylabel("unemployment rate")
    ax.set_title("Many workers: unemployment rate over time")
    ax.legend()
    plt.show()

def run(T=10_000, N=20_000, s=0.02, f=0.30, s0=0, seed=7, burn_in=1000):
    """Simulate many workers, report and plot the unemployment rate over time.

    burn_in is the number of initial periods (all workers start in s0) that
    are excluded from the post-burn-in average reported below.
    """

    states, U, u_rate = simulate_many_workers_shocks(T, N, s, f, s0, seed)

    print(f"First 10 unemployment rates: {np.round(u_rate[:10], 4)}")
    print(f"Last 10 unemployment rates:  {np.round(u_rate[-10:], 4)}")
    print(f"Average unemployment rate after burn-in (t>{burn_in}): {u_rate[burn_in:].mean():.4f}")
    print(f"Theoretical s/(s+f):         {s/(s+f):.4f}")

    plot_unemployment_rate(u_rate, s, f, burn_in=burn_in)
