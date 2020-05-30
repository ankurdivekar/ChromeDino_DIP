import numpy as np
import time
import pyautogui
from pyautogui import press
from PIL import ImageGrab, ImageDraw, ImageOps


class DinoPlayer:

    def __init__(self, visualize_windows):
        self.visualize_windows = visualize_windows

        self.window_offset = None
        self.window_game = None
        self.window_tree = None
        self.window_bird = None
        self.window_sky = None
        self.counter = None
        self.game_init()

    def game_init(self):
        print('Game Init')
        self.window_offset = 175
        self.configure_windows()
        self.counter = 0
        pyautogui.click(x=1460, y=400)
        pyautogui.moveTo(x=1460, y=800)
        pyautogui.press('up')

    def restart(self):
        print('Game Over! Restarting')
        time.sleep(3)
        self.game_init()

    def configure_windows(self):

        self.window_game = {
            'x': 1000,
            'y': 375,
            'w': 500,
            'h': 100
        }

        self.window_sky = {
            'x': 435,
            'y': 3,
            'w': 5,
            'h': 5
        }

        self.window_tree = {
            'x': self.window_offset,
            'y': 60,
            'w': 120,
            'h': 7
        }

        self.window_bird = {
            'x': self.window_offset + 20,
            'y': 40,
            'w': 50,
            'h': 5
        }

    def get_bbox(self, window):

        return [window['x'], window['y'], window['x'] + window['w'], window['y'] + window['h']]

    def get_crop(self, full, window):

        return full[window['y']:window['y'] + window['h'], window['x']:window['x'] + window['w']]

    def run(self):

        while True:
            screen = ImageGrab.grab(bbox=self.get_bbox(self.window_game)).convert("L")

            # If day, invert image
            if screen.getpixel(xy=(0, 0)) > 128:
                screen = ImageOps.invert(screen)
            screen_array = np.asarray(screen)

            if self.visualize_windows:
                draw = ImageDraw.Draw(screen)
                draw.rectangle(xy=self.get_bbox(self.window_tree), fill="black")
                draw.rectangle(xy=self.get_bbox(self.window_bird), fill="black")
                draw.rectangle(xy=self.get_bbox(self.window_sky), fill="black")
                print(screen.getpixel(xy=(0, 0)))
                # screen = ImageOps.invert(screen)
                print(screen_array[3, 470], screen_array[35, 470], screen_array[3, 435], screen_array[35, 435])
                screen.show()
                raise
            elif screen_array[3, 435] > 128 and screen_array[3, 470] > 128 and \
                    screen_array[35, 435] > 128 and screen_array[35, 470] > 128:
                self.restart()

            # Detect Tree
            self.check_obstacle(screen_array, self.window_tree, 'up')
            # Detect Bird
            # self.check_obstacle(screen_array, self.window_bird, 'up')

            self.counter += 1
            if self.counter % 20 == 0:
                self.window_offset += 1
                self.window_tree['x'] += 1
                self.window_bird['x'] += 1
                print(self.window_offset)
            # print(f'Counter: {self.counter}')

    def check_obstacle(self, screen, window, key):
            crop = self.get_crop(screen, window)

            # Check for tree
            for col in range(window['w']):
                for row in range(window['h']):
                    if crop[row, col] > 128:
                        # press(key)
                        self.jump()
                        return

    def jump(self):
        # releasing  the Down Key
        pyautogui.keyUp('down')

        # pressing Space to overcome Bush
        pyautogui.keyDown('up')

        # so that Space Key will be recognized easily
        time.sleep(0.15)

        # releasing the Space Key
        pyautogui.keyUp('up')

        # again pressing the Down Key to keep my Bot always down
        pyautogui.keyDown('down')


if __name__ == "__main__":

    dino = DinoPlayer(visualize_windows=False)
    time.sleep(2)
    dino.run()

