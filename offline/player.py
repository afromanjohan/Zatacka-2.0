import random
import pygame
from numpy import sin, cos, deg2rad
from pygamemisc.color import colorTransformer as ct

stepsPerMove = 3





class Player(object):
    def __init__(self, score, left, right, width, height, name):
        self.x = 0
        self.y = 0
        self.color = ct(name)
        self.score = score
        self.alive = True
        self.left = left
        self.right = right
        self.path = []
        self.direction = random.randint(0, 360)
        self.path.append([self.x - 1, self.y - 1, False])
        self.originalDirection = self.direction
        self.xBound = width
        self.yBound = height
        self.name = name
        self.metronome = random.randint(0, 80)

    def __gt__(self, other):
        if self.score > other.score:
            return True
        else:
            return False

    def startNewRound(self):
        self.x = random.randint(100, self.xBound - 100)
        self.y = random.randint(100, self.yBound - 100)
        self.path = []
        self.alive = True
        self.direction = random.randint(0, 360)
        self.metronome = random.randint(0, 80)

    def moveIsOutOfBounds(self, x, y):
        if not 0 < x < self.xBound:
            return True
        if not 0 < y < self.yBound:
            return True
        return False

    def playerDies(self):
        self.alive = False

    def draw(self, win):
        if len(self.path) > 5:
            self.path = self.path[-5: -1]
        for position in range(len(self.path) - 1):
            if self.path[position][2] is True:
                pygame.draw.line(win, self.color, (self.path[position][0], self.path[position][1]),
                             (self.path[position + 1][0], self.path[position + 1][1]), 3)

    def doMove(self, moveType, win):
        self.metronome += 1
        if self.alive is False:
            print(self.name + " died!!")
            return
        degrees = self.direction
        if moveType is self.left:
            degrees -= 3
            calculatedX = stepsPerMove * cos(deg2rad(degrees))
            calculatedY = stepsPerMove * sin(deg2rad(degrees))
            self.direction -= 3
        elif moveType is self.right:
            degrees += 3
            calculatedX = stepsPerMove * cos(deg2rad(degrees))
            calculatedY = stepsPerMove * sin(deg2rad(degrees))
            self.direction += 3
        else:
            calculatedX = stepsPerMove * cos(deg2rad(degrees))
            calculatedY = stepsPerMove * sin(deg2rad(degrees))
        calculatedX = (self.x + calculatedX)
        calculatedY = (self.y + calculatedY)

        self.x = calculatedX
        self.y = calculatedY
        if self.metronome%17 in {1, 2, 3}: vis = False
        else: vis = True
        self.path.append([self.x, self.y, vis])
        if self.metronome == 100: self.metronome = 0

        if self.moveIsOutOfBounds(self.x, self.y):
            self.alive = False
        try:
            x, y = int(calculatedX), int(calculatedY)
            array = pygame.PixelArray(win)[x][y]
            if array != 0:
                self.playerDies()
        except IndexError:
            self.playerDies()
        self.draw(win)
