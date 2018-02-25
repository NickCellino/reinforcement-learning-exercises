import argparse

from environments.blackjack.blackjack import Blackjack, BlackjackStates, BlackjackPlotter
from monte_carlo import mc

parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Improvement')

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
optimal_policy, Q = mc.det_policy_improvement(blackjack, iterations=args.iterations)

if args.verbose:
    for state_id in range(optimal_policy.shape[0]):
        print('--------------------------------')
        BlackjackStates.print_state(state_id)
        if (optimal_policy[state_id] == Blackjack.HIT_ACTION):
            print('HIT')
        else:
            print('STAY')

BlackjackPlotter.plot_policies(optimal_policy)
