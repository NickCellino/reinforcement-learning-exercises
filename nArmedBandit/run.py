from TestBed import TestBed
from Agent import EpsilonGreedyAgent, SoftmaxAgent

agents = []
labels = []
num_arms = 10
temps = [.25, .45, .65, .85]
for temp in temps:
    agents.append(SoftmaxAgent(temp, num_arms))
    labels.append("Softmax (t=" + str(temp) + ")")

tb = TestBed(agents, num_arms)
tb.run()
tb.plot_results(labels)