import pygame
import numpy as np
import random
from src.constants import *

class Boid:
    def __init__(self, id):
        self.id = id
        self.width, self.height = pygame.display.get_surface().get_size()
        # Generates a random angle in radians(the standard unit of angular measure used in maths) between 0:360
        self.direction = random.uniform(np.radians(DEGREE_MIN_MAX[0]), np.radians(DEGREE_MIN_MAX[1]))
        # Generates random position on screen
        self.position = np.array([random.uniform(MARGIN, self.width - MARGIN), random.uniform(MARGIN, self.height - MARGIN)])
        # Generates random velocity vector. 
        # Cosine of direction gives velocity component of x-direction 
        # Sine of direction gives velocity component of y-direction
        self.velocity = np.array([np.cos(self.direction), np.sin(self.direction)]) * random.uniform(MINSPEED, MAXSPEED)
        
        # Bias-related properties
        self.biasval = 0.001 
        self.scout_group = random.choice([0, 1, 2])  # 0 = no bias, 1 = right bias, 2 = left bias
        
        self.polygon = np.array([(10, 0), (0, 2.5), (0, -2.5)])
        self.color = ((random.uniform(COLOR_MIN_MAX[0], COLOR_MIN_MAX[1])),
                      (random.uniform(COLOR_MIN_MAX[0], COLOR_MIN_MAX[1])),
                      (random.uniform(COLOR_MIN_MAX[0], COLOR_MIN_MAX[1])))

    def move(self):
        # Enforce min and max speeds
        speed = np.linalg.norm(self.velocity)
        if speed < MINSPEED:
            self.velocity = (self.velocity / speed) * MINSPEED
        if speed > MAXSPEED:
            self.velocity = (self.velocity / speed) * MAXSPEED

        # Update boid's position
        self.position += self.velocity
        self.direction = np.arctan2(self.velocity[1], self.velocity[0])

    def update_behavior(self, boids):
        # Zero out the averages and counters 
        xpos_avg, ypos_avg = 0, 0
        xvel_avg, yvel_avg = 0, 0
        neighboring_boids = 0
        close_dx, close_dy = 0, 0

        for other in boids:
            if other.id == self.id:
                continue
            # Calculate the distance between boids
            dx = self.position[0] - other.position[0]
            dy = self.position[1] - other.position[1]
            # Check if the other boid is within the visual range
            # and within the protected range
            # The boids are in a square area of size VISUAL_RANGE
            if abs(dx) < VISUAL_RANGE and abs(dy) < VISUAL_RANGE:
                squared_distance = dx*dx + dy*dy

                if squared_distance < PROTECTED_RANGE**2:
                    close_dx += dx
                    close_dy += dy
                elif squared_distance < VISUAL_RANGE**2:
                    xpos_avg += other.position[0]
                    ypos_avg += other.position[1]
                    xvel_avg += other.velocity[0]
                    yvel_avg += other.velocity[1]
                    neighboring_boids += 1

        # Apply flocking rules if there are neighboring boids
        if neighboring_boids > 0:
            xpos_avg /= neighboring_boids
            ypos_avg /= neighboring_boids
            xvel_avg /= neighboring_boids
            yvel_avg /= neighboring_boids

            # Centering and matching contributions
            self.velocity[0] += (xpos_avg - self.position[0]) * CENTERING_FACTOR + \
                               (xvel_avg - self.velocity[0]) * MATCHING_FACTOR
            self.velocity[1] += (ypos_avg - self.position[1]) * CENTERING_FACTOR + \
                               (yvel_avg - self.velocity[1]) * MATCHING_FACTOR

        # Avoidance contribution
        self.velocity[0] += close_dx * AVOID_FACTOR
        self.velocity[1] += close_dy * AVOID_FACTOR

        # Turn at edges
        if self.position[0] < MARGIN:  # Left margin
            self.velocity[0] += TURNFACTOR
        elif self.position[0] > self.width - MARGIN:  # Right margin
            self.velocity[0] -= TURNFACTOR
        if self.position[1] < MARGIN:  # Top margin
            self.velocity[1] += TURNFACTOR
        elif self.position[1] > self.height - MARGIN:  # Bottom margin
            self.velocity[1] -= TURNFACTOR

        # Dynamic bias update for scout groups
        if self.scout_group == 1:  # Right bias
            if self.velocity[0] > 0:
                self.biasval = min(MAXBIAS, self.biasval + BIAS_INCREMENT)
            else:
                self.biasval = max(0, self.biasval - BIAS_INCREMENT)
        elif self.scout_group == 2:  # Left bias
            if self.velocity[0] < 0:
                self.biasval = min(MAXBIAS, self.biasval + BIAS_INCREMENT)
            else:
                self.biasval = max(0, self.biasval - BIAS_INCREMENT)

        # Apply bias
        if self.scout_group == 1:  # Right bias
            self.velocity[0] = (1 - self.biasval) * self.velocity[0] + (self.biasval * 1)
        elif self.scout_group == 2:  # Left bias
            self.velocity[0] = (1 - self.biasval) * self.velocity[0] + (self.biasval * (-1))

    def draw(self, display):
        # https://www.youtube.com/watch?v=a59YQ4qe7mE : 2D rotation matrix
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],
                                  [np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(display, (self.scout_group * 40,abs(self.velocity[0] * 40),abs(self.velocity[1] * 40)), rotated_polygon, 0)

    def draw_range(self, display):
        pygame.draw.circle(display, "green", self.position.astype(int), VISUAL_RANGE // 2, width=1)
        pygame.draw.circle(display, "red", self.position.astype(int), PROTECTED_RANGE // 2, width=1)

