'''
User.py

Purpose:
    creates User, which is a subclass of GameObject

'''
import pygame
import math
from GameObject import GameObject

class User(GameObject):
    @staticmethod
    def init():
        User.leftImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/userLeft.png').convert_alpha(),
            (30, 50)),0)
        User.rightImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/userRight.png').convert_alpha(),
            (30, 50)),0)

    def __init__(self, x, y, PID):
        super(User, self).__init__(x, y, User.leftImage, 40)
        self.PID=PID
        self.numPokemon=0 #use to display pokeCounts to other users
        self.scoreInputted=False
        self.andrewID=''
        self.x,self.y=x,y
        self.speed = 10
        self.dx=-1
        self.dy=1

    def move(self,keysDown): #switch image when switching direction
        leftFlag,rightFlag,upFlag,downFlag=False,False,False,False
        if keysDown(pygame.K_LEFT) and rightFlag==False:
            leftFlag=True
            self.dx=-1
            self.x-=self.speed
            self.baseImage=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/userLeft.png').convert_alpha(),
            (30, 50)),0)
        else:leftFlag=False
        
        
        if keysDown(pygame.K_RIGHT) and leftFlag==False:
            rightFlag=True
            self.dx=1
            self.x+=self.speed
            self.baseImage=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/userRight.png').convert_alpha(),
            (30, 50)),0)
        else: rightFlag=False
        
        if not keysDown(pygame.K_RIGHT) and not keysDown(pygame.K_LEFT):
            self.dx=0

        if keysDown(pygame.K_UP) and downFlag==False:
            upFlag=True
            self.dy=1
            self.y-=self.speed
        else: upFlag=False

        if keysDown(pygame.K_DOWN) and upFlag==False:
            downFlag=True
            self.dy=-1
            self.y+=self.speed
        else: downFlag=False

        if not keysDown(pygame.K_UP) and not keysDown(pygame.K_DOWN):
            self.dy=0
    
    def changePID(self,PID): #use to identify multiple players
        self.PID=PID
    
    def movePos(self,x,y): #use to move otherPlayer
        self.x=x
        self.y=y

    def update(self,keysDown, screenWidth, screenHeight):
        super(User, self).update(screenWidth, screenHeight)

