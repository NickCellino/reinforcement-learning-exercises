from numpy.random import normal, randn
import numpy as np

class NArmedBandit(object):

    def __init__(self, n):
        self._arms = randn(n)
    
    def pull_arm(self, arm):
        self.validate_arm(arm)
        return self._arms[arm] + normal()
    
    def num_arms(self):
        return len(self._arms)

    def validate_arm(self, arm):
        if arm < 0 or arm >= self.num_arms():
            raise ValueError("This arm does not exist.")

    def was_optimal_choice(self, arm):
        """
        Tells if the choice was optimal.

        Should be used for analysis purposes only
        (in other words, not for actually solving the problem)
        """
        self.validate_arm(arm)
        return np.argmax(self._arms) == arm


class MovingNArmedBandit(NArmedBandit):

    def __init__(self, n, sigma=0.1):
        super(MovingNArmedBandit, self).__init__(n)
        self._sigma = sigma

    def pull_arm(self, arm):
        value = super(MovingNArmedBandit, self).pull_arm(arm)
        self._arms += self._sigma * randn(len(self._arms))
        return value
