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


# Classes

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('../images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, delta_time):
        self.player_movement(delta_time)
        self.fire_laser()

    def player_movement(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

    def fire_laser(self):
        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE]:
            pass


class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


all_sprites = pygame.sprite.Group()
meteor = pygame.sprite.Group()

star_surface = pygame.image.load(join('../images', 'star.png')).convert_alpha()

for i in range(20):
    Star(all_sprites, star_surface)

player = Player(all_sprites)

meteor_surf = pygame.image.load(join('../images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('../images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

star_position = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    delta_time = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)

    # draw the window
    all_sprites.update(delta_time)
    display_surface.fill('darkgray')

    display_surface.blit(player.image, player.rect)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.init()