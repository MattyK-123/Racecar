import math

import pygame

import Colours
import Goal


class Racecar:
    DEBUG = False

    # Constants for car physics.
    ACC = 500
    DEC = -500
    BRAKE = 400
    FRICTION = 100
    STEER = 200
    MAX = 500

    def __init__(self, goals: list):
        # Define a variable to track this instance's score.
        self.score = 0
        self.dead = False

        # Create a copy of the goal list order.
        self.goals = goals.copy()
        self.original = goals.copy()

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

        # Draws the car's hit line if debugging is enabled.
        if Racecar.DEBUG:
            pygame.draw.line(screen, Colours.RED, self.start, self.end, 3)

    def steer(self, dt: float):
        # Get state of all keys
        keys = pygame.key.get_pressed()
        # Provides steering functionality to the vehicle.a
        if keys[pygame.K_a] and self.vel > 0:
            self.angle -= Racecar.STEER * dt
        if keys[pygame.K_d] and self.vel > 0:
            self.angle += Racecar.STEER * dt

    def drive(self, dt: float):
        # Get state of all keys
        keys = pygame.key.get_pressed()
        # If the W key is pressed accelerate
        if keys[pygame.K_w]:
            # Sets the acceleration to the constant when the player is driving
            self.acc = Racecar.ACC
        else:
            # Sets the acceleration to 0 if nothing is being pressed
            self.acc = 0
            # Start decreasing the vehicles' velocity due to friction.
            self.vel -= Racecar.BRAKE * dt
        # If the space key is pressed then the car brakes.
        if keys[pygame.K_SPACE]:
            # Brake the vehicle using the brake constant.
            self.vel -= Racecar.BRAKE * dt
        # Cap the velocity so that breaking only stops the vehicle.
        if self.vel < 0:
            self.vel = 0

    def scoring(self):
        # Get the first element of the goals array.
        goal: Goal.Goal = self.goals[0]

        # Check if the cars hit box intersects the goal and update the score. Then add the goal to then end of the list.
        if intersect(self.start, self.end, goal.start, goal.end):
            self.score += 1
            self.goals.append(self.goals.pop(0))

    def goalcast(self, screen: pygame.Surface):
        # Get the first element of the goals array.
        goal: Goal.Goal = self.goals[0]

        # Get the distance from the car to the goal.
        # distance = np.sqrt((self.pos[0] - goal.center[0]) ** 2 + (self.pos[1] - goal.center[1]) ** 2)

        # Draw the line from the car to the goal node.
        if Racecar.DEBUG:
            pygame.draw.line(screen, Colours.BLUE, self.pos, goal.center, 3)

        # Return an array containing the car's and goal's positions.
        position = [self.pos[0], self.pos[1], goal.center[0], goal.center[1]]

        return position

    def raycast(self, screen: pygame.Surface):
        # Defines the number of rays to be cast.
        rays = 10

        # Define array of distances.
        distances = [None] * rays

        # Lambda that calculates a new point based on angle and distance.
        def position(dist):
            return (self.pos[0] + dist * math.cos(math.radians(i * (360 / rays))),
                    self.pos[1] + dist * math.sin(math.radians(i * (360 / rays))))

        for i in range(rays):
            # Sets the initial pivot points.
            distance = 1
            # Sets the point we wish to check.
            p = position(distance)

            # Take large steps until grass is found.
            while not screen.get_at((math.ceil(p[0]), math.ceil(p[1]))) == Colours.GRASS:
                distance += 10
                p = position(distance)

                # If we've gone out of bounds, decrease the distance until we're safe.
                while ofb(p):
                    distance -= 1
                    p = position(distance)

            # Slows decrease the distance back to the track from previous large step.
            while screen.get_at((int(p[0]), int(p[1]))) == Colours.GRASS:
                distance -= 1
                p = position(distance)

                # Draw ray cast lines to screen if debug is enabled.
                if Racecar.DEBUG:
                    pygame.draw.line(screen, Colours.RED, self.pos, p)
                    pygame.draw.circle(screen, Colours.RED, p, 5)

            # Save the ray cast distance to the nearest edge.
            distances[i] = distance

        return distances

    def reset(self):
        # Mark the car as dead.
        self.dead = True

        # Reset the car's position.
        self.pos = (240, 210)
        self.angle = 38

        # Reset car's physical parameters.
        self.acc = 0
        self.vel = 0

        # Reset the goal order.
        self.goals = self.original.copy()

        # Reset the car's score.
        self.score = 0

    def out(self, screen: pygame.Surface):
        # Determines if the car has driven out of bounds.
        return True if screen.get_at((int(self.pos[0]), int(self.pos[1]))) == Colours.GRASS else False

    def update(self, screen: pygame.Surface, dt: float):
        # Check for acceleration and braking.
        self.drive(dt)

        # Check for steering.
        self.steer(dt)

        # Calculate the final velocity value base on the acceleration.
        self.vel = self.vel + self.acc * dt

        # Cap the car's forward velocity
        self.vel = Racecar.MAX if self.vel > Racecar.MAX else self.vel

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

        # Checks if the car has gone out of bounds and acts accordingly.
        if self.out(screen):
            self.reset()

        # Return an array of the distances to the walls.
        walls = self.raycast(screen)

        # Returns the coordinates of the vehicle and the next goal.
        coords = self.goalcast(screen)

        # Draw the car to the screen.
        self.draw(screen)

        return walls + coords


def intersect(A: tuple, B: tuple, C: tuple, D: tuple):
    # Function that checks if two line segments intersect.
    def check(X, Y, Z):
        return (Z[1] - X[1]) * (Y[0] - X[0]) > (Y[1] - X[1]) * (Z[0] - X[0])

    # Check if the two line segments intersect each other.
    return True if check(A, C, D) != check(B, C, D) and check(A, B, C) != check(A, B, D) else False


def clamp(value, start, end):
    # Restricts a value to the given range.
    return max(min(end, value), start)


def ofb(point: tuple):
    # Function that determines if a point is out of bounds.
    return True if 0 > point[0] or point[0] > 799 or 0 > point[1] or point[1] > 599 else False
