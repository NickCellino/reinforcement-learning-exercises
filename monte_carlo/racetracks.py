import csv, os, sys, random
import pygame


class RaceTrack:

    OOB = 0
    TRACK = 1
    FINISH = 2
    START = 3
    CAR = 4

    def __init__(self, csv_path):
        self.track = []
        self.start_locations = []
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
                    new_row.append(new_cell)
                    col_num += 1
                self.track.append(new_row)
                row_num += 1
        self.current_speed = [0, 0]
        self.car_location = [0, 0]

        # Init car
        self.restart_car()

    def perform_action(self, action):
        self.current_speed[0] = max(min(self.current_speed[0] + action[0], 4), 0)
        self.current_speed[1] = max(min(self.current_speed[1] + action[1], 4), 0)
        self.adjust_car_position()
        if self.out_of_bounds():
            self.restart_car()

    def out_of_bounds(self):
        return (self.car_location[0] < 0 or self.car_location[0] >= self.dimensions[0] or
                self.car_location[1] < 0 or self.car_location[1] >= self.dimensions[1] or
                self.track[self.car_location[1]][self.car_location[0]] == self.OOB)

    def restart_car(self):
        random_start = self.start_locations[random.randint(0, len(self.start_locations) - 1)]
        self.car_location[0] = random_start[0]
        self.car_location[1] = random_start[1]
        self.current_speed = [0, 0]

    def adjust_car_position(self):
        self.car_location[0] += self.current_speed[0]
        self.car_location[1] -= self.current_speed[1]

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

    FONT_SIZE = 30
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


    def draw(self):
        self.screen.fill(RaceTrackGame.BACKGROUND_COLOR)
        self.render_current_action()
        self.render_track()
        self.render_car()

    def render_current_action(self):
        current_action_string = f'[Horizontal: {self.current_action[0]}, Vertical: {self.current_action[1]}]'
        font = pygame.font.SysFont(pygame.font.get_default_font(), self.FONT_SIZE)
        text_surface = font.render(current_action_string, True, self.FONT_COLOR)
        self.screen.blit(text_surface, (10, 10))

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

    def update(self):
        pass

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            self.update_current_action()
            if self.keys[pygame.K_RETURN]:
                self.racetrack.perform_action(self.current_action)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.flip()

    @staticmethod
    def run(racetrack_file):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption(RaceTrackGame.CAPTION)
        pygame.display.set_mode(RaceTrackGame.SCREEN_SIZE)
        game = RaceTrackGame(racetrack_file)
        game.main_loop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    RaceTrackGame.run('./racetracks/racetrack_a.csv')
