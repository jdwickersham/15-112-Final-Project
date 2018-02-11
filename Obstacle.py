'''
Obstacle.py

Purpose:
    creates Obstacle, which is a subclass of GameObject

'''
import pygame
import random
from GameObject import GameObject

class Obstacle(GameObject):
	@staticmethod
	def init():
		Obstacle.image_list=[]
		Obstacle.image_list.append(pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/tree.png').convert_alpha(),
            (40, 50)),0)) #bush image
		Obstacle.image_list.append(pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/rock.png').convert_alpha(),
            (40, 40)),0)) #rock image
	
	def __init__(self, x, y):
		self.imageKey=random.randint(0,1)
		super(Obstacle, self).__init__(x, y, Obstacle.image_list[self.imageKey], 30)
		self.x,self.y=x,y