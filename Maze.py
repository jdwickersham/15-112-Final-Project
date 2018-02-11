'''
Maze.py

Purpose:
	every time the game is played, a random maze should be generated, with finish display at end of maze and user placed at beginning of maze

Algorithm:
	the algorithm for creating a maze utilizes Depth First Search, which can be read about at https://en.wikipedia.org/wiki/Maze_generation_algorithm
	original inspiration for make_maze is from https://rosettacode.org/wiki/Maze_generation#Python
'''
import pygame
import random
from GameObject import GameObject

class Wall(GameObject):
	@staticmethod
	def init():
		Wall.image_list=[]
		Wall.image_list.append(pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/bush.png').convert_alpha(),
            (80, 80)),0)) #bush image
		Wall.image_list.append(pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/rock.png').convert_alpha(),
            (80, 80)),0)) #rock image
	
	def __init__(self, x, y):
		super(Wall, self).__init__(x, y, random.choice(Obstacle.image_list), 30)
		self.x,self.y=x,y


def make_maze(width=15,height=10): #make a maze that evenly implements wall dimensions
	visited= [[0]*width for i in range(height)] #not visited values have 0, visited values have 1
	def next_move(x,y): #essentially walks to next space
		visited[x][y] = 1
		moves= [(x-1,y),(x+1,y),(x,y+1),(x,y-1)] #all possible next moves
		random.shuffle(moves) #will check through moves in random order
		for (i,j) in moves:
			final_pos=(i,j) #at very end, this will be the location for winner
			if visited(i,j) in moves: continue
			next_move(i,j)
		return (final_pos,visited) #once all moves have been accounted for, return the grid and winning pos
	
	next_move(40,40) #should start in middle of first empty block
