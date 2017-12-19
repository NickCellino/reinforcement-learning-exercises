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

    def get_expected_reward(self, action, current_state):
        moving_car_cost = abs(action) * 2
        a_cars = min(max(current_state[0] - action, 0), 20)
        expected_rental_sales_a = 10 * min(self.EXPECTED_REQUESTS_A, a_cars)
        b_cars = min(max(current_state[1] + action, 0), 20)
        expected_rental_sales_b = 10 * min(self.EXPECTED_REQUESTS_B, b_cars)
        return expected_rental_sales_a + expected_rental_sales_b - moving_car_cost

    def next_state_probability(self, current, next, action):
        immediate_a = current[0] - action
        immediate_b = current[1] + action
        if immediate_a < 0 or immediate_a > 20:
            return 0.0
        elif immediate_b < 0 or immediate_b > 20:
            return 0.0
        probability_a = self.a_transitions[immediate_a, next[0]]
        probability_b = self.b_transitions[immediate_b, next[1]]
        return probability_a * probability_b

    def evaluate_policy(self, policy, gamma=0.9, convergence=1.0):
        """
        Generates a value function for a given deterministic policy.
        The policy should specify the action [-5, +5] for each
        state, which is the number of cars at location A and the number
        of cars at location B, where each ranges from 0 to 20.

        :param policy: A 21 x 21 array
        :return: A 21 x 21  array
        """
        ret = np.zeros((21, 21))
        diff = np.inf
        while diff > convergence:
            temp = np.copy(ret)
            for a, b in product(range(policy.shape[0]), range(policy.shape[1])):
                action = policy[a, b]
                next_state_gain_expectation = 0.0
                for a_prime, b_prime in product(range(policy.shape[0]), range(policy.shape[1])):
                    probability_next_state = self.next_state_probability((a, b), (a_prime, b_prime), action)
                    immediate_reward = self.get_expected_reward(action, (a, b))
                    next_state_gain_expectation += probability_next_state * (immediate_reward + gamma * temp[a_prime, b_prime])
                ret[a, b] = next_state_gain_expectation
            diff = np.max(np.fabs(np.subtract(ret, temp)))
            print(diff)
        return ret

    def get_greedy_policy(self, value, gamma=0.9):
        """
        Generates a policy that is greedy with respect to the provided value function.

        :param value: A 21 x 21 array
        :return: A 21 x 21 array
        """
        policy = np.zeros((21, 21))
        for a, b in product(range(policy.shape[0]), range(policy.shape[1])):
            best_action = None
            best_action_gain = - np.inf
            print(f'{100*float(a) / policy.shape[0]} %')
            for action in np.arange(-5, 6):
                next_state_gain_expectation = 0.0
                for a_prime, b_prime in product(range(policy.shape[0]), range(policy.shape[1])):
                    probability_next_state = self.next_state_probability((a, b), (a_prime, b_prime), action)
                    immediate_reward = self.get_expected_reward(action, (a, b))
                    next_state_gain_expectation += probability_next_state * (immediate_reward + gamma * value[a_prime, b_prime])
                if next_state_gain_expectation > best_action_gain:
                    best_action = action
                    best_action_gain = next_state_gain_expectation
            policy[a, b] = best_action
        return policy

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
    # random_policy = np.random.randint(-5, 6, (21, 21))
    zero_policy = np.zeros((21, 21), dtype=int)
    value = cars.evaluate_policy(zero_policy, convergence=2.0)
    next_policy = cars.get_greedy_policy(value)
    cars.plot_policy(next_policy)
    # print(value)
    # print(cars.a_transitions)

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
