# External imports
import pygame

import Barrier
# Local imports
import FPS
import Racecar


def main():
    # Initialise pygame
    pygame.init()

    # Sets the screen dimensions
    size = 800, 600

    # Import window icon
    icon = pygame.image.load("../Assets/Flag.png")
    # Import background surface
    background = pygame.image.load("../Assets/Track.png")

    # Setting the window title and logo.
    pygame.display.set_caption("Racecar")
    pygame.display.set_icon(icon)

    # Create game window
    screen = pygame.display.set_mode(size)

    # Create new pygame clock object to maintain constant frame-rate (100 FPS).
    clock = pygame.time.Clock()

    # Variable used to store the game state
    state = "INIT"

    # Instantiate Barrier object.
    barrierList = []

    # Instantiate Racecar object.
    car = Racecar.Racecar(screen, barrierList)

    startPoint = (0, 0)
    endPoint = (0, 0)

    # Start the main gameplay loop
    while True:
        # Caps the frame-rate to 100 and returns the change in time in seconds
        dt = clock.tick(100) * 10 ** (-3)

        # Draw the background surface at the origin
        screen.blit(background, (0, 0))

        if state == "INIT":
            # Change state to PLAY state.
            state = "PLAY"

        elif state == "PLAY":
            # Call vehicles update method.
            car.update(dt)

            # Update barriers
            for barrier in barrierList:
                barrier.update()

        elif state == "QUIT":
            pygame.quit()
            exit()

        # Transition the state to the QUIT state if the close button is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "QUIT"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] and startPoint == (0, 0):
            startPoint = pygame.mouse.get_pos()

        elif keys[pygame.K_e] and endPoint == (0, 0) and not startPoint == (0, 0):
            endPoint = pygame.mouse.get_pos()
            barrierList.append(Barrier.Barrier(screen, startPoint, endPoint))
            startPoint = (0, 0)
            endPoint = (0, 0)

        # Display the fps in the top left corner.
        FPS.display(screen, clock)

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    main()
