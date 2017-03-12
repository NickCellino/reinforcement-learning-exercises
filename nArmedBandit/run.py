from TestBed import TestBed
from Agent import EpsilonGreedyAgent, SoftmaxAgent

agents = []
labels = []
num_arms = 10
agents.append(EpsilonGreedyAgent(0.01, num_arms))
labels.append("E-Greedy (e=0.01)")
agents.append(EpsilonGreedyAgent(0.1, num_arms))
labels.append("E-Greedy (e=0.1)")
agents.append(SoftmaxAgent(.15, num_arms))
labels.append("Softmax (t=0.15)")
agents.append(SoftmaxAgent(.25, num_arms))
labels.append("Softmax (t=0.25)")

tb = TestBed(agents, num_arms)
tb.run()
tb.plot_results(labels)