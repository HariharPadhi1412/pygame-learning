from os.path import join
from random import randint, uniform

import pygame

# general setup

pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

star_surface = pygame.image.load(join('../images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('../images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('../images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('../images', 'Oxanium-Bold.ttf'), 20)
font_surface = font.render('text', True, 'red')


# Classes

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('../images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400  # milliseconds

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
        self.check_fire_event(recent_keys)

    def check_fire_event(self, recent_keys):
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_grp))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)
        self.speed = 400

    def update(self, delta_time):
        self.rect.centery -= self.speed * delta_time
        self.kill_sprite()

    def kill_sprite(self):
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, position, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=position)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        self.kill_meteor()

    def kill_meteor(self):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
meteor_grp = pygame.sprite.Group()
laser_grp = pygame.sprite.Group()


def collisions():
    collision_sprite = pygame.sprite.spritecollide(player, meteor_grp, True)

    for laser in laser_grp:
        collided_meteor = pygame.sprite.spritecollide(laser, meteor_grp, True)
        if collided_meteor and len(collided_meteor) >= 1:
            laser.kill()


def display_score():
    current_time = pygame.time.get_ticks()
    text_surface = font.render(str(current_time), True, 'red')
    text_rect = text_surface.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surface, text_rect)
    pygame.draw.rect(display_surface, (250, 250, 250), text_rect.inflate(20, 40).move(0, -5), 5, 10)


for i in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)

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
            Meteor(meteor_surf, (x, y), (meteor_grp, all_sprites))

    # draw the window
    all_sprites.update(delta_time)
    collisions()
    display_surface.fill('darkgray')
    display_score()
    display_surface.blit(player.image, player.rect)
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.init()