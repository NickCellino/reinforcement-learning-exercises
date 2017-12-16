import numpy as np
from itertools import product


class GridWorld:

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, size=5):
        self._size = size
        self._rewards = np.zeros((4, size, size))
        self._rewards[[self.UP, self.DOWN], [0, self._size-1], :] = -1
        self._rewards[[self.LEFT, self.RIGHT], :, [0, self._size-1]] = -1
        # Special A location
        self._rewards[:, 0, 1] = 10
        # Special B location
        self._rewards[:, 0, 3] = 5

    def get_uniform_policy(self):
        policy = np.zeros((4, self._size, self._size))
        policy[:, :, :] = 0.25
        return policy

    def get_expected_rewards(self, policy):
        expected_rewards = policy * self._rewards
        return expected_rewards.sum(axis=0)

    def get_transition_probabilities(self):
        transition_probabilities = np.zeros((4, self._size, self._size, self._size, self._size))
        # Normal cases
        for row, col in product(range(self._size), range(self._size)):
            transition_probabilities[
                [self.UP, self.DOWN, self.LEFT, self.RIGHT],
                row, col,
                [row-1]
            ] = 1
        # Handle edges
        for col in range(self._size):
            # Moving up or down in top or botton row leaves you in same state
            transition_probabilities[[self.UP, self.DOWN], [0, self._size-1], col, [0, self._size-1], col] = 1
        for row in range(self._size):
            # Moving left or right in leftmost or rightmost column leaves you in same state
            transition_probabilities[[self.LEFT, self.RIGHT], row, [0, self._size-1], row, [0, self._size-1]] = 1
        return transition_probabilities

    # def get_value_function(self, policy):
        # transition_probabilities = self.get_transition_probabilities(policy)
        # pass


if __name__ == '__main__':
    g = GridWorld()
    policy = g.get_uniform_policy()
    expected_rewards = g.get_expected_rewards(policy)
    # print(expected_rewards)
    probs = g.get_transition_probabilities()
    print(probs[g.LEFT, :, 0, :, :])
