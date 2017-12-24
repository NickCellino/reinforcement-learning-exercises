import csv, os, sys
import pygame

CAPTION = 'Racing Game'
SCREEN_SIZE = (800, 800)

BACKGROUND_COLOR = (255, 50, 50)
RECT_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)

FONT_SIZE = 30
FONT_HEIGHT = 30

TOP_BOTTOM_MARGIN = 10
TRACK_LOCATION = (20, 40)
LEFT_RIGHT_MARGIN = 10

TRACK_SIZE = (SCREEN_SIZE[0] - 2 * LEFT_RIGHT_MARGIN, SCREEN_SIZE[1] - FONT_HEIGHT - 2 * TOP_BOTTOM_MARGIN,)


class RaceTrack:

    OOB = 0
    TRACK = 1
    FINISH = 2
    START = 3

    def __init__(self, csv_path):
        self.track = []
        with open(csv_path, 'r') as csvfile:
            track_layout = csv.reader(csvfile, delimiter=',')
            for row in track_layout:
                new_row = []
                for cell in row:
                    new_row.append(int(cell))
                self.track.append(new_row)

    def perform_action(self, action):
        print(f'Vertical speed: {action[0]}')
        print(f'Horizontal speed: {action[1]}')


class RaceTrackGame:


    def __init__(self, racetrack_csv):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.racetrack = RaceTrack(racetrack_csv)
        self.current_action = [0, 0]

    def update_current_action(self):
        # Forward
        if self.keys[pygame.K_i]:
            self.current_action[0] = min(self.current_action[0] + 1, 4)
        # Back
        if self.keys[pygame.K_k]:
            self.current_action[0] = max(self.current_action[0] - 1, 0)
        # Left
        if self.keys[pygame.K_j]:
            self.current_action[1] = max(self.current_action[1] - 1, 0)
        # Right
        if self.keys[pygame.K_l]:
            self.current_action[1] = min(self.current_action[1] + 1, 4)


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.render_current_action()
        self.render_track()

    def render_current_action(self):
        current_action_string = f'[Vertical: {self.current_action[0]}, Horizontal: {self.current_action[1]}]'
        font = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)
        text_surface = font.render(current_action_string, True, FONT_COLOR)
        self.screen.blit(text_surface, (10, 10))

    def render_track(self):
        pygame.draw.rect(self.screen, RECT_COLOR, (LEFT_RIGHT_MARGIN, FONT_HEIGHT + TOP_BOTTOM_MARGIN, TRACK_SIZE[0], TRACK_SIZE[1]), 2)
        # pygame.draw.rect(self.screen, )

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


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE)
    game = RaceTrackGame('./racetracks/racetrack_a.csv')
    game.main_loop()
    pygame.quit()
    sys.exit()
