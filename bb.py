import pygame
from math import floor
from random import randint
# pygame setup
pygame.init()
height = 600
width = 800
player_start_height = floor(height*0.9)
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

def check_circle_box_collision(circle_x:int, circle_y:int, radius:int, box_x:int, box_y:int, box_w:int, box_h:int):
    # Find the box edge coordinates
    box_right = box_x + box_w
    box_bottom = box_y + box_h

    # Clamp the circle center coordinates to the box bounds
    closest_x = max(box_x, min(circle_x, box_right))
    closest_y = max(box_y, min(circle_y, box_bottom))

    # Calculate distance from the closest point to the circle center
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    distance_squared = (distance_x ** 2) + (distance_y ** 2)

    # Return True if the distance is less than the radius squared
    return distance_squared < (radius ** 2)


class Block:
    all:list[Block] = []
    def __init__(self,x:int,y:int,w:int,h:int,color:str | tuple[int,int,int] = (120,120,120)):
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        self._active = True
        self._color = color
        Block.all.append(self)
    def draw(self):
        pygame.draw.rect(screen,self._color,pygame.Rect(self._x,self._y,self._width,self._height))
    def onframe(self):
        self.draw()
    def got_hit_by_ball(self): # code checking goes in ball
        self._active = False
    def get_att(self,att:str):
        match att:
            case 'x':return self._x
            case 'y': return self._y
            case 'w': return self._width
            case 'h': return self._height
            case _: return 0
    def is_active(self):
        return self._active
class Ball:
    all:list[Ball] = []
    def __init__(self,x:int | float,y:int,vx:int = 0,vy:int = 0,r:int = 5,color: tuple[int,int,int] | str = (255,255,255)):
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy
        self._r = r
        self._color = color
        self._active = True
        self._prev_x = x
        self._prev_y = y
        Ball.all.append(self)
    def move(self):
        self._prev_x = self._x
        self._prev_y = self._y

        self._x += self._vx
        self._y += self._vy
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
        if self.player_col():
           self.player_collision()
        self.block_coll()
        self.draw()
    def is_active(self):
        return self._active
    def player_col(self):
        return check_circle_box_collision(self._x,self._y,self._r,player.get_dimention('x'),player.get_dimention('y'),player.get_dimention('w'),player.get_dimention('h')) # type: ignore
    
    def player_collision(self):
        if not self.player_col():
            return

        px = player.get_dimention('x')
        py = player.get_dimention('y')
        pw = player.get_dimention('w')

        # Was the ball previously above the paddle?
        if self._prev_y + self._r <= py:
            self._vy = -abs(self._vy)
            self._y = py - self._r
            transfer = 0.3

        # Otherwise, it hit the side
        else:
            if self._prev_x < px:
                self._vx = -abs(self._vx)
            elif self._prev_x > px + pw:
                self._vx = abs(self._vx)
        transfer = 1.0
        # add speed based on player speed
        self._vx = self._vx + player.get_dimention('s')*transfer*player.get_dimention('d')
    def block_coll(self):
        for bl in [block for block in Block.all if block.is_active()]:
            bx = bl.get_att('x')
            by = bl.get_att('y')
            bw = bl.get_att('w')
            bh = bl.get_att('h')

            if not check_circle_box_collision(self._x, self._y, self._r,bx, by, bw, bh): # type: ignore
                continue
            bl.got_hit_by_ball()
            # Previous ball boundaries
            prev_left = self._prev_x - self._r
            prev_right = self._prev_x + self._r
            prev_top = self._prev_y - self._r
            prev_bottom = self._prev_y + self._r

            # Top collision
            if prev_bottom <= by:
                self._vy = -abs(self._vy)
                self._y = by - self._r

            # Bottom collision
            elif prev_top >= by + bh:
                self._vy = abs(self._vy)
                self._y = by + bh + self._r

            # Left collision
            elif prev_right <= bx:
                self._vx = -abs(self._vx)
                self._x = bx - self._r

            # Right collision
            elif prev_left >= bx + bw:
                self._vx = abs(self._vx)
                self._x = bx + bw + self._r

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

class Player:
    def __init__(self,w:int = 60,h:int = 20,speed:int = 10):
        self._width = w
        self._height = h
        self._x:int = floor(width/2)
        self._y:int = player_start_height
        self._speed =speed
        self._dir = 0
    def draw(self):
        pygame.draw.rect(screen,"white",pygame.Rect(self._x,self._y,self._width,self._height))
    def left(self):
        self._dir = -1
        if not self._x <= 0: self._x = self._x - self._speed
    def right(self):
        self._dir = 1
        if not self._x +self._width >= width: self._x =self._x +self._speed
    def onframe(self):
        self._dir = 0
        self.draw()
    def get_dimention(self,type:str) -> int:
        match type:
            case 'x':
                return self._x
            case 'y':
                return self._y
            case 'w':
                return self._width
            case 'h':return self._height
            case 's': return self._speed
            case 'd': return self._dir
            case _:
                return 0
Ball(60,60,5,-5)
Block(100,100,20,20)
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
    if keys[pygame.K_SPACE]:
        Ball(randint(1,width-1),randint(1,200),randint(-10,10),randint(-10,10))
    screen.fill('black')
    for b in [ball for ball in Ball.all if ball.is_active()]:
        b.onframe()
    for bl in [block for block in Block.all if block.is_active()]:
        bl.onframe()
    player.onframe()

    pygame.display.flip() # rendering happens last
    clock.tick(60) 