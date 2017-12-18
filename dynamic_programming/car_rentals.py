import numpy as np
import matplotlib.pyplot as plt
import math


class JacksCarRental:

    def poisson(self, expected, num):
        return ((expected**num)/math.factorial(num))*math.exp(-expected)

    def get_next_state(self, state, action):
        pass

    def get_expected_reward(self, state):
        # Dealership A
        for request

    def evaluate_policy(self, policy, gamma=0.9, convergence=0.01):
        """
        Generates a value function for a given deterministic policy.
        The policy should specify the action [-5, +5] for each
        state, which is the number of cars at location A and the number
        of cars at location B, where each ranges from 0 to 20.

        :param policy: A 21 x 21 array
        :return: A 441 x 1 array
        """
        ret = np.zeros((policy.shape[0]))
        diff = np.inf
        while diff > convergence:
            temp = np.copy(ret)
            for i in range(len(policy)):
                action = policy[i]
                next_state = self.get_next_state(i, action)
                ret[state] = self.get_expected_reward(next_state) + gamma*temp[next_state]
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
    print(cars.poisson(3, 3))
    print(cars.poisson(3, 4))
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
