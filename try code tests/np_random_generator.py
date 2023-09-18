import numpy as np


# by default it uses Permuted Congruential Generator (64-bit, PCG64)
# generator period = 2^128 = 3,4E38
rng1 = np.random.default_rng(seed=0)
rng2 = np.random.default_rng(seed=1)

print(rng1)
print(rng1.integers(0, 100, 1))  # [8]
print(rng1.integers(0, 100, 1))  # [8]
print(rng2)
print(rng2.integers(0, 100, 1))  # [8]
print(rng2.integers(0, 100, 1))  # [8]