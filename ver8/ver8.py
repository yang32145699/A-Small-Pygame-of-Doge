import pygame

import random

from pygame.locals import *

from sys import exit

import time

image_left = ['left-1.png','left-2.png','left-3.png','left-4.png']
image_right = ['right-1.png','right-2.png','right-3.png','right-4.png']
image_scale = (72,95)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load(image_left[1]),(image_scale))
        self.rect = self.image.get_rect()
        self.rect.move_ip(500,700)
        self.health = 100
        self.mega = 4
        self.count = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -12)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            if self.count > 3:
                self.count = 0
            self.image = pygame.transform.smoothscale(pygame.image.load(image_left[self.count]),(image_scale))
            self.count += 1
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            if self.count > 2:
                self.count = 0
            self.image = pygame.transform.smoothscale(pygame.image.load(image_right[self.count]),(image_scale))
            self.count += 1
            self.rect.move_ip(5, 0)

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
        self.speed = random.uniform(6, 12)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 700:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin,self).__init__()
        self.image = pygame.image.load('coin.png')
        self.rect = self.image.get_rect(
            center=(random.randint(0, 2000), 0)
        )
        self.speed = random.uniform(3, 10)
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 700:
            self.kill()

pygame.init()

clock = pygame.time.Clock()

flag = 0

screen = pygame.display.set_mode((1000, 700))

pygame.display.set_caption('by.Yang')

background = pygame.image.load('prestart.jpg').convert()

ADDENEMY = pygame.USEREVENT + 1
ADDCOIN = pygame.USEREVENT + 2

pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDCOIN, 2500)

player = Player()

enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    clock.tick(90)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                t1 = time.time()
                flag = 1
                background = pygame.image.load('cloudy.jpg').convert()

            if event.key == K_ESCAPE:
                running = False
                
            if event.key == K_x:
                if player.mega > 2:
                    player.mega -= 3
                    for i in enemies:
                        i.kill()
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCOIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    coins.update()

    
    if flag == 1:
        #Time!
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        hit = pygame.sprite.spritecollide(player,enemies,True)
        for i in hit:
            player.health -= 40

        get_coin = pygame.sprite.spritecollide(player,coins,True)
        for i in get_coin:
            player.health += 10
            player.mega += 1

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
            mega_fortmat = time_font.render('Abilities :   %s' % str(player.mega),True,(255,255,255))
            screen.blit(mega_fortmat,(730,640))

            if player.health <= 40:
                time_font = pygame.font.Font('1.TTF',40)
                warning_fortmat = time_font.render('Last Chance !~',True,(255,255,255))
                screen.blit(warning_fortmat,(350,40))

            #Gravity!
            player.rect.move_ip(0,6)

    pygame.display.flip()
