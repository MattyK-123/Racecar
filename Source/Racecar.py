# External imports
import math

import pygame

# Internal imports
import Colours


class Racecar:
    # Constant that tells the car to draw debug lines.
    DEBUG = True

    def __init__(self, screen, barrierList):

        # Get reference to the game screen
        self.screen = screen

        # Get reference to list of barriers
        self.barrierList = barrierList

        # Set the steering sensitivity
        self.steering = 5

        # Racecar coordinates and rotation angle
        self.x = 150
        self.y = 150
        self.a = 38

        # Sets car's collision line points.
        self.front = (self.x + 25 * math.cos(math.radians(self.a)), self.y + 25 * math.sin(math.radians(self.a)))
        self.back = (self.x - 25 * math.cos(math.radians(self.a)), self.y - 25 * math.sin(math.radians(self.a)))

        # Racecar physics variables
        self.vel = 0
        self.acc = 0

        # Sets vehicle constants
        self.ACC = 500
        self.DEC = -500
        self.BRAKE = 400
        self.FRICTION = 100
        self.STEER = 200

        # Sets the limits for the vehicle
        self.VEL_LIM = 500

        # Import the sprites to be used for the vehicle and scale using scale factor
        scale = 0.1
        self.carSurface = pygame.image.load("../Assets/Racecar.png")
        self.carSurface = pygame.transform.scale(self.carSurface,
                                                 (self.carSurface.get_width() * scale,
                                                  self.carSurface.get_height() * scale))

        # Draw the image for the first time and store the images rectangle
        rotated_image = pygame.transform.rotate(self.carSurface, -1 * self.a)
        self.carRect = self.screen.blit(rotated_image,
                                        (self.x - int(rotated_image.get_width() / 2),
                                         self.y - int(rotated_image.get_height() / 2)))

    # Return true if line segments AB and CD intersect
    def intersect(self):

        # Helper function defined as a lambda within the intersect method
        def ccw(A_, B_, C_):
            return (C_[1] - A_[1]) * (B_[0] - A_[0]) > (B_[1] - A_[1]) * (C_[0] - A_[0])

        for barrier in self.barrierList:
            A = self.front
            B = self.back
            C = barrier.start
            D = barrier.end
            if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
                barrier.COLLISION = True
                # return True
            else:
                barrier.COLLISION = False
        return False

    def draw(self):
        # Rotate the image by the angle "a".
        rotated_image = pygame.transform.rotate(self.carSurface, -1 * self.a)

        # Draw the rotated image to the screen.
        self.carRect = self.screen.blit(rotated_image,
                                        (self.x - int(rotated_image.get_width() / 2),
                                         self.y - int(rotated_image.get_height() / 2)))

        # If debug is enabled, draw the car's collision line.
        if Racecar.DEBUG:
            pygame.draw.line(self.screen, Colours.BLACK, self.front, self.back, 3)

    def update(self, dt):
        # Get state of all keys
        keys = pygame.key.get_pressed()

        # If the W key is pressed accelerate
        if keys[pygame.K_w]:
            # Sets the acceleration to the constant when the player is driving
            self.acc = self.ACC
        else:
            # Sets the acceleration to 0 if nothing is being pressed
            self.acc = 0
            # Start decreasing the vehicles' velocity due to friction.
            self.vel -= self.BRAKE * dt
            # Cap the velocity so that breaking only stops the vehicle.
            if self.vel < 0:
                self.vel = 0

        # If the space key is pressed the car brakes.
        if keys[pygame.K_SPACE]:
            # Brake the vehicle using the brake constant.
            self.vel -= self.BRAKE * dt
            # Cap the velocity so that breaking only stops the vehicle.
            if self.vel < 0:
                self.vel = 0

        # Provides steering functionality to the vehicle.a
        if keys[pygame.K_a] and self.vel > 0:
            self.a -= self.STEER * dt
        if keys[pygame.K_d] and self.vel > 0:
            self.a += self.STEER * dt

        # Calculate the change in distance based on the velocity
        delta = self.vel * dt + 0.5 * self.acc * (dt ** 2)

        # Calculate the final velocity value
        self.vel = self.vel + self.acc * dt

        # Cap the vehicles forward velocity
        if self.vel > 0 and self.vel > self.VEL_LIM:
            self.vel = self.VEL_LIM

        # Update coordinates based on delta
        self.x += delta * math.cos(math.radians(self.a))
        self.y += delta * math.sin(math.radians(self.a))

        # Cap the vehicles' x coordinate to the width of the screen
        if self.x > 800:
            self.x = 0
        elif self.x < 0:
            self.x = 800

        # Cap the vehicles' y coordinate to the width of the screen
        if self.y > 600:
            self.y = 0
        elif self.y < 0:
            self.y = 600

        # Calculates the car's new collision points
        self.front = (self.x + 25 * math.cos(math.radians(self.a)), self.y + 25 * math.sin(math.radians(self.a)))
        self.back = (self.x - 25 * math.cos(math.radians(self.a)), self.y - 25 * math.sin(math.radians(self.a)))

        # Check for intersections with barriers.
        self.intersect()

        # Draw the vehicles changes to the screen
        self.draw()
