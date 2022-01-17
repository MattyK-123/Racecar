import neat
import pygame

import Goal
import Racecar
import Text

# Initialise pygame.
pygame.init()

# Import window icon.
icon = pygame.image.load("../Assets/Flag.png")
# Import background surface.
background = pygame.image.load("../Assets/Track.png")

# Setting the window title and logo.
pygame.display.set_caption("Racecar")
pygame.display.set_icon(icon)

# Sets the screen dimensions.
size = (800, 600)

# Create game window.
screen = pygame.display.set_mode(size)

# Create new pygame clock object to maintain constant frame-rate (100 FPS).
clock = pygame.time.Clock()

# Variable used to store the time between successive frames.
dt = clock.tick(100) * 10 ** (-3)

# Variable used to store the game state.
STATE = "INIT"

# Variables that enables debugging visuals on all classes.
Racecar.Racecar.DEBUG = False
Goal.Goal.DEBUG = False


def main():
    global STATE, dt, screen

    # Define an array to store a list of goal nodes.
    goals = []

    # Populate the goal list with objects generated from "Goals.txt".
    goals = Goal.loadGoals("../Data/Goals.txt")

    # Define a car variable.
    car = Racecar.Racecar(goals)

    while True:
        # Caps the frame-rate to 100 and returns the change in time in seconds.
        dt = clock.tick(100) * 10 ** (-3)

        # Draw the background surface at the origin
        screen.blit(background, (0, 0))

        # Update the car's position based on inputs.
        x = car.update(screen, dt)

        # Draw the goal nodes to the screen.
        for goal in goals:
            goal.draw(screen)

        # Check the even log for certain events.
        for event in pygame.event.get():
            # Transition the state to the QUIT state if the close button is clicked.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Check if the keys 1 or 2 where pressed to enable the various debug displays.
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    Racecar.Racecar.DEBUG = not Racecar.Racecar.DEBUG
                elif event.key == pygame.K_2:
                    Goal.Goal.DEBUG = not Goal.Goal.DEBUG

        # Draw various statistics to the screen
        Text.draw(screen, "FPS: " + str(round(clock.get_fps(), 4)), (105, 5))
        Text.draw(screen, "STATE: " + STATE, (5, 5))

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    # Load configuration for NEAT-Python.
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         "../Data/Config.txt")

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(5))

    main()
