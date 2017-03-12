from numpy.random import random, random_integers, normal
import numpy as np

class Agent:

    def __init__(self, num_arms):
        self._num_arms = num_arms
        self._results = np.zeros((self._num_arms, 2))
        self._value_estimates = normal(size=(self._num_arms))
    
    def reset(self):
        self._value_estimates = normal(size=(self._num_arms))
        self._results = np.zeros((self._num_arms, 2))
            
    def _update_value_estimate(self, reward, arm):
        old_estimate = self._value_estimates[arm]
        self._results[arm, 0] += reward
        self._results[arm, 1] += 1
        self._value_estimates[arm] = self._results[arm, 0] / self._results[arm, 1]
            
    def do_pull(self, bandit):
        arm = self._choose_arm()
        reward = bandit.pull_arm(arm)
        self._update_value_estimate(reward, arm)
        return reward

class SoftmaxAgent(Agent):

    def __init__(self, temperature, num_arms):
        Agent.__init__(self, num_arms)
        self._temperature = temperature
    
    def _gibbs_distribution(self):
        dist = np.exp(self._value_estimates/self._temperature)
        dist = dist / np.sum(dist)
        return dist
    
    def _cumulative_sum(self, arr):
        total = 0
        ret = np.zeros(len(arr))
        for i in range(len(arr)):
            ret[i] = total + arr[i]
            total += arr[i]
        return ret
    
    def _get_sample(self, dist):
        cumulative_dist = self._cumulative_sum(dist)
        r = random()
        for i in range(len(cumulative_dist)):
            if r < cumulative_dist[i]:
                return i

    def _choose_arm(self):
        dist = self._gibbs_distribution()
        return self._get_sample(dist)
        
class EpsilonGreedyAgent(Agent):

    def __init__(self, epsilon, num_arms):
        Agent.__init__(self, num_arms)
        self._epsilon = epsilon
    
    def _choose_arm(self):
        if random() < self._epsilon:
            return random_integers(0, len(self._results) - 1)
        else:
            return np.argmax(self._value_estimates)
