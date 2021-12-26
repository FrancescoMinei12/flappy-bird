import pygame
import random

pygame.init()

screenbg = pygame.image.load('img/bg.png')
bird = pygame.image.load('img/bird.png')
gameover = pygame.image.load('img/gameover.png')
base = pygame.image.load('img/base.png')
pipe = pygame.image.load('img/pipe.png')
reversePipe = pygame.transform.flip(pipe, False, True)

screen = pygame.display.set_mode((288, 512))
fps = 60
speed_adv = 3
font = pygame.font.SysFont('Comic Sans MS', 50, bold=True)


class Pipe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)

    def print(self):
        self.x -= speed_adv
        screen.blit(pipe, (self.x, self.y + 210))
        screen.blit(reversePipe, (self.x, self.y - 210))

    def die(self, Bird, birdx, birdy):
        t = 5
        bird_dx = birdx+bird.get_width()-t
        bird_sx = birdx+t
        pipe_dx = self.x+reversePipe.get_width()
        pipe_sx = self.x
        bird_up = birdy+t
        bird_down = birdy+bird.get_height()-t
        pipe_up = self.y+110
        pipe_down = self.y+210
        if(bird_dx > pipe_sx and bird_sx < pipe_dx):
            if(bird_up < pipe_up or bird_down > pipe_down):
                lost()

    def middle_pipe(self, Bird, birdx):
        t = 5
        bird_dx = birdx+Bird.get_width()-t
        bird_sx = birdx+t
        pipe_dx = self.x
        pipe_sx = self.x+reversePipe.get_width()
        if(bird_dx > pipe_dx and bird_sx < pipe_sx):
            return True


def draw():
    screen.blit(screenbg, (0, 0))
    for t in pipes:
        t.print()
    screen.blit(bird, (birdX, birdY))
    screen.blit(base, (basex, 400))
    points_drawer = font.render(str(points), 1, (255, 255, 255))
    screen.blit(points_drawer, (144, 0))


def init():
    global birdX, birdY, birdSpeed, basex, pipes, points, middle
    birdX, birdY = 60, 150
    birdSpeed = 0
    basex = 0
    pipes = []
    pipes.append(Pipe())
    points = 0
    middle = False


def update():
    pygame.display.update()
    pygame.time.Clock().tick(fps)


def lost():
    screen.blit(gameover, (50, 180))
    update()
    restart = False
    while(not restart):
        for x in pygame.event.get():
            if(x.type == pygame.KEYDOWN and x.key == pygame.K_SPACE):
                init()
                restart = True
            if(x.type == pygame.QUIT):
                pygame.quit()


init()

while(True):
    basex -= speed_adv
    if (basex < -45):
        basex = 0
    birdSpeed += 1
    birdY += birdSpeed
    for x in pygame.event.get():
        if(x.type == pygame.KEYDOWN and x.key == pygame.K_UP):
            birdSpeed = -10
        if(x.type == pygame.QUIT):
            pygame.quit()
    max = 0
    for p in pipes:
        if p.x > max:
            max = p.x
    if(max < 150):
        pipes.append(Pipe())
    for p in pipes:
        p.die(bird, birdX, birdY)
    if(not middle):
        for t in pipes:
            if(t.middle_pipe(bird, birdX)):
                middle = True
                break
    if(middle):
        middle = False
        for t in pipes:
            if(t.middle_pipe(bird, birdX)):
                middle = True
                break
        if(not middle):
            points += 1
    if(birdY > 380):
        lost()
    draw()
    update()
