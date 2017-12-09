from numpy.random import normal, randn

class NArmedBandit(object):

    def __init__(self, n):
        self._arms = randn(n)
    
    def pull_arm(self, arm):
        if arm < 0 or arm >= self.num_arms():
            raise ValueError("This arm does not exist.")
        return self._arms[arm] + normal()
    
    def num_arms(self):
        return len(self._arms)


class MovingNArmedBandit(NArmedBandit):

    def __init__(self, n, sigma=0.1):
        super(MovingNArmedBandit, self).__init__(n)
        self._sigma = sigma

    def pull_arm(self, arm):
        value = super(MovingNArmedBandit, self).pull_arm(arm)
        self._arms += self._sigma * randn(len(self._arms))
        return value
