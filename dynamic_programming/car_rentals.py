import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from tqdm import tqdm

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

    def get_action_cost(self, current, action):
        return abs(action) * self.MOVING_CAR_COST

    def get_expected_reward(self, action, current, next):
        cost = self.get_action_cost(current, action)

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

        :param policy: A self.max_cars x self.max_cars array
        :return: A self.max_cars x self.max_cars  array
        """
        ret = np.zeros((self.max_cars, self.max_cars))
        diff = np.inf
        print(f'Evaluating policy until diff < {convergence}')
        while diff > convergence:
            temp = np.copy(ret)
            for a in range(policy.shape[0]):
                for b in range(policy.shape[1]):
                    ret[a, b] = self.expected_return((a, b), policy[a, b], temp, gamma)
            diff = np.max(np.fabs(np.subtract(ret, temp)))
            print(f'Diff: {diff}')
        return ret

    def get_greedy_policy(self, value, gamma=0.9):
        """
        Generates a policy that is greedy with respect to the provided value function.

        :param value: A self.max_cars x self.max_cars array
        :return: A self.max_cars x self.max_cars array
        """
        policy = np.zeros((self.max_cars, self.max_cars))
        print('Improving Policy...')
        for a in tqdm(range(policy.shape[0])):
            for b in range(policy.shape[1]):
                best_action = [None, -np.inf]
                for action in np.arange(-5, 6):
                    if a - action < 0 or b + action < 0:
                        # This action is not allowed if it makes one dealership have less than 0 cars
                        continue
                    next_state_gain_expectation = self.expected_return((a, b), action, value, gamma)
                    if next_state_gain_expectation > best_action[1]:
                        best_action[0] = action
                        best_action[1] = next_state_gain_expectation
                policy[a, b] = best_action[0]
        return policy.astype(int)

    def run_policy_improvement(self, gamma=0.9, convergence=5.0):
        initial_policy = np.zeros((self.max_cars, self.max_cars), dtype=int)
        policies = [initial_policy]
        value = None
        while len(policies) < 2 or not np.array_equal(policies[-1], policies[-2]):
            value = self.evaluate_policy(policies[-1], gamma, convergence)
            greedy = self.get_greedy_policy(value)
            policies.append(greedy)
        return policies, value

    def plot_results(self, policies, value_function):
        self.plot_value_function(value_function, figure=1)
        self.plot_policies(policies, starting_fig=2)
        plt.show()

    def plot_value_function(self, value_function, figure=1):
        fig = plt.figure(figure)
        ax = fig.add_subplot(111, projection='3d')
        x = np.arange(0, self.max_cars)
        y = np.arange(0, self.max_cars)
        X, Y = np.meshgrid(x, y)
        ax.plot_wireframe(X, Y, value_function)
        fig.suptitle('Optimal Value Function')
        plt.xlabel('# of Cars at Dealership B')
        plt.ylabel('# of Cars at Dealership A')

    def plot_policies(self, policies, starting_fig=1):
        figure = starting_fig
        for i in range(len(policies)):
            fig = plt.figure(figure)
            figure += 1
            policy = policies[i]
            plt.imshow(policy, cmap='jet')
            plt.ylabel('# of Cars at Dealership A')
            plt.xlabel('# of Cars at Dealership B')
            plt.xticks(np.arange(0, policy.shape[0], 1))
            plt.yticks(np.arange(0, policy.shape[1], 1))
            plt.gca().invert_yaxis()
            if i == (len(policies) - 1):
                fig.suptitle('Optimal Policy')
            else:
                fig.suptitle(f'Policy {i}')

            # Annotate states
            for i in range(policy.shape[0]):
                for j in range(policy.shape[1]):
                    plt.text(j, i, '%d' % policy[i,j], horizontalalignment='center', verticalalignment='center')

            plt.colorbar()

class JacksCarRentalWithHelp(JacksCarRental):

    SECOND_PARKING_LOT_COST = 4

    def get_action_cost(self, current, action):
        if action > 0:
            moving_cost = self.MOVING_CAR_COST * (action - 1)
        else:
            moving_cost = self.MOVING_CAR_COST * abs(action)

        overnight_cars_a = current[0] - action
        overnight_cars_b = current[1] + action

        parking_cost = 0
        if overnight_cars_a > 10:
            parking_cost += self.SECOND_PARKING_LOT_COST
        if overnight_cars_b > 10:
            parking_cost += self.SECOND_PARKING_LOT_COST

        return moving_cost + parking_cost
