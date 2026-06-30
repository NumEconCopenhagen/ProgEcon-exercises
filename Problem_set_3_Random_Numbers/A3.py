import numpy as np

def simulate_worker_shocks(T, s, f, s0=0, seed=42):
    """Single worker hit by random shocks each period (0=E, 1=U).

    - In E: separate to U with probability s
    - In U: find a job to E with probability f

    Returns the state path (length T+1) and the uniform draws used.
    """

    rng = np.random.default_rng(seed)
    states = np.empty(T + 1, dtype=np.int8)
    states[0] = s0
    uniforms = rng.random(T)  # one draw per period: u_t ~ U[0,1]

    for t in range(T):
        epsilon = uniforms[t]
        if states[t] == 0:                 # E today
            states[t+1] = 1 if (epsilon < s) else 0
        else:                              # U today
            states[t+1] = 0 if (epsilon < f) else 1

    return states, uniforms

def run(T=1_000, s=0.02, f=0.30, s0=0, seed=7):
    """Simulate one worker and report the share of time spent unemployed."""

    path, draws = simulate_worker_shocks(T, s, f, s0, seed)

    print(f"First 10 shocks (uniforms): {np.round(draws[:10], 3)}")
    print(f"First 10 states (0=E,1=U):  {path[:11].tolist()}")
    print(f"Share of time in U (single worker): {path.mean():.4f}")
