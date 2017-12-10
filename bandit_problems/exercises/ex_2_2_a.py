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
                    default=3000)
args = parser.parse_args()

# Parameters
num_arms = args.arms
num_trials = args.trials
num_pulls = args.pulls

agents = []
agents.append(EpsilonGreedyAgent(0, num_arms))
agents.append(EpsilonGreedyAgent(0.01, num_arms))
agents.append(EpsilonGreedyAgent(0.1, num_arms))

tb = TestBed(agents, num_arms, num_trials=num_trials, num_pulls=num_pulls)
tb.run()
tb.plot_results(title='Exercise 2.2')
