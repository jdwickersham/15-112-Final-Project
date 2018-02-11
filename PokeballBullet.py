'''
Enemy.py

Purpose:
    creates PokeballBullet, which is a subclass of GameObject

'''
import pygame
import math
from GameObject import GameObject


class PokeballBullet(GameObject):
    def init():
        PokeballBullet.speed= 15
        PokeballBullet.size=20

    def __init__(self, x, y, x1, y1):
        size = PokeballBullet.size
        image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images/pokeball.png').convert_alpha(),
            (20, 20)),0)
        super(PokeballBullet, self).__init__(x, y, image, size // 2)
        dx=(x1-x)
        dy=(y1-y)
        hyp= math.sqrt(dx**2+dy**2)
        vx= PokeballBullet.speed * dx/hyp
        vy= PokeballBullet.speed * dy/hyp
        self.velocity = vx, vy
        self.timeOnScreen = 0

    def update(self, screenWidth, screenHeight):
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        if self.rect.left > screenWidth:
            self.kill()
        elif self.rect.right < 0:
            self.kill()
        if self.rect.top > screenHeight:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        #delete pokeball if it misses and goes off screen
        
        