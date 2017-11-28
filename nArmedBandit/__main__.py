from Agent import VariableEpsilonGreedyAgent
from TestBed import TestBed

agents = []
labels = []
num_arms = 10
num_turns = 1000
agents.append(VariableEpsilonGreedyAgent(num_arms, num_turns, 1.01))
labels.append("Exponentially Decreasing Epsilon Greedy Agent (alpha=1.01)")
agents.append(VariableEpsilonGreedyAgent(num_arms, num_turns, 1.05))
labels.append("Exponentially Decreasing Epsilon Greedy Agent (alpha=1.05)")
agents.append(VariableEpsilonGreedyAgent(num_arms, num_turns, 1.1))
labels.append("Exponentially Decreasing Epsilon Greedy Agent (alpha=1.1)")

tb = TestBed(agents, num_arms, num_trials=200, verbose=True)
tb.run()
tb.plot_results(labels)
