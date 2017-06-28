import pygame

import random

from pygame.locals import *

from sys import exit

import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('doge.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(500,700)
        self.health = 100
        self.mega = 3

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
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
        self.speed = random.uniform(1.8, 3)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()


pygame.init()

flag = 0

screen = pygame.display.set_mode((1000, 700))

pygame.display.set_caption('by.Yang')

background = pygame.image.load('prestart.jpg').convert()

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
            if event.key == K_RETURN:
                flag = 1
                background = pygame.image.load('cloudy.jpg').convert()
                pass

            if event.key == K_ESCAPE:
                running = False
            if event.key == K_x:
                if player.mega:
                    player.mega -= 1
                    for i in enemies:
                        i.kill()
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

    
    if flag == 1:
        #Time!
        t1 = time.time()
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        hit = pygame.sprite.spritecollide(player, enemies,True)
        for i in hit:
            player.health -= 25

        if player.health <= 0:

            death_background = pygame.image.load('death.jpg').convert()
            screen.blit(death_background, (0, 0))
            screen.blit(time_fortmat,(390,115))

        else:
            t2 = time.time()
            time_passed = int(t2-t1)

            time_font = pygame.font.Font('1.TTF',30)
            time_fortmat = time_font.render('Game Time:  %s' %str(time_passed),True,(255,255,255))
            screen.blit(time_fortmat,(730,580))
            health_fortmat = time_font.render('Health :  %s' % str(player.health),True,(255,255,255))
            screen.blit(health_fortmat,(730,610))
            mega_fortmat = time_font.render('Clear all  %s' % str(player.mega),True,(255,255,255))
            screen.blit(mega_fortmat,(730,640))

            if player.health == 25:
                time_font = pygame.font.Font('1.TTF',40)
                warning_fortmat = time_font.render('Last Chance !~',True,(255,255,0))
                screen.blit(warning_fortmat,(350,500))

            #Gravity!
            player.rect.move_ip(0,1)

    pygame.display.flip()
