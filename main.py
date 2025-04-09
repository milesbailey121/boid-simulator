import pygame
from pygame.locals import *
from boid import Boid
from pygame.math import Vector2 as Vector

pygame.init()
BOID_NUM = 100
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
        for boid in boids:
            boid.move()
            boid.draw(display)

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    main(1280, 720)
