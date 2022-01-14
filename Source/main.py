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


def main():
    global STATE, dt, screen

    # Define an array to store a list of goal nodes.
    goals= []

    # Define a car variable.
    car = None

    while True:
        # Caps the frame-rate to 100 and returns the change in time in seconds.
        dt = clock.tick(100) * 10 ** (-3)

        # Draw the background surface at the origin
        screen.blit(background, (0, 0))

        # Defines the start of the state machine and its various states.
        if STATE == "INIT":
            # Populate the goal list with objects generated from "Goals.txt".
            goals = Goal.loadGoals("../Data/Goals.txt")

            # Change state to the play state.
            STATE = "PLAY"

            car = Racecar.Racecar(goals)

        elif STATE == "PLAY":
            # Update the car's position based on inputs.
            car.update(dt)

            # Draw the car to the screen.
            car.draw(screen)

            # Draw the goal nodes to the screen.
            for goal in goals:
                goal.draw(screen)

        elif STATE == "QUIT":
            pygame.quit()
            exit()

        # Transition the state to the QUIT state if the close button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                STATE = "QUIT"

        # Draw various statistics to the screen
        Text.draw(screen, "FPS: " + str(round(clock.get_fps(), 5)), (105, 5))
        Text.draw(screen, "STATE: " + STATE, (5, 5))
        Text.draw(screen, "SCORE: " + str(round(car.score, 5)), (205, 5))

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    main()
