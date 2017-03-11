from numpy.random import random, random_integers, normal

class Agent:

    def __init__(self, num_arms):
        self._num_arms = num_arms
        self._results = []
        self._value_estimates = []
        for i in range(self._num_arms):
            self._results.append([0.0, 0])
            self._value_estimates.append(normal())
    
class SoftmaxAgent:

    def __init__(self, temperature, num_arms):
        Agent.__init__(self, num_arms)
        self._temperature = temperature
    
    def _choose_arm(self):
        return random_integers(0, num_arms - 1)

class EpsilonGreedyAgent(Agent):

    def __init__(self, epsilon, num_arms):
        Agent.__init__(self, num_arms)
        self._epsilon = epsilon
        self._update_best_arm()
    
    def _update_best_arm(self):
        self._current_best_arm = self._value_estimates.index(max(self._value_estimates))
    
    def _choose_arm(self):
        if random() < self._epsilon:
            # Explore
            return random_integers(0, len(self._results) - 1)
        else:
            # Exploit
            return self._value_estimates.index(max(self._value_estimates))
    
    def _update_estimate(self, reward, arm):
        old_estimate = self._value_estimates[arm]
        self._results[arm][0] += reward
        self._results[arm][1] += 1
        self._value_estimates[arm] = self._results[arm][0] / self._results[arm][1]
        return self._value_estimates[arm] - old_estimate

    def do_pull(self, bandit):
        arm = self._choose_arm()
        reward = bandit.pull_arm(arm)
        self._update_estimate(reward, arm)
        return reward
