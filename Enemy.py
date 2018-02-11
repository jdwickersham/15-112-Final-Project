'''
Enemy.py

Purpose:
    creates Enemy, which is a subclass of GameObject

'''

#https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_I)
#name, image, speed= average stats/10

import pygame
import random
from GameObject import GameObject

class Enemy (GameObject):
    @staticmethod
    def init():
        Enemy.leftImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/enemyLeft.png').convert_alpha(),
            (40, 60)),0)
        Enemy.rightImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/enemyRight.png').convert_alpha(),
            (40, 60)),0)
        Enemy.leftSteal = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/enemyLeftStolen.png').convert_alpha(),
            (40, 60)),0)
        Enemy.rightSteal = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/enemyRightStolen.png').convert_alpha(),
            (40, 60)),0)
        Enemy.speed=3
    
    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y, Enemy.leftImage, 30)
        self.x,self.y=x,y
        self.canSteal=True
        self.angleSpeed=random.randint(-10,10)
        self.vX=random.uniform(-Enemy.speed, Enemy.speed)
        self.vY=random.uniform(-Enemy.speed, Enemy.speed)
        if self.vX>0: self.image= Enemy.rightImage
        self.velocity= self.vX,self.vY

    def update(self, screenWidth, screenHeight):
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= screenHeight + self.height
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        if self.vX>0 and self.canSteal==True:
            self.image=Enemy.rightImage
        if self.vX<0 and self.canSteal==True:
            self.image=Enemy.leftImage
        if self.vX>0 and self.canSteal==False:
            self.image=Enemy.rightSteal
        if self.vX<0 and self.canSteal==False:
            self.image=Enemy.leftSteal
        self.updateRect()