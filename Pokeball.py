'''
Pokeball.py

Purpose:
    creates Pokeball, which is a subclass of GameObject

'''


import pygame
import random
from GameObject import GameObject
import time

class Pokeball(GameObject):
	minTime=5
	maxTime=20
	@staticmethod
	def init():
		Pokeball.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/pokeball.png').convert_alpha(),
            (25, 25)),0)
	def __init__(self, x, y):
		super(Pokeball, self).__init__(x, y, Pokeball.image, 30)
		self.x,self.y=x,y
		self.counter=0
		self.startTime=time.time()
		self.timeDuration=random.randint(Pokeball.minTime,Pokeball.maxTime) #random time value to be displayed on game object
		self.timeLeft=self.timeDuration-(time.time()-self.startTime)
	def update(self):
		self.timeLeft=self.timeDuration-(time.time()-self.startTime)

