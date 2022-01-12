# External imports
import pygame

# Internal imports
import Colours


class Goal:
    # Constant that tells the barrier to be drawn to screen
    DEBUG = False

    def __init__(self, screen, start, end):
        # Get reference to the game screen
        self.screen = screen

        # Defines the coordinates for the lines endpoints.
        self.start = start
        self.end = end

        # Is used to change the color of the line if the barrier is being collided with.
        self.COLLISION = False

    def draw(self):
        # Draws the barrier to the screen if debug mode is enabled
        if Goal.DEBUG and not self.COLLISION:
            pygame.draw.line(self.screen, Colours.BLACK, self.start, self.end, 3)
        elif Goal.DEBUG and self.COLLISION:
            pygame.draw.line(self.screen, Colours.RED, self.start, self.end, 3)

    def update(self):
        self.draw()


def loadGoals(screen):
    loadedGoals = []

    file = open("../Data/Barriers.txt", "r+")

    lines = file.readlines()

    for line in lines:
        split = line.split(",")

        p1 = (float(split[0]), float(split[1]))
        p2 = (float(split[2]), float(split[3]))
        loadedGoals.append(Goal(screen, p1, p2))

    file.close()

    return loadedGoals
