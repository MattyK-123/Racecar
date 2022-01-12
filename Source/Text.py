# External imports
import pygame

# Internal imports
import Colours

# Initialize the pygame font module
pygame.font.init()

# Set the font
font = pygame.font.SysFont('Ariel', 20)


def renderText(screen, text, position):
    # Render the text surface with the FPS value.
    textSurface = font.render(text, False, Colours.BLACK)

    # Draw the text to the screen.
    screen.blit(textSurface, position)
