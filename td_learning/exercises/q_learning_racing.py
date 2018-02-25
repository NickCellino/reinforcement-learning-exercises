from environments.racing.racing import RaceTrack
from td_learning import td
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Q Learning Racetrack')

parser.add_argument('racetrack',
                    type=str,
                    help='Path to racetrack csv file')
parser.add_argument('policy',
                    type=str,
                    help='Path at which to save policy file')
parser.add_argument('--convergence',
                    type=float,
                    help='Convergence criteria for Q',
                    default=10000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()

racetrack = RaceTrack(args.racetrack)
policy, Q = td.q_learning(
    racetrack,
    alpha_func=lambda n: 1/n,
    epsilon=0.2,
    convergence=args.convergence
)

np.save(args.policy, policy)
