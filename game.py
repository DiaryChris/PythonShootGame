# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BULLET_SPEED = 10


#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = BULLET_SPEED

    def move(self):
        self.rect.top -= self.speed
        


#玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self,plane_img, player_rect, init_pos):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = BULLET_SPEED

        self.image = []


    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed
        




#初始化
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Air War')

background = pygame.image.load('resources/image/background.png')
game_over = pygame.image.load('resources/image/gameover.png')
plane_img = pygame.image.load('resources/image/shoot.png')

#玩家飞机动画
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        
player_rect.append(pygame.Rect(165, 360, 102, 126))
#玩家飞机爆炸动画
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

player_pos = (450, 550)
player = Player(plane_img, player_rect, player_pos)

# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

player = plane_img.subsurface(pygame.rect(0, 99, 102, 126))









#主循环
while True:

    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(player, (450, 550))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#键盘事件处理

key_pressed = pygame.key.get_pressed()

if key_pressed[K_w] or key_pressed[K_UP]:
    player.moveUp()
if key_pressed[K_s] or key_pressed[K_DOWN]:
    player.moveDown()
if key_pressed[K_a] or key_pressed[K_LEFT]:
    player.moveLeft()
if key_pressed[K_d] or key_pressed[K_RIGHT]:
    player.moveRight()

#子弹处理



#敌机处理

                    






















#