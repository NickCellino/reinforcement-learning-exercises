from environments.racing.racing import RaceTrackGame
import argparse


parser = argparse.ArgumentParser(description='Plays the racetrack game with the specified policy.')

parser.add_argument('racetrack',
                    type=str,
                    help='Path to racetrack csv file')
parser.add_argument('policy',
                    type=str,
                    help='Path to serialized policy file')
parser.add_argument('--timestep',
                    type=float,
                    help='Length of timesteps (s)',
                    default=0.1)
parser.add_argument('--episodes',
                    type=int,
                    help='Number of episodes to train over',
                    default=10)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()

RaceTrackGame.bot_run(args.racetrack, args.policy, episodes=args.episodes, timestep=args.timestep)
