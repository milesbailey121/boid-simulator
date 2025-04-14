import pygame
from pygame.locals import *
from src.boid import Boid
from pygame.math import Vector2 as Vector
from src.constants import *
import numpy as np

pygame.init()

def main(height,width):
    run = True

    display = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Boid Simulation")
    pygame.display.set_icon(pygame.image.load("src/assets/icon-32x32.png"))
    clock = pygame.time.Clock()
    visualse_range = False
    boids = []
    for i in range(BOID_NUM):
        boids.append(Boid(i))
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if visualse_range == False:
                    visualse_range = True
                else:
                    visualse_range = False
    
        display.fill((0,0,0))
        # pygame.draw.rect(display, (255, 0, 0), (MARGIN, MARGIN, width - MARGIN, height - MARGIN), 1)
        for boid in boids:
            boid.update_behavior(boids)
            boid.move()
            boid.draw(display)
            if visualse_range:
                boid.draw_range(display)

        pygame.display.update()
        clock.tick(30)
        print(clock.get_fps())

if __name__ == "__main__":
    # main(1280, 720)
    main(640, 480)
