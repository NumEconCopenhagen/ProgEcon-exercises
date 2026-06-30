import numpy as np

def rng_warmup(seed=2025, n=5):
    """Reproducible draws: seed vs. stream.

    Prints a small report:
      - u1,z1 : first uniforms/normals from a fresh generator
      - u2,z2 : same draws reproduced from a new generator with the same seed
      - u_next,z_next : calling the first generator again advances the stream
    """

    # a. fresh generator
    rng = np.random.default_rng(seed)
    u1 = rng.random(n)
    z1 = rng.standard_normal(n)

    # b. same seed -> identical sequence
    rng_same = np.random.default_rng(seed)
    u2 = rng_same.random(n)
    z2 = rng_same.standard_normal(n)

    # c. calling the first generator again continues (advances) the stream
    u_next = rng.random(n)
    z_next = rng.standard_normal(n)

    # d. report
    print(f"u1:            {u1}")
    print(f"u2 (match u1): {u2}")
    print(f"z1:            {z1}")
    print(f"z2 (match z1): {z2}")
    print()
    print(f"u_next (different): {u_next}")
    print(f"z_next (different): {z_next}")

    assert np.allclose(u1, u2) and np.allclose(z1, z2)
    assert not np.allclose(u1, u_next) and not np.allclose(z1, z_next)
