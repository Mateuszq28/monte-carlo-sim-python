import numpy as np

class MyRandom():

    # random seed to be set in next instance of MyRandom class
    random_state_pool = 0
    # how many random numbers has been already generated
    generated_num = 0

    def __init__(self):
        self.random_state = MyRandom.random_state_pool
        MyRandom.random_state_pool += 1
        self.rng1 = np.random.default_rng(seed=self.random_state)

    def uniform_closed(self, low: int, high: int, precision):
        """
        Generate random float number from closed interval [a, b]
        """
        rnd = self.rng1.integers(0, (high-low) * (10 ** precision) + 1) / (10 ** precision) + low
        MyRandom.generated_num += 1
        return rnd
    
    def uniform_half_open(self, low, high):
        """
        Generate random float number from half-open interval [a, b)
        """
        MyRandom.generated_num += 1
        return self.rng1.uniform(low=low, high=high)
    
    def randint(self, low, high, size=None):
        """
        Generate random int from half-open interval [a, b)
        """
        MyRandom.generated_num += 1
        return self.rng1.integers(low=low, high=high, size=size)