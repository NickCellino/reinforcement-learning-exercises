import os, sys, pygame, time
import numpy as np

from monte_carlo.racetrack import RaceTrack, RacerBot


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


    def draw(self, action):
        self.screen.fill(RaceTrackGame.BACKGROUND_COLOR)
        self.render_current_action(action)
        self.render_current_speed()
        self.render_track()
        self.render_car()

    def render_current_action(self, action):
        current_action_string = f'[H: {action[0]}, V: {action[1]}]'
        text_surface = self.font.render(current_action_string, True, self.FONT_COLOR)
        self.screen.blit(text_surface, (10, 10))

    def render_current_speed(self):
        current_speed_string = f'Current speed: H: {self.racetrack.current_speed[0]}, V: {self.racetrack.current_speed[1]}'
        text_surface = self.font.render(current_speed_string, True, self.FONT_COLOR)
        self.screen.blit(text_surface, (self.SCREEN_SIZE[0] - self.SPEED_RIGHT_MARGIN, 10))

    def render_track(self):
        for row in range(len(self.racetrack.track)):
            for col in range(len(self.racetrack.track[row])):
                cell = self.racetrack.track[row][col]
                self.draw_cell(cell, col, row)

    def render_car(self):
        self.draw_cell(RaceTrack.CAR, self.racetrack.car_location[0], self.racetrack.car_location[1])

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
                self.racetrack.perform_action(a)

    def bot_loop(self, bot, episodes):
        for episode in range(episodes):
            location = self.racetrack.car_location
            speed = self.racetrack.current_speed
            state = (location[0], location[1], speed[0], speed[1])
            state_id = self.racetrack.state_to_id(state)
            done = False
            while not done:
                a = bot.get_action(state_id)
                self.draw(self.racetrack.id_to_action(a))
                pygame.display.flip()
                (r, state_id, done) = self.racetrack.perform_action(a)
                time.sleep(1)


    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.draw(self.current_action)
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
    def bot_run(racetrack_file, bot, episodes=10):
        RaceTrackGame.init()
        game = RaceTrackGame(racetrack_file)
        game.bot_loop(bot, episodes)
        RaceTrackGame.quit()

    @staticmethod
    def run(racetrack_file):
        RaceTrackGame.init()
        game = RaceTrackGame(racetrack_file)
        game.main_loop()
        RaceTrackGame.quit()


# RaceTrackGame.run('./monte_carlo/racetracks/racetrack_a.csv')

policy = np.zeros((1, 9)) + (1/9)
bot = RacerBot(np.tile(policy, (20000, 1)))
RaceTrackGame.bot_run('./monte_carlo/racetracks/racetrack_a.csv', bot, episodes=3)