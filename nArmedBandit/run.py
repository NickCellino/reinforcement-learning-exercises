from Agent import EpsilonGreedyAgent
from NArmedBandit import NArmedBandit
import numpy as np
import matplotlib.pyplot as plt

num_arms = 10
num_trials = 2000
num_pulls = 1000
epsilon_vals = [0, 0.01, 0.1]
colors = ['r', 'g', 'b']
results = np.zeros((len(epsilon_vals), num_pulls))

for trial_num in range(num_trials):
    agents = []
    for epsilon in epsilon_vals:
        agents.append(EpsilonGreedyAgent(epsilon, num_arms))
    b = NArmedBandit(num_arms)
    for pull in range(num_pulls):
        for i in range(len(epsilon_vals)):
            reward = agents[i].do_pull(b)
            results[i, pull] += reward

results = results / num_trials
for i in range(len(epsilon_vals)):
    plt.plot(results[i], colors[i], label=str(epsilon_vals[i]))
plt.title('10-Armed Bandit Strategies')
plt.xlabel('Pull Number')
plt.ylabel('Average Reward')
plt.legend(loc=4)
plt.show()