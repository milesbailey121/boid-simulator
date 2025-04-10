import pygame
import numpy as np
import random
from src.constants import *

class Boid:
    def __init__(self,id):
        self.id = id
        self.width, self.height = pygame.display.get_surface().get_size()
        # Generates a random angle in radians(the standard unit of angular measure used in maths) between 0:360
        self.direction = random.uniform(np.radians(DEGREE_MIN_MAX[0]),np.radians(DEGREE_MIN_MAX[1]))
        # Generates random position on screen
        self.position = np.array([random.uniform(MARGIN,self.width - MARGIN),random.uniform(MARGIN,self.height - MARGIN)])
        # Generates random velocity vector. 
        # Cosine of direction gives velocity component of x-direction 
        # Sine of direction gives velocity component of y-direction
        self.velocity = np.array([np.cos(self.direction),np.sin(self.direction)])
        
        self.acceleration = np.array([0,0])
        self.coherence_acceleration = np.array([0,0])
        self.seperate_acceleration = np.array([0,0])
        self.align_acceleration = np.array([0,0])
        self.wall_avoidence_acceleration = np.array([0,0])


        self.polygon = np.array([(20,0),(0,5),(0,-5)])
        self.color = ((random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])))

    def move(self):
        self.acceleration = self.coherence_acceleration + self.seperate_acceleration + self.align_acceleration + self.wall_avoidence_acceleration

        vel = self.velocity + self.acceleration
        self.velocity = (vel) / np.linalg.norm(vel)
        self.direction = np.arctan2(self.velocity[1],self.velocity[0])
        self.position += self.velocity

        # Logic to loop boids around screen
        if self.position[0] > self.width or self.position[0] < 0:
            self.position[0] = np.abs(self.position[0] - self.width + 10)
        if self.position[1] > self.height or self.position[1] < 0:
            self.position[1] = np.abs(self.position[1] - self.height + 10)

    def cohere(self,boids,distances):
        near_boids = [
            d[1] for d in distances[self.id]
            if 0 < d[0] < VISUAL_RANGE
        ]
        if len(near_boids) > 0:
            near_boid = [boids[near_boid_id] for near_boid_id in near_boids]

            centre_of_flock = np.mean(np.array([boid.position for boid in near_boid]))

            vector = np.subtract(centre_of_flock,self.position)

            self.coherence_acceleration = COHERENCE * (vector / np.linalg.norm(vector))
        else:
            self.coherence_acceleration = np.array([0,0])

    def seperate(self,boids,distances):
        near_boids = [
            d[1] for d in distances[self.id]
            if 0 <= d[0] < PROTECTED_RANGE
        ]
        if len(near_boids) > 0:
            near_boid = [boids[near_boid_id] for near_boid_id in near_boids]

            center_of_near = np.mean(np.array([boid.position for boid in near_boid]))
			# Difference between self and center of gravity vector of the flock
            vector = np.subtract(center_of_near, self.position)
            
            norm = np.linalg.norm(vector)
            if norm == 0:
                # Overlapping boids: apply a small random force
                self.seperate_acceleration = np.random.uniform(-0.1, 0.1, size=2)
            else:
                # Normal separation (away from center)
                self.seperate_acceleration = -SEPERATION * (vector / norm)
        else:
            self.seperate_acceleration = np.array([0,0])

    def align(self,boids,distances):
        near_boids = [
            d[1] for d in distances[self.id]
            if 0 < d[0] > VISUAL_RANGE
        ]
        if len(near_boids) > 0:
            near_boid = [boids[near_boid_id] for near_boid_id in near_boids]

            vector = np.sum([boid.velocity for boid in near_boid], axis=0)
            self.align_acceleration = ALIGNMENT * (vector / np.linalg.norm(vector))
        else:
            self.align_acceleration = np.array([0,0])
    
    def avoid_walls(self):
        # Reset wall avoidance acceleration each frame
        self.wall_avoidence_acceleration = np.zeros(2)
        
        # Calculate how close we are to each wall (0 = at margin, 1 = at screen edge)
        left_strength = 1 - (self.position[0] / MARGIN) if self.position[0] < MARGIN else 0
        right_strength = 1 - ((self.width - self.position[0]) / MARGIN) if self.position[0] > self.width - MARGIN else 0
        top_strength = 1 - (self.position[1] / MARGIN) if self.position[1] < MARGIN else 0
        bottom_strength = 1 - ((self.height - self.position[1]) / MARGIN) if self.position[1] > self.height - MARGIN else 0
        
        # Apply proportional avoidance force
        if left_strength > 0:
            self.wall_avoidence_acceleration[0] += TURNFACTOR * left_strength
        if right_strength > 0:
            self.wall_avoidence_acceleration[0] -= TURNFACTOR * right_strength
        if top_strength > 0:
            self.wall_avoidence_acceleration[1] += TURNFACTOR * top_strength
        if bottom_strength > 0:
            self.wall_avoidence_acceleration[1] -= TURNFACTOR * bottom_strength


    def draw(self,display):
        # https://www.youtube.com/watch?v=a59YQ4qe7mE : 2D rotation matrix
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],
									[np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(display, self.color, rotated_polygon,0)

    def draw_range(self,display):
        pygame.draw.circle(display,"green",self.position,VISUAL_RANGE / 2,width=1)
        pygame.draw.circle(display,"red",self.position,PROTECTED_RANGE / 2,width=1)
