import numpy as np
import matplotlib.pyplot as plt
import math

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
        """
        :param max_cars: Non-inclusive upper-bound for how many cars can be at a dealership
        """
        self.max_cars = max_cars
        self.action_space = np.arange(-5, 6)
        self.a_transitions = self.init_transition_probabilities('A')
        self.b_transitions = self.init_transition_probabilities('B')
        self.a_expected_revenue = self.init_expected_revenue('A')
        self.b_expected_revenue = self.init_expected_revenue('B')

    def init_expected_revenue(self, dealership):
        """
        Returns a self.max_cars x self.max_cars x len(self.action_space) array.
        Each cell holds the expected revenue for the specified dealership with
        the specified previous state, next state, and action.
        :param dealership: 'A' or 'B'
        """
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
        ret = np.zeros((self.max_cars, self.max_cars))
        for current in range(ret.shape[0]):
            for next in range(ret.shape[1]):
                probability = 0.0
                for requests in range(self.POISSON_CUTOFF):
                    for returns in range(self.POISSON_CUTOFF):
                        cars_after_requests = max(current - requests, 0)
                        cars_after_returns = min(cars_after_requests + returns, self.max_cars - 1)
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
        expected_sales_a = self.a_expected_revenue[action, current[0], next[0]]
        expected_sales_b = self.b_expected_revenue[action, current[1], next[1]]

        return expected_sales_a + expected_sales_b - cost

    def next_state_probability(self, current, next, action):
        immediate_a = current[0] - action
        immediate_b = current[1] + action
        if immediate_a < 0 or immediate_a > (self.max_cars - 1):
            return 0.0
        elif immediate_b < 0 or immediate_b > (self.max_cars - 1):
            return 0.0
        probability_a = self.a_transitions[immediate_a, next[0]]
        probability_b = self.b_transitions[immediate_b, next[1]]
        return probability_a * probability_b

    def expected_return(self, state, action, state_value, gamma):
        (a, b) = state
        next_state_gain_expectation = 0.0
        for a_prime in range(self.max_cars):
            for b_prime in range(self.max_cars):
                probability_next_state = self.next_state_probability((a, b), (a_prime, b_prime), action)
                immediate_reward = self.get_expected_reward(action, (a, b), (a_prime, b_prime))
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
        ret = np.zeros((self.max_cars, self.max_cars))
        diff = np.inf
        while diff > convergence:
            temp = np.copy(ret)
            for a in range(policy.shape[0]):
                for b in range(policy.shape[1]):
                    ret[a, b] = self.expected_return((a, b), policy[a, b], temp, gamma)
            diff = np.max(np.fabs(np.subtract(ret, temp)))
            print(diff)
        return ret

    def print_progress(self, state):
        progress = (state[0] + (state[1] / self.max_cars)) / self.max_cars
        print('%.2f' % (100 * progress))

    def get_greedy_policy(self, value, gamma=0.9):
        """
        Generates a policy that is greedy with respect to the provided value function.

        :param value: A self.max_cars x self.max_cars array
        :return: A self.max_cars x self.max_cars array
        """
        policy = np.zeros((self.max_cars, self.max_cars))
        for a in range(policy.shape[0]):
            for b in range(policy.shape[1]):
                self.print_progress((a, b))
                best_action = [None, -np.inf]
                for action in np.arange(-5, 6):
                    if a - action < 0 or b + action < 0:
                        # This action is not allowed if it makes one dealership have less than 0 cars
                        continue
                    next_state_gain_expectation = self.expected_return((a, b), action, value, gamma)
                    if next_state_gain_expectation > best_action[1]:
                        best_action[0] = action
                policy[a, b] = best_action
        return policy

    def plot_policies(self, policies):
        for i in range(len(policies)):
            policy = policies[i]
            plt.figure(i + 1)
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

    def show_plots(self):
        pass

if __name__ == '__main__':
    MAX_CARS = 21
    cars = JacksCarRental(max_cars=MAX_CARS)
    policies = []
    policies.append(np.zeros((MAX_CARS, MAX_CARS), dtype=int))
    policies.append(np.random.randint(-5, 6, (MAX_CARS, MAX_CARS)))
    policies.append(np.random.randint(-5, 6, (MAX_CARS, MAX_CARS)))
    policies.append(np.random.randint(-5, 6, (MAX_CARS, MAX_CARS)))
    policies.append(np.random.randint(-5, 6, (MAX_CARS, MAX_CARS)))
    cars.plot_policies(policies)

    # value = cars.evaluate_policy(policy)
    # greedy = cars.get_greedy_policy(value)
    # cars.plot_policy(greedy)
    #
    # value1 = cars.evaluate_policy(greedy.astype(int))
    # greedy2 = cars.get_greedy_policy(value1)
    # cars.plot_policy(greedy2)
    #
    # value2 = cars.evaluate_policy(greedy2.astype(int))
    # greedy3 = cars.get_greedy_policy(value2)
    # cars.plot_policy(greedy3)

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
