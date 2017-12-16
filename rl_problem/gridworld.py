import numpy as np
from itertools import product


class GridWorld:

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, size=5):
        self.size = size
        self.action_space = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        self.A = (0, 1)
        self.A_prime = (4, 1)
        self.B = (0, 3)
        self.B_prime = (2, 3)
        self._rewards = self._init_rewards()
        self._transitions = self._init_state_transitions()

    def get_uniform_policy(self):
        policy = np.zeros((4, self.size, self.size))
        policy[:, :, :] = 0.25
        return policy

    def get_expected_rewards(self, policy):
        expected_rewards = policy * self._rewards
        return expected_rewards.sum(axis=0)

    def _init_rewards(self):
        rewards = np.zeros((4, self.size, self.size))
        rewards[[self.UP, self.DOWN], [0, self.size - 1], :] = -1
        rewards[[self.LEFT, self.RIGHT], :, [0, self.size - 1]] = -1
        # Special A location
        rewards[:, self.A[0], self.A[1]] = 10
        # Special B location
        rewards[:, self.B[0], self.B[1]] = 5
        return rewards

    def _init_state_transitions(self):
        state_transitions = np.zeros((4, self.size, self.size, self.size, self.size))
        # Normal cases
        for row in range(self.size):
            for col in range(self.size):
                if row != 0:
                    state_transitions[self.UP, row, col, row-1, col] = 1
                if row != self.size - 1:
                    state_transitions[self.DOWN, row, col, row+1, col] = 1
                if col != 0:
                    state_transitions[self.LEFT, row, col, row, col-1] = 1
                if col != self.size - 1:
                    state_transitions[self.RIGHT, row, col, row, col+1] = 1

        # Handle edges
        for col in range(self.size):
            # Moving up or down in top or botton row leaves you in same state
            state_transitions[[self.UP, self.DOWN], [0, self.size - 1], col, [0, self.size - 1], col] = 1
        for row in range(self.size):
            # Moving left or right in leftmost or rightmost column leaves you in same state
            state_transitions[[self.LEFT, self.RIGHT], row, [0, self.size - 1], row, [0, self.size - 1]] = 1

        # Handle A and B
        state_transitions[:, [self.A[0], self.B[0]], [self.A[1], self.B[1]], :, :] = 0
        state_transitions[:, self.A[0], self.A[1], self.A_prime[0], self.A_prime[1]] = 1
        state_transitions[:, self.B[0], self.B[1], self.B_prime[0], self.B_prime[1]] = 1

        return state_transitions

    def get_value_function(self, policy, gamma=0.9):
        # Solve V = R + gamma*P(s,s')*V
        transition_probabilities = self.get_transition_probabilities(policy)
        expected_rewards = self.get_expected_rewards(policy).reshape(self.size**2)
        right_side_inverse = np.linalg.inv(np.identity(self.size**2) - gamma*transition_probabilities)
        return np.matmul(right_side_inverse, expected_rewards)

    def get_transition_probabilities(self, policy):
        ret = np.zeros((self.size**2, self.size**2))
        for action in self.action_space:
            # p(a|s)
            action_policy = np.tile(policy[action, :, :].reshape(self.size**2), (self.size**2, 1))
            # p(s'|s, a)
            state_transitions = self._transitions[action, :, :, :, :].reshape(self.size**2, self.size**2)
            ret = np.add(ret, np.multiply(action_policy, state_transitions))
        return ret

    def get_optimal_value_function(self, gamma=0.9, convergence=0.01):
        ret = np.zeros(self.size**2)
        copy = np.copy(ret)
        diff = None
        while diff is None or diff > convergence:
            for row, col in product(range(self.size), range(self.size)):
                new_reward = None
                for action in self.action_space:
                    next_state_distribution = self._transitions[action, row, col].reshape(self.size**2)
                    expected_rewards = np.matmul(next_state_distribution, ret)
                    test = self._rewards[action, row, col] + gamma*expected_rewards
                    if new_reward is None or test > new_reward:
                        new_reward = test
                copy[row*self.size + col] = new_reward
            diff = np.sum(np.fabs(np.subtract(ret, copy)))
            ret = copy
            copy = np.copy(ret)
        return ret
