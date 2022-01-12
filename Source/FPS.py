import pygame
import Colours

# Initialize the pygame font module
pygame.font.init()

# Set the font
font = pygame.font.SysFont('Ariel', 20)


# Display the current FPS.
def display(screen, clock):
    # Render the text surface with the FPS value.
    textsurface = font.render("FPS: " + str(round(clock.get_fps(), 4)), False, Colours.BLACK)
    # Draw the text to the screen.
    screen.blit(textsurface, (5, 5))
