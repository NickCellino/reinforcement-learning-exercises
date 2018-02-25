import csv
import os
import random
import sys
import time

import numpy as np
import pygame


class RacerBot:

    def __init__(self, policy):
        self.policy = policy

    def get_action(self, state_id):
        choices = np.arange(0, self.policy.shape[1])
        probabilities = self.policy[state_id]
        probabilities /= probabilities.sum()
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

    def num_states(self):
        return len(self.states)

    def num_actions(self):
        return len(self.actions)

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

    def perform_action(self, state_id, action_id):
        """
        Returns reward, next state, and if we finished.
        """
        state = self.id_to_state(state_id)
        current_location = [state[0], state[1]]
        current_speed = [state[2], state[3]]
        action = self.id_to_action(action_id)

        current_speed[0] = max(min(current_speed[0] + action[0], self.MAX_SPEED - 1), 0)
        current_speed[1] = max(min(current_speed[1] + action[1], self.MAX_SPEED - 1), 0)
        if current_speed[0] == 0 and current_speed[1] == 0:
            current_speed[1] = 1
        if self.crosses_finish_line(current_location, current_speed):
            next_state = self.starting_line_state()
            return (0, self.state_to_id(next_state), True)
        else:
            next_location = self.get_next_location(current_location, current_speed)
            if self.out_of_bounds(next_location):
                next_state = self.starting_line_state()
                return (-5, self.state_to_id(next_state), False)
            next_state = (next_location[0], next_location[1], current_speed[0], current_speed[1])
            return (-1, self.state_to_id(next_state), False)

    def crosses_finish_line(self, position, speed):
        horizontal = speed[0]
        vertical = speed[1]
        intermediate_location = [0, 0]
        intermediate_location[0] = position[0]
        intermediate_location[1] = position[1]
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

    def out_of_bounds(self, location):
        return (location[0] < 0 or location[0] >= self.dimensions[0] or
                location[1] < 0 or location[1] >= self.dimensions[1] or
                self.track[location[1]][location[0]] == self.OOB)

    def get_next_location(self, location, speed):
        next_loc = [location[0] + speed[0], location[1] - speed[1]]
        return next_loc

    def get_starting_state(self):
        return self.state_to_id(self.starting_line_state())

    def starting_line_state(self):
        random_start = self.start_locations[random.randint(0, len(self.start_locations) - 1)]
        ret = (random_start[0], random_start[1], 0, 0)
        return ret

    @property
    def dimensions(self):
        return (len(self.track[0]), len(self.track))


class RaceTrackGame:

    CAPTION = 'Racing Game'
    SCREEN_SIZE = (500, 800)

    OOB_COLOR = (240, 252, 22)
    TRACK_COLOR = (147, 150, 155)
    FINISH_COLOR = (1, 75, 234)
    START_COLOR = (2, 234, 72)
    CAR_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (0, 50, 50)
    CELL_BORDER = 2
    SPEED_RIGHT_MARGIN = SCREEN_SIZE[0]/2

    FONT_SIZE = 25
    FONT_HEIGHT = 30
    FONT_COLOR = (255, 255, 255)

    TOP_BOTTOM_MARGIN = 10
    TRACK_LOCATION = (20, 40)
    LEFT_RIGHT_MARGIN = 10

    TRACK_SIZE = (SCREEN_SIZE[0] - 2 * LEFT_RIGHT_MARGIN, SCREEN_SIZE[1] - FONT_HEIGHT - 2 * TOP_BOTTOM_MARGIN)

    def __init__(self, racetrack_csv):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.racetrack = RaceTrack(racetrack_csv)
        self.current_action = [0, 0]
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.FONT_SIZE)

        self.cell_size = self.get_cell_size()
        self.track_top_left = self.get_track_drawing_info()

        self.current_state = self.racetrack.starting_line_state()

        self.current_score = 0

    def get_cell_size(self):
        track_dimensions = self.racetrack.dimensions
        return (int(self.TRACK_SIZE[0] / track_dimensions[0]), int(self.TRACK_SIZE[1] / track_dimensions[1]))

    def get_track_drawing_info(self):
        track_dimensions = self.racetrack.dimensions

        # Correct for rounding
        actual_track_size = (self.cell_size[0] * track_dimensions[0], self.cell_size[1] * track_dimensions[1])
        margins = (self.TRACK_SIZE[0] - actual_track_size[0], self.TRACK_SIZE[1] - actual_track_size[1])

        track_top_left = (self.LEFT_RIGHT_MARGIN + margins[0] / 2, self.FONT_HEIGHT + self.TOP_BOTTOM_MARGIN + margins[1] / 2)

        return track_top_left

    def update_current_action(self):
        # Forward
        if self.keys[pygame.K_i]:
            self.current_action[1] = min(self.current_action[1] + 1, 1)
        # Back
        if self.keys[pygame.K_k]:
            self.current_action[1] = max(self.current_action[1] - 1, -1)
        # Left
        if self.keys[pygame.K_j]:
            self.current_action[0] = max(self.current_action[0] - 1, -1)
        # Right
        if self.keys[pygame.K_l]:
            self.current_action[0] = min(self.current_action[0] + 1, 1)

    def draw(self, state, action):
        self.screen.fill(RaceTrackGame.BACKGROUND_COLOR)
        self.render_current_action(action)
        self.render_game_state(state)

    def render_game_state(self, state):
        self.render_track()
        self.render_current_speed((state[2], state[3]))
        self.render_car((state[0], state[1]))

    def render_current_action(self, action):
        current_action_string = f'[H: {action[0]}, V: {action[1]}]'
        text_surface = self.font.render(current_action_string, True, self.FONT_COLOR)
        self.screen.blit(text_surface, (10, 10))

    def render_current_speed(self, speed):
        current_speed_string = f'Current speed: H: {speed[0]}, V: {speed[1]}'
        text_surface = self.font.render(current_speed_string, True, self.FONT_COLOR)
        self.screen.blit(text_surface, (self.SCREEN_SIZE[0] - self.SPEED_RIGHT_MARGIN, 10))

    def render_track(self):
        for row in range(len(self.racetrack.track)):
            for col in range(len(self.racetrack.track[row])):
                cell = self.racetrack.track[row][col]
                self.draw_cell(cell, col, row)

    def render_car(self, location):
        self.draw_cell(RaceTrack.CAR, location[0], location[1])

    def get_track_pixel_pos(self, col, row):
        return (self.track_top_left[0] + col*self.cell_size[0], self.track_top_left[1] + row*self.cell_size[1])

    def draw_cell(self, cell, col, row):
        if cell == RaceTrack.OOB:
            color = RaceTrackGame.OOB_COLOR
        elif cell == RaceTrack.FINISH:
            color = RaceTrackGame.FINISH_COLOR
        elif cell == RaceTrack.TRACK:
            color = RaceTrackGame.TRACK_COLOR
        elif cell == RaceTrack.START:
            color = RaceTrackGame.START_COLOR
        elif cell == RaceTrack.CAR:
            color = RaceTrackGame.CAR_COLOR
        else:
            raise ValueError('Unknown cell type')

        draw_position = self.get_track_pixel_pos(col, row)

        pygame.draw.rect(self.screen, color, (draw_position[0], draw_position[1], self.cell_size[0] - self.CELL_BORDER, self.cell_size[1] - self.CELL_BORDER))

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            self.update_current_action()
            if self.keys[pygame.K_RETURN]:
                a = self.racetrack.action_to_id(self.current_action)
                s = self.racetrack.state_to_id(self.current_state)
                (r, s, finished) = self.racetrack.perform_action(s, a)
                self.current_score += r
                self.current_state = self.racetrack.id_to_state(s)
                if finished:
                    print('Finished!!')
                    print(f'You scored: {self.current_score}')
                    self.current_score = 0

    def bot_loop(self, bot, episodes, timestep):
        for episode in range(episodes):
            state = self.racetrack.starting_line_state()
            s = self.racetrack.state_to_id(state)
            done = False
            steps = 0
            while not done:
                steps += 1
                a = bot.get_action(s)
                self.draw(self.racetrack.id_to_state(s), self.racetrack.id_to_action(a))
                pygame.display.flip()
                (r, s, done) = self.racetrack.perform_action(s, a)
                time.sleep(timestep)
            print(f'Finished in {steps} steps!')


    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.draw(self.current_state, self.current_action)
            pygame.display.flip()

    @staticmethod
    def init():
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption(RaceTrackGame.CAPTION)
        pygame.display.set_mode(RaceTrackGame.SCREEN_SIZE)

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def bot_run(racetrack_file, policy_file, episodes=10, timestep=1):
        RaceTrackGame.init()
        policy = np.load(policy_file)
        bot = RacerBot(policy)
        game = RaceTrackGame(racetrack_file)
        game.bot_loop(bot, episodes, timestep)
        RaceTrackGame.quit()

    @staticmethod
    def run(racetrack_file):
        RaceTrackGame.init()
        game = RaceTrackGame(racetrack_file)
        game.main_loop()
        RaceTrackGame.quit()