import pygame


def main():
    # Initialise pygame.
    pygame.init()

    # Sets the screen dimensions.
    size = 800, 600

    # Create game window.
    screen = pygame.display.set_mode(size)

    # Define a variable to control the main loop.
    running = True

    # Start the main gameplay loop.
    while running:


        # Terminates the application when the user clicks the exit button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
