import pygame
import numpy as np
import random

DEGREE_MIN_MAX = [0,360]
COLOR_MIN_MAX = [0,255]
TURNFACTOR = 0.2
ROTATEFACTOR = 0.01
MARGIN = 100

class Boid:
    def __init__(self,id):
        self.id = id
        self.width, self.height = pygame.display.get_surface().get_size()
        # Generates a random angle in radians(the standard unit of angular measure used in maths) between 0:360
        self.direction = random.uniform(np.radians(DEGREE_MIN_MAX[0]),np.radians(DEGREE_MIN_MAX[1]))
        # Generates random position on screen
        self.position = np.array([random.uniform(0,self.width),random.uniform(0,self.height)])
        # Generates random velocity vector. 
        # Cosine of direction gives velocity component of x-direction 
        # Sine of direction gives velocity component of y-direction
        self.velocity = np.array([np.cos(self.direction),np.sin(self.direction)])
        
        self.acceleration = np.array([0,0])
        
        self.polygon = np.array([(20,0),(0,5),(0,-5)])
        self.color = ((random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])),(random.uniform(COLOR_MIN_MAX[0],COLOR_MIN_MAX[1])))

    def move(self):
        self.position += self.velocity
        # Logic to loop boids around screen
        if self.position[0] > self.width or self.position[0] < 0:
            self.position[0] = np.abs(self.position[0] - self.width)
        if self.position[1] > self.height or self.position[1] < 0:
            self.position[1] = np.abs(self.position[1] - self.height)
        #TO DO: Implement Boid turning around at boreder 
        # if self.position[0] < MARGIN:
        #     self.velocity[0] = self.velocity[0] + TURNFACTOR
        #     self.direction = self.direction + ROTATEFACTOR
        # if self.position[0] > self.width - MARGIN:
        #     self.velocity[0] = self.velocity[0] - TURNFACTOR
        #     self.direction = self.direction - ROTATEFACTOR
        # if self.position[1] > self.height - MARGIN:
        #     self.velocity[1] = self.velocity[1] - TURNFACTOR
        #     self.direction= self.direction - ROTATEFACTOR
        # if self.position[1] < MARGIN:
        #     self.velocity[1] = self.velocity[1] + TURNFACTOR
        #     self.direction = self.direction + ROTATEFACTOR

    def draw(self,display):
        # https://www.youtube.com/watch?v=a59YQ4qe7mE : 2D rotation matrix
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)],
									[np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(display, self.color, rotated_polygon,0)
