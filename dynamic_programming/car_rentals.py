import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import product


class JacksCarRental:

    EXPECTED_RETURNS_A = 3
    EXPECTED_REQUESTS_A = 3
    EXPECTED_RETURNS_B = 2
    EXPECTED_REQUESTS_B = 4
    MOVING_CAR_COST = 2
    RENTAL_SALE_PRICE = 10

    # Don't bother computing poisson for anything above this
    # It will be very close to 0
    POISSON_CUTOFF = 14

    def __init__(self, max_cars=21):
        self.max_cars = max_cars
        self.action_space = np.arange(-5, 6)
        self.a_transitions = self.init_transition_probabilities('A')
        self.b_transitions = self.init_transition_probabilities('B')
        self.a_expected_revenue = self.init_expected_revenue('A')
        self.b_expected_revenue = self.init_expected_revenue('B')
        # self.expected_rewards = self.init_expected_rewards()

    def init_expected_revenue(self, dealership):
        revenue = np.zeros((self.action_space.shape[0], self.max_cars, self.max_cars))
        for cars in range(self.max_cars):
            for cars_after in range(self.max_cars):
                for action in self.action_space:
                    if (dealership is 'A' and cars - action < 0) or (dealership is 'B' and cars + action < 0):
                        continue
                    revenue[action, cars, cars_after] = self.get_expected_revenue(dealership, action, cars, cars_after)
        return revenue

    def get_expected_revenue(self, dealership, action, now, after):
        if dealership is 'A':
            after_move = now - action
        elif dealership is 'B':
            after_move = now + action
        else:
            raise ValueError('Dealership must be A or B')

        expected_revenue = 0.0
        for requests in range(self.POISSON_CUTOFF):
            probability = self.expected_requests_probability(dealership, requests)
            expected_revenue += probability * self.RENTAL_SALE_PRICE * min(after_move, requests)

        return expected_revenue

    def init_transition_probabilities(self, dealership):
        ret = np.zeros((21, 21))
        for current, next in product(range(ret.shape[0]), range(ret.shape[1])):
            probability = 0.0
            for requests, returns in product(range(self.POISSON_CUTOFF), range(self.POISSON_CUTOFF)):
                cars_after_requests = max(current - requests, 0)
                cars_after_returns = min(cars_after_requests + returns, 20)
                if cars_after_returns == next:
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
        ret = ((expected**num)/math.factorial(num))*math.exp(-expected)
        return ret

    def get_expected_reward(self, action, current, next):
        cost = abs(action) * self.MOVING_CAR_COST

        a_cars = current[0] - action
        if a_cars < 0:
            raise ValueError("Action causing negative cars at A")

        # expected_sales_a = 0.0
        # expected_sales_a = self.get_expected_revenue('A', action, current[0], next[0])
        expected_sales_a = self.a_expected_revenue[action, current[0], next[0]]
        # for requests, returns in product(range(self.POISSON_CUTOFF), range(self.POISSON_CUTOFF)):
        #     cars_after_requests = max(a_cars - requests, 0)
        #     reward = self.RENTAL_SALE_PRICE * min(a_cars, requests)
        #     cars_after_returns = min(cars_after_requests + returns, 20)
        #     if cars_after_returns == next[0]:
        #         request_probability = self.expected_requests_probability('A', requests)
        #         return_probability = self.expected_returns_probability('A', returns)
        #         expected_sales_a += request_probability * return_probability * reward

        b_cars = current[1] + action
        if b_cars < 0:
            raise ValueError("Action causing negative cars at B")

        # expected_sales_b = 0.0
        expected_sales_b = self.b_expected_revenue[action, current[1], next[1]]
        # for requests, returns in product(range(self.POISSON_CUTOFF), range(self.POISSON_CUTOFF)):
        #     cars_after_requests = max(b_cars - requests, 0)
        #     reward = self.RENTAL_SALE_PRICE * min(b_cars, requests)
        #     cars_after_returns = min(cars_after_requests + returns, 20)
        #     if cars_after_returns == next[1]:
        #         request_probability = self.expected_requests_probability('B', requests)
        #         return_probability = self.expected_returns_probability('B', returns)
        #         expected_sales_b += request_probability * return_probability * reward

        return expected_sales_a + expected_sales_b - cost

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

    def expected_return(self, state, action, state_value, gamma):
        (a, b) = state
        next_state_gain_expectation = 0.0
        for a_prime, b_prime in product(range(policy.shape[0]), range(policy.shape[1])):
            probability_next_state = self.next_state_probability((a, b), (a_prime, b_prime), action)
            immediate_reward = self.get_expected_reward(action, (a, b), (a_prime, b_prime))
            # immediate_reward = self.expected_rewards[action, a, b, a_prime, b_prime]
            next_state_gain_expectation += probability_next_state * (immediate_reward + gamma * state_value[a_prime, b_prime])
        return next_state_gain_expectation

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
                ret[a, b] = self.expected_return((a, b), policy[a, b], temp, gamma)
            diff = np.max(np.fabs(np.subtract(ret, temp)))
            print(diff)
        return ret

    def print_progress(self, state):
        progress = (state[0] + (state[1] / 21.0)) / 21
        print(f'{100 * progress}%')

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
            self.print_progress((a, b))
            for action in np.arange(-5, 6):
                if a - action < 0 or b + action < 0:
                    # This action is not allowed if it makes one dealership have less than 0 cars
                    continue
                next_state_gain_expectation = self.expected_return((a, b), action, value, gamma)
                if next_state_gain_expectation > best_action_gain:
                    best_action = action
                    best_action_gain = next_state_gain_expectation
            policy[a, b] = best_action
        return policy

    def plot_policy(self, policy):
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
    policy = np.zeros((21, 21), dtype=int)
    value = cars.evaluate_policy(policy)
    greedy = cars.get_greedy_policy(value)
    cars.plot_policy(greedy)

    value1 = cars.evaluate_policy(greedy.astype(int))
    greedy2 = cars.get_greedy_policy(value1)
    cars.plot_policy(greedy2)

    # temp = None
    # figure_counter = 1
    # while temp is None or not np.array_equal(policy, temp):
    #     plt.figure(figure_counter)
    #     cars.plot_policy(policy)
    #     figure_counter += 1
    #
    #     temp = np.copy(policy)
    #     value = cars.evaluate_policy(policy.astype(int), convergence=2.0)
    #     policy = cars.get_greedy_policy(value)
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
