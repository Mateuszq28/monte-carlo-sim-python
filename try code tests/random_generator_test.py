import numpy as np

# np.random.seed(1011)

rng1 = np.random.RandomState(0)
rng2 = np.random.RandomState(1)

print(rng1.randint(0, 100, 1))  # [8]
print(rng1.randint(0, 100, 1))  # [8]
print(rng2.randint(0, 100, 1))  # [8]