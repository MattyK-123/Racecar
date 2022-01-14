import math

import pygame

import Goal

# Constants for car physics.
ACC = 500
DEC = -500
BRAKE = 400
FRICTION = 100
STEER = 200
MAX = 500


class Racecar:
    DEBUG = False

    def __init__(self, goals: list):
        # Define a variable to track this instance's score.
        self.score = 0

        # Create a copy of the goal list order.
        self.goals = goals.copy()

        # Define the car's position in the plane and the angle from the origin.
        self.pos = (240, 210)
        self.angle = 38

        # Maintain the coordinates of the car's hit line.
        self.start = (self.pos[0] + 25 * math.cos(math.radians(self.angle)),
                      self.pos[1] + 25 * math.sin(math.radians(self.angle)))
        self.end = (self.pos[0] - 25 * math.cos(math.radians(self.angle)),
                    self.pos[1] - 25 * math.sin(math.radians(self.angle)))

        # Define the car's acceleration and velocity values.
        self.acc = 0
        self.vel = 0

        # Import the sprites to be used for the vehicle and scale using scale factor
        scale = 0.1
        self.car = pygame.image.load("../Assets/Racecar.png")
        self.car = pygame.transform.scale(self.car, (self.car.get_width() * scale, self.car.get_height() * scale))

    def draw(self, screen: pygame.Surface):
        # Rotate the image by the car's angle.
        rotated = pygame.transform.rotate(self.car, -1 * self.angle)

        # Draw the rotated image to the screen.
        screen.blit(rotated, (self.pos[0] - int(rotated.get_width() / 2), self.pos[1] - int(rotated.get_height() / 2)))

    def steer(self, dt: float):
        # Get state of all keys
        keys = pygame.key.get_pressed()
        # Provides steering functionality to the vehicle.a
        if (keys[pygame.K_a]) and self.vel > 0:
            self.angle -= STEER * dt
        if (keys[pygame.K_d]) and self.vel > 0:
            self.angle += STEER * dt

    def drive(self, dt: float):
        # Get state of all keys
        keys = pygame.key.get_pressed()
        # If the W key is pressed accelerate
        if keys[pygame.K_w]:
            # Sets the acceleration to the constant when the player is driving
            self.acc = ACC
        else:
            # Sets the acceleration to 0 if nothing is being pressed
            self.acc = 0
            # Start decreasing the vehicles' velocity due to friction.
            self.vel -= BRAKE * dt
            # Cap the velocity so that breaking only stops the vehicle.
            if self.vel < 0:
                self.vel = 0
        # If the space key is pressed the car brakes.
        if keys[pygame.K_SPACE]:
            # Brake the vehicle using the brake constant.
            self.vel -= BRAKE * dt
            # Cap the velocity so that breaking only stops the vehicle.
            if self.vel < 0:
                self.vel = 0

    def scoring(self):
        # Get the first element of the goals array.
        goal: Goal.Goal = self.goals[0]

        # Check if the cars hit box intersects the goal and update the score. Then add the goal to then end of the list.
        if intersect(self.start, self.end, goal.start, goal.end):
            self.score += 10
            self.goals.append(self.goals.pop(0))

    def update(self, dt: float):
        # Check for acceleration and braking.
        self.drive(dt)

        # Check for steering.
        self.steer(dt)

        # Calculate the final velocity value base on the acceleration.
        self.vel = self.vel + self.acc * dt

        # Cap the car's forward velocity
        self.vel = MAX if self.vel > MAX else self.vel

        # Calculate the change in distance based on the velocity.
        delta = self.vel * dt + 0.5 * self.acc * (dt ** 2)

        # Update the car's position based on its change in distance.
        x = self.pos[0] + delta * math.cos(math.radians(self.angle))
        y = self.pos[1] + delta * math.sin(math.radians(self.angle))
        self.pos = (x, y)

        # Update the car's hit box based on the new position.
        self.start = (self.pos[0] + 25 * math.cos(math.radians(self.angle)),
                      self.pos[1] + 25 * math.sin(math.radians(self.angle)))
        self.end = (self.pos[0] - 25 * math.cos(math.radians(self.angle)),
                    self.pos[1] - 25 * math.sin(math.radians(self.angle)))

        # Calculate the score.
        self.scoring()


def intersect(A: tuple, B: tuple, C: tuple, D: tuple):
    # Helper function defined as a lambda within the intersect method
    def check(X, Y, Z):
        return (Z[1] - X[1]) * (Y[0] - X[0]) > (Y[1] - X[1]) * (Z[0] - X[0])

    # Check if the two line segments intersect each other.
    return True if check(A, C, D) != check(B, C, D) and check(A, B, C) != check(A, B, D) else False
