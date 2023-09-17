import numpy as np

# seed is not changing anything in this example
# np.random.seed(1011)

# by default it uses Mersenne Twister (MT19937)
# generator period = 2^19937 = 4,3E6001
rng1 = np.random.RandomState(0)
rng2 = np.random.RandomState(1)

print(rng1)
print(rng1.randint(0, 100, 1))  # [44]
print(rng1.randint(0, 100, 1))  # [47]
print(rng2)
print(rng2.randint(0, 100, 1))  # [37]
print(rng2.randint(0, 100, 1))  # [12]