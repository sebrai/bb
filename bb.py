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
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy
        self._r = r
        self._color = color
        self._active = True
        Ball.all.append(self)
    def move(self):
        self._x = self._x +self._vx
        self._y = self._y +self._vy
    def draw(self):
        pygame.draw.circle(screen,self._color,(self._x,self._y),float(self._r))
    def remove(self):
        self._active = False
    def check_under(self) -> bool:
        return self._y -self._r > height
    def wall_edge_coll(self) -> bool:
        return self._x -self._r < 0 or self._x + self._r > width
    def top_edge_collision(self) -> bool:
        return self._y - self._r < 0
    def onframe(self):
        self.move()
        if self.check_under(): self.remove()
        if self.top_edge_collision(): self._vy = -self._vy
        if self.wall_edge_coll(): self._vx = -self._vx
        self.draw()
    def is_active(self):
        return self._active
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
        self._width = w
        self._height = h
        self._x:int = floor(width/2)
        self._y:int = floor(height*0.9)
        self._speed =speed
    def draw(self):
        pygame.draw.rect(screen,"white",pygame.Rect(self._x,self._y,self._width,self._height))
    def left(self):
        if not self._x <= 0: self._x = self._x - self._speed
    def right(self):
        if not self._x +self._width >= width: self._x =self._x +self._speed
    def onframe(self):
        self.draw()
Ball(60,60,0,-5)
player = Player()
while running: # game loop

    for event in pygame.event.get(): # actions
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
       player.left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
       player.right()
    screen.fill('black')
    for b in [ball for ball in Ball.all if ball.is_active()]:
        b.onframe()
    player.onframe()

    pygame.display.flip() # rendering happens last
    clock.tick(60) 