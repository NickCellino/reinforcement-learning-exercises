from monte_carlo.blackjack import Blackjack
from monte_carlo import mc
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Q Evaluation')

parser.add_argument('--episodes',
                    type=int,
                    help='Number of episodes to train over',
                    default=10000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


blackjack = Blackjack(verbose=args.verbose)

policy = np.zeros(blackjack.num_states())
Q = mc.fv_policy_q_evaluation(blackjack, policy, episodes=args.episodes)
