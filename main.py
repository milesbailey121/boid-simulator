import pygame
from pygame.locals import *
from src.boid import Boid
from pygame.math import Vector2 as Vector
from src.constants import *
import numpy as np

pygame.init()

def distance_between_vectors(vectors):
	distance_list = [[0] * len(vectors) for _ in range(len(vectors))]
	for i in range(len(vectors)):
		distance_list[i][i] = (0, i)
		for j in range(len(vectors)):
			if i < j:
				# Calculate the distance between two vectors.
				distance = np.linalg.norm(np.subtract(vectors[i], vectors[j]))
				# Store the calculated distance at index i,j.
				distance_list[i][j] = (distance, j)
				distance_list[j][i] = (distance, i)
	return distance_list

def main(height,width):
    run = True

    display = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Boid Simulation")
    clock = pygame.time.Clock()
    
    boids = []
    for i in range(BOID_NUM):
        boids.append(Boid(i))
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
    
        display.fill((0,0,0))

        distances = distance_between_vectors([boid.position for boid in boids]) # Added
        for boid in boids:
            boid.cohere(boids,distances)
            boid.seperate(boids,distances)
            boid.align(boids,distances)
            boid.move()
            boid.draw(display)

        clock.tick(30)
        pygame.display.update()
        

if __name__ == "__main__":
    main(1280, 720)
