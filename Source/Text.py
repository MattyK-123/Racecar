import pygame
import Colours

# Initialize the pygame font module
pygame.font.init()

# Set the font
font = pygame.font.SysFont('Ariel', 20)


def draw(screen, text, position):
    # Render the text.
    textSurface = font.render(text, False, Colours.BLACK)

    # Draw the text to the screen.
    screen.blit(textSurface, position)
