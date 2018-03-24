# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 600

PLAYER_SPEED = 8 
BULLET_SPEED = 10
ENEMY_SPEED = 2
PLAYER_POS = (600, 450)



#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = BULLET_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        


#玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, player_imgs, player_exp_imgs, init_pos):
        super().__init__()
        self.imgs = player_imgs
        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.exp_imgs = player_exp_imgs
        self.speed = PLAYER_SPEED
        self.bullets = pygame.sprite.Group()
        self.mask = pygame.mask.from_surface(self.image)
        self.img_index = 0
        self.exp_img_index = 0
        self.is_hit = False
        self.shoot_counter = 0


    def shoot(self, bullet_img):
        if self.shoot_counter == 15:
            bullet = Bullet(bullet_img, self.rect.midtop)
            self.bullets.add(bullet)
        self.shoot_counter += 1
        if self.shoot_counter > 15:
            self.shoot_counter = 0
        

    def show(self):
        screen.blit(self.imgs[self.img_index], self.rect)
        self.img_index += 1
        self.img_index %= len(self.imgs)  

    def exp(self):
        screen.blit(self.exp_imgs[self.exp_img_index // 12], self.rect)
        self.exp_img_index += 1
        if self.exp_img_index == len(self.exp_imgs) * 12:
            return True


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

#敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_imgs, enemy_exp_imgs, init_pos):
        super().__init__()
        self.imgs = enemy_imgs
        self.image = self.imgs[0]
        self.exp_imgs = enemy_exp_imgs
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.exp_img_index = 0
        self.speed = ENEMY_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top += self.speed

    def exp(self):
        screen.blit(self.exp_imgs[self.exp_img_index // 5], self.rect)
        self.exp_img_index += 1
        if self.exp_img_index == len(self.exp_imgs) * 5:
            return True


#初始化
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Air War')

#图片载入
background = pygame.image.load('resources/image/background.png').convert()
plane_img = pygame.image.load('resources/image/shoot.png').convert_alpha()

#玩家飞机图片
player_imgs = []
player_imgs.append(plane_img.subsurface(pygame.Rect(0, 99, 102, 126)))       
player_imgs.append(plane_img.subsurface(pygame.Rect(165, 360, 102, 126)))
player_exp_imgs = []
player_exp_imgs.append(plane_img.subsurface(pygame.Rect(165, 234, 102, 126)))
player_exp_imgs.append(plane_img.subsurface(pygame.Rect(330, 624, 102, 126)))
player_exp_imgs.append(plane_img.subsurface(pygame.Rect(330, 498, 102, 126)))
player_exp_imgs.append(plane_img.subsurface(pygame.Rect(432, 624, 102, 126)))


#子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)


#敌机图片
enemy_imgs = []
enemy_imgs.append(plane_img.subsurface(pygame.Rect(534, 612, 57, 43)))
enemy_exp_imgs = []
enemy_exp_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_exp_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_exp_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_exp_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

def main():

    #初始化敌机组
    enemies = pygame.sprite.Group()
    enemies_exp = pygame.sprite.Group()

    #初始化player对象
    player = Player(player_imgs, player_exp_imgs, PLAYER_POS)

    #频率计数器
    enemy_counter = 0
    #计分
    score = 0

    #主循环

    clock = pygame.time.Clock()
    running = True

    while running:

        #限定帧数
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
        

        #玩家飞机绘制
        if not player.is_hit:
            player.show()
        else:
            if player.exp():
                running = False


        #子弹生成
        if not player.is_hit:
            player.shoot(bullet_img)
            

        #子弹动作
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        #子弹绘制
        player.bullets.draw(screen)


        #敌机生成
        if enemy_counter == 50:
            enemy_pos = (random.randint(0, SCREEN_WIDTH - enemy_imgs[0].get_rect().width), 0)
            enemy = Enemy(enemy_imgs, enemy_exp_imgs, enemy_pos)
            enemies.add(enemy)
        enemy_counter += 1
        if enemy_counter > 50:
            enemy_counter = 0

        #敌机动作
        for enemy in enemies:
            enemy.move()
            if pygame.sprite.collide_mask(player, enemy):
                player.is_hit = True
                enemies_exp.add(enemy)
                enemies.remove(enemy)
                break
            for bullet in player.bullets:
                if pygame.sprite.collide_mask(bullet, enemy):
                    enemies_exp.add(enemy)
                    enemies.remove(enemy)
                    score += 1
                    break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)

        for enemy in enemies_exp:
            if enemy.exp():
                enemies_exp.remove(enemy)

        #敌机绘制
        enemies.draw(screen)

        #分数绘制
        score_font = pygame.font.SysFont('arialblack', 36)
        score_text = score_font.render(str(score), True, (127, 127, 127))
        score_rect = score_text.get_rect()
        score_rect.topleft = (25, 20)
        screen.blit(score_text, score_rect)


        #刷新屏幕
        pygame.display.update()
        

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

        #处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    #绘制得分
    font = pygame.font.SysFont('arialblack', 24)
    font_big = pygame.font.SysFont('arialblack', 50)
    text = font.render('Score: '+ str(score), True, (127, 127, 127))
    game_over = font_big.render('Game Over', True, (60, 60, 60))
    text_rect = text.get_rect()
    game_over_rect = game_over.get_rect()
    centerx = screen.get_rect().centerx
    centery = screen.get_rect().centery
    text_rect.centerx = centerx
    text_rect.centery = centery + 30
    game_over_rect.centerx = centerx
    game_over_rect.centery = centery - 30
    screen.blit(text, text_rect)
    screen.blit(game_over, game_over_rect)

    pygame.display.update()

    #游戏退出或重新开始
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                main()

#开始游戏
main()






















#