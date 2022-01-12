# External imports
import pygame

# Internal imports
import Colours


class Barrier:
    # Constant that tells the barrier to be drawn to screen
    DEBUG = True

    def __init__(self, screen, start, end):
        # Get reference to the game screen
        self.screen = screen

        # Defines the coordinates for the lines endpoints.
        self.start = start
        self.end = end

        # Is used to change the color of the line if the barrier is being collided with.
        self.COLLISION = False

    def __del__(self):
        # TODO: Save barriers coordinates to file
        pass

    def draw(self):
        # Draws the barrier to the screen if debug mode is enabled
        if Barrier.DEBUG and not self.COLLISION:
            pygame.draw.line(self.screen, Colours.BLACK, self.start, self.end, 3)
        else:
            pygame.draw.line(self.screen, Colours.RED, self.start, self.end, 3)

    def update(self):
        self.draw()
