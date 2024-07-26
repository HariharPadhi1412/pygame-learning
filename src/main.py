from os.path import join
from random import randint

import pygame

# general setup

pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

surf = pygame.Surface((100, 200))
player_direction = pygame.math.Vector2(2, -1)
player_speed = 100

# importing an image
player_surface = pygame.image.load(join('../images', 'player.png')).convert_alpha()
player_rect = player_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
star_surface = pygame.image.load(join('../images', 'star.png')).convert_alpha()

meteor_surf = pygame.image.load(join('../images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('../images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

star_position = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the window
    display_surface.fill('darkgray')
    for pos in star_position:
        display_surface.blit(star_surface, pos)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(meteor_surf, meteor_rect)

    player_rect.center += player_direction * player_speed * dt
    display_surface.blit(player_surface, player_rect)

    pygame.display.update()

pygame.init()