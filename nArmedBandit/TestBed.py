from NArmedBandit import NArmedBandit
import numpy as np
import matplotlib.pyplot as plt

class TestBed:

    _plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, 
                 agents,
                 num_arms=10, 
                 num_trials=2000, 
                 num_pulls=1000):
        self._num_arms = num_arms
        self._num_trials = num_trials
        self._num_pulls = num_pulls
        self._agents = agents
        self._results = np.zeros((len(agents), num_pulls))
    
    def _reset_agents(self):
        for agent in self._agents:
            agent.reset()
    
    def run(self):
        for trial_num in range(self._num_trials):
            b = NArmedBandit(self._num_arms)
            self._reset_agents()
            for pull in range(self._num_pulls):
                for i in range(len(self._agents)):
                    reward = self._agents[i].do_pull(b)
                    self._results[i, pull] += reward
    
    def plot_results(self, labels):
        avgs = self._results / self._num_trials
        for i in range(len(self._agents)):
            plt.plot(avgs[i], self._plot_colors[i%len(self._plot_colors)], label=labels[i])
        plt.title(str(self._num_arms) + '-Armed Bandit TestBed')
        plt.xlabel('Pull Number')
        plt.ylabel('Average Reward')
        plt.legend(loc=4)
        plt.show()
