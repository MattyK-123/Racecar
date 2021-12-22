# External imports

import pygame

# Local imports
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

    # Create new pygame clock object to maintain constant frame-rate
    clock = pygame.time.Clock()

    # Variable used to store the game state
    state = "PLAY"

    # Instantiate Racecar object.
    car = Racecar.Racecar(screen)

    # Start the main gameplay loop
    while True:
        # Caps the frame-rate to 60 and returns the change in time in seconds
        dt = clock.tick(60) * 10 ** (-3)

        # Draw the background surface at the origin
        screen.blit(background, (0, 0))

        if state == "PLAY":
            car.update(dt)
            car.draw()
        elif state == "QUIT":
            pygame.quit()
            exit()

        # Transitions the state to QUIT once the user presses the close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "QUIT"

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    main()
