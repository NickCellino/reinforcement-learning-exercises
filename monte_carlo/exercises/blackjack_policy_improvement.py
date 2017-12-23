from monte_carlo.blackjack import Blackjack
from monte_carlo.blackjack_policies import *
from monte_carlo.mc import MonteCarlo
import argparse


parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Q Evaluation')

parser.add_argument('--iterations',
                    type=int,
                    help='Number of iterations to run',
                    default=5000000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


blackjack = Blackjack(verbose=args.verbose)
optimal_policy, Q = MonteCarlo.policy_improvement(blackjack, iterations=args.iterations)

if args.verbose:
    for state_id in range(optimal_policy.shape[0]):
        print('--------------------------------')
        BlackjackStates.print_state(state_id)
        if (optimal_policy[state_id] == Blackjack.HIT_ACTION):
            print('HIT')
        else:
            print('STAY')

BlackjackPlotter.plot_policies(optimal_policy)
