import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import product


class JacksCarRental:

    EXPECTED_RETURNS_A = 3
    EXPECTED_REQUESTS_A = 3
    EXPECTED_RETURNS_B = 2
    EXPECTED_REQUESTS_B = 4

    def __init__(self, size=21):
        self.size = size
        self.a_transitions = self.init_transition_probabilities('A')
        self.b_transitions = self.init_transition_probabilities('B')

    def init_transition_probabilities(self, dealership):
        ret = np.zeros((21, 21))
        for current, next in product(range(ret.shape[0]), range(ret.shape[1])):
            probability = 0.0
            for requests, returns in product(range(21), range(21)):
                if min(max(current + returns - requests, 0), 20) == next:
                    request_probability = self.expected_requests_probability(dealership, requests)
                    return_probability = self.expected_returns_probability(dealership, returns)
                    probability += request_probability * return_probability
                ret[current, next] = probability
        return ret

    def expected_returns_probability(self, dealership, returns):
        if dealership is 'A':
            return self.poisson(self.EXPECTED_RETURNS_A, returns)
        elif dealership is 'B':
            return self.poisson(self.EXPECTED_RETURNS_B, returns)
        else:
            raise ValueError('Dealership must be A or B')

    def expected_requests_probability(self, dealership, requests):
        if dealership is 'A':
            return self.poisson(self.EXPECTED_REQUESTS_A, requests)
        elif dealership is 'B':
            return self.poisson(self.EXPECTED_REQUESTS_B, requests)
        else:
            raise ValueError('Dealership must be A or B')

    def poisson(self, expected, num):
        if num < 0:
            return 0.0
        ret = ((expected**num)/math.factorial(num))*math.exp(-expected)
        return ret

    def get_next_state(self, state, action):
        a = state[0]
        b = state[1]
        return (a - action, b + action)

    def get_expected_reward(self, state, action):
        # Dealership A
        a = state[0]
        b = state[1]

    def next_state_probability(self, next, state, action):
        after_move = (state[0] - action, state[1] + action)
        required_returns_to_a = next[0] - after_move[0]
        required_returns_to_b = next[1] - after_move[1]
        if required_returns_to_a < 0 or required_returns_to_b < 0:
            return 0.0
        else:
            a_prob = self.poisson(self.EXPECTED_RETURNS_A, required_returns_to_a)
            b_prob = self.poisson(self.EXPECTED_RETURNS_B, required_returns_to_b)
            return a_prob*b_prob

    def evaluate_policy(self, policy, gamma=0.9, convergence=0.01):
        """
        Generates a value function for a given deterministic policy.
        The policy should specify the action [-5, +5] for each
        state, which is the number of cars at location A and the number
        of cars at location B, where each ranges from 0 to 20.

        :param policy: A 21 x 21 x 1 array
        :return: A 21 x 21 x 1 array
        """
        ret = np.zeros((policy.shape[0]))
        diff = np.inf
        while diff > convergence:
            temp = np.copy(ret)
            for a, b in product(range(policy.shape[0]), range(policy.shape[1])):
                action = policy[a, b]
                # next_state = self.get_next_state((a, b), action)
                for a_prime, b_prime in product(range(policy.shape[0], policy.shape[1])):
                    probability_next_state = self.next_state_probability((a_prime, b_prime), (a, b), action)

                ret[a, b] = self.get_expected_reward((a, b), action) + gamma*temp[next_state]
            diff = np.max(np.fabs(np.subtract(ret, temp)))
        return ret

    def plot_policy(self, policy):
        plt.figure()
        plt.imshow(policy, cmap='jet')
        plt.ylabel('# of Cars at Dealership A')
        plt.xlabel('# of Cars at Dealership B')
        plt.xticks(np.arange(0, policy.shape[0], 1))
        plt.yticks(np.arange(0, policy.shape[1], 1))
        plt.gca().invert_yaxis()

        # Annotate states
        for i in range(policy.shape[0]):
            for j in range(policy.shape[1]):
                plt.text(j, i, '%d' % policy[i,j], horizontalalignment='center', verticalalignment='center')

        plt.colorbar()
        plt.show()


if __name__ == '__main__':
    cars = JacksCarRental()
    # print(cars.a_transitions)
    print(np.sum(cars.a_transitions, axis=1))
    print(np.sum(cars.b_transitions, axis=1))

    # print(cars.next_state_probability((5, 5), (6, 6), 0))
    # print(cars.poisson(3, 3))
    # print(cars.poisson(3, 4))
    # policy = np.zeros(21*21)
    # size = 21
    # for i in range(5):
    #     for j in range(5):
    #         policy[i*size + j] = 3
    # for i in range(10, size):
    #     for j in range(5, 10):
    #         policy[i*size + j] = -5
    # for i in range(7, 9):
    #     for j in range(1, 3):
    #         policy[i*size + j] = 5
    # cars.plot_policy(policy)
