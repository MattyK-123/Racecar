import pygame


def main():
    # Initialise pygame.
    pygame.init()

    # Sets the screen dimensions.
    size = 800, 600

    # Import window icon.
    icon = pygame.image.load("Assets/Flag.png")

    # Setting the window title and logo.
    pygame.display.set_caption("Racecar")
    pygame.display.set_icon(icon)

    # Create game window.
    screen = pygame.display.set_mode(size)

    # Create new pygame clock object to maintain constant frame-rate.
    clock = pygame.time.Clock()

    # Define a variable to control the main loop.
    running = True

    # Start the main gameplay loop.
    while running:
        # Caps the frame-rate to 60 and returns the change in time in seconds.
        dt = clock.tick(60) * 10 ** (-3)

        # Terminates the application when the user clicks the exit button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update screen.
        pygame.display.flip()


if __name__ == "__main__":
    main()
