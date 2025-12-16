import random
import pygame
JUMP_FORCE = -16.5
NEWTONTHING =0.75
FLOOR = 300
class Obstacle:
    def __init__(self):
        self.speed = 10
        self.x = 710
        self.y = 0
        self.hitbox0 = pygame.Rect(0,0,115,35)
        self.hitbox1 = pygame.Rect(0,0,30,30)
        self.create()
    def create (self):
        self.obstacle_type = random.randint(0,1)
        self.active_hitbox = self.hitbox0 if self.obstacle_type == 0 else self.hitbox1
        type1_object = ["Eggs0.png", "Eggs1.png","Eggs2.png","Eggs3.png"]
        type0_object = ["SmallTallRock.png"]
        if self.obstacle_type == 0:
            self.image = random.choice(type0_object)
            self.image = pygame.image.load(self.image)
            self.image = pygame.transform.scale_by(self.image, 0.25)
            self.y = 340
        elif self.obstacle_type == 1:
            self.image = random.choice(type1_object)
            self.image = pygame.image.load(self.image)
            self.image = pygame.transform.scale_by(self.image, 0.25)
            self.y = 370
    def update(self, screen, scr):
        self.x -= (self.speed + (scr // 100))
        if self.obstacle_type == 0:
            self.active_hitbox.x = self.x 
            self.active_hitbox.y = self.y + 30
        if self.obstacle_type == 1:
            self.active_hitbox.x = self.x + 45
            self.active_hitbox.y = self.y
        if self.x < -100:
            self.x = 710
            self.create()
        # pygame.draw.rect(screen, "red", self.active_hitbox)
        screen.blit(self.image, (self.x, self.y))
    