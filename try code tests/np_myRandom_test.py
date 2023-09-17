import numpy as np

class MyRandom():

    random_state_pool = 0

    def __init__(self):
        self.random_state = MyRandom.random_state_pool
        MyRandom.random_state_pool += 1
        self.rng1 = np.random.RandomState(self.random_state)

    def uniform_closed(self, low: int, high: int, precision):
        """
        Generate random float number from closed interval [a, b]
        """
        rnd = self.rng1.randint(0, (high-low) * (10 ** precision) + 1) / (10 ** precision) + low
        return rnd
    
    def uniform_half_open(self, low, high):
        """
        Generate random float number from half-open interval [a, b)
        """
        return self.rng1.uniform(low=low, high=high)
    
    def randint(self, low, high, size=None):
        """
        Generate random int from half-open interval [a, b)
        """
        return self.rng1.randint(low=low, high=high, size=size)