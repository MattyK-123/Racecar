# External imports
import math

import pygame


class Racecar:
    # Initializes new Racecar object. The cars coordinates are represented using an x and y coordinate along with an
    # angular offset
    def __init__(self, screen):
        # Get reference to the game screen
        self.screen = screen

        # Set the steering sensitivity
        self.steering = 5

        # Racecar coordinates and rotation angle
        self.x = 150
        self.y = 150
        self.a = 38

        # Racecar physics variables
        self.vel = 0
        self.acc = 0

        # Sets acceleration constants
        self.ACC = 500
        self.DEC = -500
        self.BRAKE = 400
        self.FRICTION = 100
        self.STEER = 200

        # Sets the limits for the vehicle
        self.VEL_LIM = 500

        # Import the sprites to be used for the vehicle and scale using scale factor
        scale = 0.1
        self.car = pygame.image.load("../Assets/Racecar.png")
        self.car = pygame.transform.scale(self.car,
                                          (self.car.get_width() * scale, self.car.get_height() * scale))

    def draw(self):
        rotated_image = pygame.transform.rotate(self.car, -1 * self.a)
        self.screen.blit(rotated_image,
                         (self.x - int(rotated_image.get_width() / 2), self.y - int(rotated_image.get_height() / 2)))

    def update(self, dt):
        # Get state of all keys
        keys = pygame.key.get_pressed()

        # If the W key is pressed accelerate
        if keys[pygame.K_w]:
            # Sets the acceleration to the constant when the player is driving
            self.acc = self.ACC
        # If the S key is pressed decelerate
        # elif keys[pygame.K_s]:
        #     # Sets the acceleration to the constant for when the player is reversing
        #     self.acc = self.DEC
        else:
            # Sets the acceleration to 0 if nothing is being pressed
            self.acc = 0

        # If the space key is pressed the car brakes.
        if keys[pygame.K_SPACE]:
            # Brake the vehicle using the brake constant.
            self.vel -= self.BRAKE * dt
            # Cap the velocity so that breaking only stops the vehicle.
            if self.vel < 0:
                self.vel = 0

        if keys[pygame.K_a] and self.vel > 0:
            self.a -= self.STEER * dt
        if keys[pygame.K_d] and self.vel > 0:
            self.a += self.STEER * dt

        # Calculate the change in distance based on the velocity
        delta = self.vel * dt + 0.5 * self.acc * (dt ** 2)

        # Calculate the final velocity value
        self.vel = self.vel + self.acc * dt

        # Cap the vehicles forward and reverse velocities
        if self.vel > 0 and self.vel > self.VEL_LIM:
            self.vel = self.VEL_LIM
        elif self.vel < 0 and self.vel < (self.VEL_LIM * -1):
            self.vel = self.VEL_LIM * -1

        # Update coordinates based on delta
        self.x += delta * math.cos(math.radians(self.a))
        self.y += delta * math.sin(math.radians(self.a))

        # Draw the vehicles changes to the screen
        self.draw()
