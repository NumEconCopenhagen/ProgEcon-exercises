import numpy as np

def make_P(s, f):
    """Return the 2x2 transition matrix for states 0=E (employed), 1=U (unemployed).

      s : separation probability  P(E -> U)
      f : job-finding probability P(U -> E)
    """

    assert 0.0 <= s <= 1.0 and 0.0 <= f <= 1.0, "Probabilities must be in [0,1]."
    P = np.array([[1.0 - s, s],
                  [f,       1.0 - f]], dtype=float)
    assert np.allclose(P.sum(axis=1), 1.0, atol=1e-12), "Rows must sum to 1."
    return P

def steady_state_unemployment(s, f):
    """Theoretical stationary unemployment share s/(s+f)."""
    return s / (s + f)


def simulate_distribution(P, pi0, T):
    """Deterministically iterate the distribution forward: pi_{t+1} = pi_t @ P.

    No random numbers here - this is the exact law of motion of the
    population shares. Returns an array of shape (T+1, 2).
    """
    
    pi = np.empty((T + 1, 2))
    pi[0] = pi0
    for t in range(T):
        pi[t+1] = pi[t] @ P

    return pi


def run(s=0.02, f=0.30, T=200, pi0=(1.0, 0.0)):
    """Build P, run a deterministic simulation, and compare the unemployment
    share to the theoretical steady state s/(s+f).

    pi0 : initial population shares (pi_E, pi_U) at t=0, i.e. the row vector
    pi_0 in pi_{t+1} = pi_t @ P. Entries must be nonnegative and sum to 1,
    e.g. pi0=(1.0, 0.0) means the whole population starts employed.
    """
    
    P = make_P(s, f)
    pi = simulate_distribution(P, np.array(pi0, dtype=float), T)
    u_path = pi[:, 1]  # unemployment share each period

    print(f"P =\n{P}")
    print(f"First 10 unemployment shares: {np.round(u_path[:10], 4)}")
    print(f"Deterministic steady-state unemployment: {u_path[-1]:.4f}")
    print(f"Theoretical s/(s+f):                     {steady_state_unemployment(s, f):.4f}")
