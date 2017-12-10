from bandit_problems.agents import *
from bandit_problems.test_bed import TestBed
import argparse

parser = argparse.ArgumentParser(description="Exercise 2.2")
parser.add_argument('--arms',
                    type=int,
                    help='Number of arms for the bandit',
                    default=10)
parser.add_argument('--trials',
                    type=int,
                    help='Number of trials to average over',
                    default=2000)
parser.add_argument('--pulls',
                    type=int,
                    help='Number of pulls per trial',
                    default=1000)
args = parser.parse_args()

# Parameters
num_arms = args.arms
num_trials = args.trials
num_pulls = args.pulls

agents = []
agents.append(EpsilonGreedyAgent(0.1, num_arms))
agents.append(ExponentialDecreaseEpsilonGreedyAgent(num_arms, num_pulls, decline_rate=1.01))
agents.append(ExponentialDecreaseEpsilonGreedyAgent(num_arms, num_pulls, decline_rate=1.0075))
agents.append(ExponentialDecreaseEpsilonGreedyAgent(num_arms, num_pulls, decline_rate=1.015))

tb = TestBed(agents, num_arms, num_trials=num_trials, num_pulls=num_pulls)
tb.run()
tb.plot_results(title='Decreasing Epsilon Value')
