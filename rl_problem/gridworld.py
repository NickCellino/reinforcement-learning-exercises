import numpy as np


class GridWorld:

    def __init__(self, size=5):
        self._rewards = np.zeros(size**2)

    def get_uniform_policy(self):
        pass
