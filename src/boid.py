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

        self.polygon = np.array([(20,0),(0,5),(0,-5)])
        self.color = ((random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])))

    def move(self):
        self.acceleration = self.coherence_acceleration + self.seperate_acceleration + self.align_acceleration

        vel = self.velocity + self.acceleration
        self.velocity = (vel) / np.linalg.norm(vel)
        self.direction = np.arctan2(self.velocity[1],self.velocity[0])
        self.position += self.velocity

        # Logic to loop boids around screen
        # if self.position[0] > self.width or self.position[0] < 0:
        #     self.position[0] = np.abs(self.position[0] - self.width)
        # if self.position[1] > self.height or self.position[1] < 0:
        #     self.position[1] = np.abs(self.position[1] - self.height)
        
        if self.position[0] < MARGIN:
            self.velocity[0] = self.velocity[0] + TURNFACTOR
        if self.position[0] > self.width - MARGIN:
            self.velocity[0] = self.velocity[0] - TURNFACTOR
        if self.position[1] > self.height - MARGIN:
            self.velocity[1] = self.velocity[1] - TURNFACTOR
        if self.position[1] < MARGIN:
            self.velocity[1] = self.velocity[1] + TURNFACTOR

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
            self.coherence_acceleration = np.array([(0,0)])

    def seperate(self,boids,distances):
        near_boids = [
            d[1] for d in distances[self.id]
            if 0 < d[0] > PROTECTED_RANGE
        ]
        if len(near_boids) > 0:
            near_boid = [boids[near_boid_id] for near_boid_id in near_boids]

            centre_of_flock_near = np.mean(np.array([boid.position for boid in near_boid]))

            vector = np.subtract(centre_of_flock_near,self.position)

            self.seperate_acceleration =  - SEPERATION * (vector / np.linalg.norm(vector))
        else:
            self.seperate_acceleration = np.array([(0,0)])

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
            self.align_acceleration = np.array([(0,0)])
        

    def draw(self,display):
        # https://www.youtube.com/watch?v=a59YQ4qe7mE : 2D rotation matrix
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],
									[np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(display, self.color, rotated_polygon,0)
