# External imports
import pygame

# Local imports
import Barrier
import Colours
import Goal
import Racecar
import Text


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

    # Create new pygame clock object to maintain constant frame-rate (100 FPS)
    clock = pygame.time.Clock()

    # Variable used to store the game state
    state = "INIT"

    # Instantiate Barrier object list
    barrierList = []

    # Instantiate Goal object list
    goalList = []

    # Declare Racecar object
    car = None

    # TODO: Keep for adding new goals and barriers
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

            # Import the barriers from the barrier file
            barrierList = Barrier.loadBarriers(screen)

            # Import the goals from the goal file
            goalList = Goal.loadGoals(screen)

            # Initialize Racecar object.
            car = Racecar.Racecar(screen, barrierList, goalList)

        elif state == "PLAY":
            # Call vehicles update method
            car.update(dt)

            # Update barriers
            for barrier in barrierList:
                barrier.update()

            # Update goals
            for goal in goalList:
                goal.update()

        elif state == "QUIT":
            # TODO: Keep for saving barriers to text file
            # Clear barriers text file
            open("../Data/Goals.txt", "w").close()
            # Save the barriers on screen to the text file
            file = open("../Data/Goals.txt", "a")
            for goal in goalList:
                file.write(str(goal.start[0]) + "," + str(goal.start[1]) + "," + str(goal.end[0]) + "," + str(
                    goal.end[1]) + "\n")
            # Close the file and quit
            file.close()

            pygame.quit()
            exit()

        # Transition the state to the QUIT state if the close button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "QUIT"

        # TODO: Keep for adding new goals and barriers
        # Allows the creation of barriers using the mouse
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] and startPoint == (0, 0):
            startPoint = pygame.mouse.get_pos()

        elif keys[pygame.K_e] and endPoint == (0, 0) and not startPoint == (0, 0):
            endPoint = pygame.mouse.get_pos()
            goalList.append(Goal.Goal(screen, startPoint, endPoint))
            startPoint = (0, 0)
            endPoint = (0, 0)

        if not startPoint == (0, 0):
            pygame.draw.line(screen, Colours.BLACK, startPoint, pygame.mouse.get_pos(), 3)

        # Display the fps in the top left corner
        Text.renderText(screen, "FPS: " + str(round(clock.get_fps(), 5)), (105, 5))

        # Display the current game state
        Text.renderText(screen, "STATE: " + state, (5, 5))

        # Display the play cars current score
        Text.renderText(screen, "SCORE: " + str(round(car.score, 5)), (205, 5))

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    main()
