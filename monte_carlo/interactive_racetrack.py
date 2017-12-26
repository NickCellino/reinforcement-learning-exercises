from monte_carlo.racetrack_game import RaceTrackGame
import argparse

parser = argparse.ArgumentParser(description='Interactive Race Track Game')

parser.add_argument('racetrack',
                    type=str,
                    help='Path to racetrack csv file')

args = parser.parse_args()

RaceTrackGame.run(args.racetrack)
