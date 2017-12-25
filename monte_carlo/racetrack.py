import random, csv
import numpy as np


class RacerBot:

    def __init__(self, policy):
        self.policy = policy

    def get_action(self, state_id):
        choices = np.arange(0, self.policy.shape[1])
        probabilities = self.policy[state_id]
        print(f'Choices: {choices}, Probs: {probabilities}')
        return np.random.choice(choices, p=probabilities)


class RaceTrack:

    OOB = 0
    TRACK = 1
    FINISH = 2
    START = 3
    CAR = 4

    MAX_SPEED = 5

    def __init__(self, csv_path):
        self.track = []
        self.start_locations = []
        self.finish_locations = []
        self.visualization = None
        with open(csv_path, 'r') as csvfile:
            track_layout = csv.reader(csvfile, delimiter=',')
            row_num = 0
            for row in track_layout:
                new_row = []
                col_num = 0
                for cell in row:
                    new_cell = int(cell)
                    if new_cell == RaceTrack.START:
                        self.start_locations.append([col_num, row_num])
                    if new_cell == RaceTrack.FINISH:
                        self.finish_locations.append([col_num, row_num])
                    new_row.append(new_cell)
                    col_num += 1
                self.track.append(new_row)
                row_num += 1
        self.current_speed = [0, 0]
        self.car_location = [0, 0]

        # Init car
        self.restart_car()

        self.states = []
        for col in range(len(self.track[0])):
            for row in range(len(self.track)):
                for horizontal_speed in np.arange(0, self.MAX_SPEED):
                    for vertical_speed in np.arange(0, self.MAX_SPEED):
                        self.states.append((col, row, horizontal_speed, vertical_speed))

        self.actions = []
        for horizontal_accel in np.arange(-1, 2):
            for vertical_accel in np.arange(-1, 2):
                self.actions.append((horizontal_accel, vertical_accel))

    def action_to_id(self, action):
        return (
            (action[0] + 1) * 3 +
            (action[1] + 1)
        )

    def id_to_action(self, id):
        return self.actions[id]

    def state_to_id(self, state):
        col = state[0]
        row = state[1]
        horizontal_speed = state[2]
        vertical_speed = state[3]
        return (
            col * len(self.track) * self.MAX_SPEED * self.MAX_SPEED +
            row * self.MAX_SPEED * self.MAX_SPEED +
            horizontal_speed * self.MAX_SPEED +
            vertical_speed
        )

    def id_to_state(self, id):
        return self.states[id]

    def perform_action(self, action_id):
        """
        Returns reward, next state, and if we finished.
        """
        action = self.id_to_action(action_id)
        self.current_speed[0] = max(min(self.current_speed[0] + action[0], self.MAX_SPEED - 1), 0)
        self.current_speed[1] = max(min(self.current_speed[1] + action[1], self.MAX_SPEED - 1), 0)
        if self.crosses_finish_line(self.car_location, self.current_speed):
            self.restart_car()
            return (0, self.state_to_id((self.car_location[0], self.car_location[1], self.current_speed[0], self.current_speed[1])), True)
        else:
            self.car_location = self.get_next_location(self.car_location, self.current_speed)
            if self.out_of_bounds():
                self.restart_car()
            return (-1, self.state_to_id((self.car_location[0], self.car_location[1], self.current_speed[0], self.current_speed[1])), False)

    def crosses_finish_line(self, position, speed):
        horizontal = speed[0]
        vertical = speed[1]
        intermediate_location = [0, 0]
        intermediate_location[0] = self.car_location[0]
        intermediate_location[1] = self.car_location[1]
        while (horizontal + vertical > 0):
            if horizontal >= vertical:
                intermediate_location[0] += 1
                horizontal -= 1
            else:
                intermediate_location[1] -=1
                vertical -= 1
            for finish_location in self.finish_locations:
                if intermediate_location[0] == finish_location[0] and intermediate_location[1] == finish_location[1]:
                    return True
        return False

    def out_of_bounds(self):
        return (self.car_location[0] < 0 or self.car_location[0] >= self.dimensions[0] or
                self.car_location[1] < 0 or self.car_location[1] >= self.dimensions[1] or
                self.track[self.car_location[1]][self.car_location[0]] == self.OOB)

    def get_next_location(self, location, speed):
        next_loc = [location[0] + speed[0], location[1] - speed[1]]
        return next_loc

    def restart_car(self):
        random_start = self.start_locations[random.randint(0, len(self.start_locations) - 1)]
        self.car_location[0] = random_start[0]
        self.car_location[1] = random_start[1]
        self.current_speed = [0, 0]

    @property
    def dimensions(self):
        return (len(self.track[0]), len(self.track))