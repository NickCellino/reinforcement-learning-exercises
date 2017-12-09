# -*- coding: utf-8 -*-

from numpy.random import random, random_integers, normal
import numpy as np

class Agent:

    def __init__(self, num_arms):
        self._num_arms = num_arms
        self._results = np.zeros((self._num_arms, 2))
        self._value_estimates = normal(0, 0.01, size=(self._num_arms))
    
    def reset(self):
        self._value_estimates = normal(size=(self._num_arms))
        self._results = np.zeros((self._num_arms, 2))
            
    def _update_value_estimate(self, reward, arm):
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
        return dist / np.sum(dist)
    
    def _get_sample(self, dist):
        cumulative_dist = np.cumsum(dist)
        r = random()
        for i in range(len(cumulative_dist)):
            if r < cumulative_dist[i]:
                return i
    
    def _choose_arm(self):
        dist = self._gibbs_distribution()
        return self._get_sample(dist)

    def __str__(self):
        return f'Softmax Agent (t={self._temperature})'

        
class EpsilonGreedyAgent(Agent):

    def __init__(self, epsilon, num_arms):
        Agent.__init__(self, num_arms)
        self._starting_epsilon = epsilon
        self._epsilon = epsilon
    
    def reset(self):
        self._epsilon = self._starting_epsilon
        Agent.reset(self)
    
    def _choose_arm(self):
        if random() < self._epsilon:
            return random_integers(0, len(self._results) - 1)
        else:
            return np.argmax(self._value_estimates)

    def __str__(self):
        return f'Epsilon Greedy Agent (ε={self._epsilon})'


class FixedAlphaEpsilonGreedyAgent(EpsilonGreedyAgent):

    def __init__(self, epsilon, num_arms, alpha=0.1):
        EpsilonGreedyAgent.__init__(self, epsilon, num_arms)
        self._alpha = alpha

    def _update_value_estimate(self, reward, arm):
        self._value_estimates[arm] += self._alpha * (reward - self._value_estimates[arm])

    def __str__(self):
        return f'Fixed Alpha Epsilon Greedy Agent (ε={self._epsilon}, α={self._alpha})'


class VariableEpsilonGreedyAgent(EpsilonGreedyAgent):

    def __init__(self, num_arms, num_turns, decline_rate=1.001):
        EpsilonGreedyAgent.__init__(self, 1.0, num_arms)
        self._num_turns = num_turns
        self._num_pulls = 0
        self._decline_rate = decline_rate
    
    def reset(self):
        self._num_pulls = 0
        EpsilonGreedyAgent.reset(self)
    
    # Calculates and sets the next epsilon value
    def _adjust_epsilon(self):
        self._epsilon = ((1 - (self._decline_rate**(-self._num_pulls))) /
                         (self._decline_rate**(-self._num_turns) - 1)) + 1
        
    def do_pull(self, bandit):
        self._adjust_epsilon()
        reward = Agent.do_pull(self, bandit)
        self._num_pulls += 1
        return reward

    def __str__(self):
        return f'Variable Epsilon Greedy Agent (decline_rate={self._decline_rate})'
