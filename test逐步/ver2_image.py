import pygame

import random

from pygame.locals import *

from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('doge.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.move_ip(500,700)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 700:
            self.rect.bottom = 700


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('rain.png')
        self.rect = self.image.get_rect(
            center=(random.randint(0, 1000), 0)
        )
        self.speed = random.uniform(1.5, 2.2)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()


pygame.init()

screen = pygame.display.set_mode((1000, 700))

pygame.display.set_caption('DogeGam by.Yang')

background = pygame.image.load('cloudy.jpg').convert()

ADDENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(ADDENEMY, 250)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        exit()
    #Gravity!
    player.rect.move_ip(0,1)

    pygame.display.flip()