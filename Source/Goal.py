import pygame

import Colours


class Goal:
    DEBUG = True

    def __init__(self, start: tuple, end: tuple):
        # Defines the coordinates for the lines endpoints.
        self.start = start
        self.end = end

        # Property that tells the car if the goal is the next active goal.
        self.active = False

    def draw(self, surface: pygame.Surface):
        # Draws the barrier to the screen if debug mode is enabled.
        if Goal.DEBUG and self.active:
            pygame.draw.line(surface, Colours.GREEN, self.start, self.end, 3)
        elif Goal.DEBUG and not self.active:
            pygame.draw.line(surface, Colours.RED, self.start, self.end, 3)


# Returns an array of goal objects created from the provided text file.
def loadGoals(path: str):
    loadedGoals = []
    file = open(path, "r+")
    lines = file.readlines()
    for line in lines:
        split = line.split(",")
        p1 = (float(split[0]), float(split[1]))
        p2 = (float(split[2]), float(split[3]))
        loadedGoals.append(Goal(p1, p2))
    file.close()
    return loadedGoals
