from numpy.random import normal

class NArmedBandit:

    def __init__(self, n):
        self._arms = []
        for i in range(n):
            self._arms.append(normal())
    
    def pull_arm(self, arm):
        if arm < 0 or arm >= self.num_arms():
            raise ValueError("This arm does not exist.")
        return self._arms[arm] + normal()
    
    def num_arms(self):
        return len(self._arms)