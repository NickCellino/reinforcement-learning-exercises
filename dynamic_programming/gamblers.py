import math
import matplotlib.pyplot as plt
import numpy as np


class GamblersProblem():

    _plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, win_probability=0.4):
        self._win_probability = win_probability

    def get_possible_next_states(self, state, action):
        ret = []
        # Either we win
        ret.append(state + action)
        # or we lose
        ret.append(state - action)
        return list(set(ret))

    def probability_next_state(self, state, action, next_state):
        # Special "sink" states
        if state == 0:
            if next_state == 0:
                return 1.0
            return 0.0
        if state == 100:
            if next_state == 100:
                return 1.0
            return 0.0

        # Loss
        if next_state == (state - action):
            return 1 - self._win_probability
        # Win
        elif next_state == (state + action):
            return self._win_probability
        else:
            # Should never actually make it here
            return 0.0

    def reward(self, state, action, next_state):
        if next_state == 100:
            return 1.0
        else:
            return 0.0

    def value_iteration(self, convergence=0.0001):
        diff = np.inf
        value = np.zeros(101)
        temp = np.copy(value)
        ret = []
        while diff > convergence:
            for state in range(1, value.shape[0] - 1):
                action_space = np.arange(0, min(state, 100 - state) + 1)
                best_value = None
                for action in action_space:
                    possible_next_states = self.get_possible_next_states(state, action)
                    gain = 0.0
                    for next_state in possible_next_states:
                        gain += self.probability_next_state(state, action, next_state) * (
                            self.reward(state, action, next_state) + temp[next_state]
                        )
                    if best_value is None or gain > best_value:
                        best_value = gain
                value[state] = best_value
            diff = np.max(np.fabs(np.subtract(temp, value)))
            temp = np.copy(value)
            ret.append(temp)
        return ret

    def get_greedy_policy(self, value):
        policy = np.zeros(101)
        for state in np.arange(1, 100):
            action_space = np.arange(0, min(state, 100 - state) + 1)
            best_action = [None, -np.inf]
            for action in action_space:
                possible_next_states = self.get_possible_next_states(state, action)
                gain = 0.0
                for next_state in possible_next_states:
                    gain += self.probability_next_state(state, action, next_state) * (
                        self.reward(state, action, next_state) + value[next_state]
                    )
                if best_action[0] is None:
                    best_action[0] = action
                    best_action[1] = gain
                elif math.isclose(gain, best_action[1]):
                    # Tie breaking strategy
                    # Choose more conservative action
                    if action < best_action[0]:
                        best_action[0] = action
                elif gain > best_action[1]:
                    best_action[0] = action
                    best_action[1] = gain
            policy[state] = best_action[0]
        return policy

    def plot_value_functions(self, value_functions):
        for i in range(len(value_functions)):
            plt.plot(value_functions[i][0:-1], self._plot_colors[i%len(self._plot_colors)], label=f'Value Function {i}')
        plt.title(f"Gambler's Problem Value Iteration (Win Probability = {self._win_probability})")
        plt.xlabel('Capital')
        plt.ylabel('Value')
        plt.legend(loc=4)

    def plot_policy(self, policy):
        plt.plot(np.arange(0, 101), policy)
        plt.title(f'Optimal Policy for Gambler (Win Probability = {self._win_probability})')
        plt.xlabel('Captial')
        plt.ylabel('Stake')

    def plot_results(self, value_functions, policy, figure=1):
        plt.figure(figure)
        self.plot_value_functions(value_functions)
        plt.figure(figure + 1)
        self.plot_policy(policy)
        return figure + 2

if __name__ == '__main__':
    gmb = GamblersProblem()
    values = gmb.value_iteration(convergence=0.001)
    policy = gmb.get_greedy_policy(values[-1])
    gmb.plot_value_functions(values)
    gmb.plot_policy(policy)
