# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#初始化
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Air War')

background = pygame.image.load('resources/image/background.png')
game_over = pygame.image.load('resources/image/gameover.png')
plane_img = pygame.image.load('resources/image/shoot.png')

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


                






















#