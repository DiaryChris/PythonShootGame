# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 600

PLAYER_SPEED = 8 
BULLET_SPEED = 10
PLAYER_POS = (600, 450)


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
        self.image = []
        for i in range(len(player_rect)): 
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = PLAYER_SPEED
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False


    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        else:
            self.rect.bottom += self.speed
        
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        else:
            self.rect.right += self.speed




#初始化
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Air War')

background = pygame.image.load('resources/image/background.png').convert()
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



# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

#敌机1图片

enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))


player = Player(plane_img, player_rect, PLAYER_POS)

shoot_frequency = 0
enemy_frequency = 0

clock = pygame.time.Clock()

running = True

#主循环
while True:

    clock.tick(60)

    #绘制背景
    screen.fill(0)
    background_rect = background.get_rect()
    bgw = background_rect.width
    bgh = background_rect.height
    row = SCREEN_WIDTH // bgw + 1
    col = SCREEN_HEIGHT // bgh + 1
    for i in range(row):
        for j in range(col):
            screen.blit(background, (i * bgw, j * bgh))
    



    #显示玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        player.img_index += 1
        player.img_index %= 2        



    #子弹处理

    if not player.is_hit:
        if shoot_frequency == 15:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency > 15:
            shoot_frequency = 0

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    player.bullets.draw(screen)



    #敌机处理




    
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


    #刷新状态
    pygame.display.update()

    #退出游戏
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()                    























#