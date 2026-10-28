import pygame
from math import floor
# pygame setup
pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

class Block:
    all:list[Block] = []
    def __init__(self):
        pass
class Ball:
    all:list[Ball] = []
    def __init__(self,x:int,y:int,vx:int = 0,vy:int = 0,r:int = 5,color: tuple[int,int,int] | str = (255,255,255)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.active = True
        Ball.all.append(self)
    def move(self):
        self.x = self.x +self.vx
        self.y = self.y +self.vy
    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),float(self.r))
    def remove(self):
        self.active = False
    def check_under(self) -> bool:
        return self.y -self.r > height
    def wall_edge_coll(self) -> bool:
        return self.x -self.r < 0 or self.x + self.r > width
    def top_edge_collision(self) -> bool:
        return self.y - self.r < 0
    def onframe(self):
        self.move()
        if self.check_under(): self.remove()
        if self.top_edge_collision(): self.vy = -self.vy
        if self.wall_edge_coll(): self.vx = -self.vx
        self.draw()
class Level:
    levels = [
        [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        ],
        [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        ],
        [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        ],

    ]
    def __init__(self):
        pass
class Player:
    def __init__(self,w:int = 40,h:int = 15,speed:int = 10):
        self.width = w
        self.height = h
        self.x:int = floor(width/2)
        self.y:int = floor(height*0.9)
        self.speed =speed
    def draw(self):
        pass
    def left(self):
        if not self.x <= 0: self.x = self.x - self.speed
    def right(self):
        pass
Ball(60,60,20)
player = Player()
while running: # game loop

    for event in pygame.event.get(): # actions
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    for b in Ball.all:
        b.onframe()
    

    pygame.display.flip() # rendering happens last
    clock.tick(60) 