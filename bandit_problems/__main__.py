from Agent import EpsilonGreedyAgent, FixedAlphaEpsilonGreedyAgent
from TestBed import TestBed

agents = []
labels = []
num_arms = 10
num_trials = 200
num_pulls = 10000
# agents.append(EpsilonGreedyAgent(0, num_arms))
# labels.append("Epsilon Greedy Agent (e = 0)")
# agents.append(EpsilonGreedyAgent(0.01, num_arms))
# labels.append("Epsilon Greedy Agent (e = 0.01)")
agents.append(EpsilonGreedyAgent(0.1, num_arms))
labels.append("Epsilon Greedy Agent (e = 0.1)")
agents.append(FixedAlphaEpsilonGreedyAgent(0.1, num_arms))
labels.append("Fixed Alpha Greedy Agent (alpha = 0.1)")

tb = TestBed(agents, num_arms, num_trials=num_trials, num_pulls=num_pulls, verbose=True)
tb.run_moving()
tb.plot_results(labels)
