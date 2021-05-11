import random

class Player:
    def __init__(self, x, y, direction, color, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.alive = True
        self.score = 0
        self.color = color
        self.xBorder = (0, width)
        self.yBorder = (0, height)
        self.left = left
        self.right = right


    def prepareNewROund(self):
        self.x = random.randint(self.xBorder[0] + 100, self.xBorder[1] - 100)
        self.y = random.randint(self.yBorder[0] + 100, self.yBorder[1] - 100)
        self.alive = True
        self.direction = random.randint(0, 360)

    def moveIsOutOfBounds(self, x, y):
        if not xBorder[0] < x < self.xBorder[1]:
            return True
        if not self.yBorder[0] < y < self.yBorder[1]:
            return True
        return False

    def playerDies(self):
        self.alive = False

    def gotoAndReturnNextPos(self, move):
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
        self.x = (self.x + calculatedX)
        self.y = (self.y + calculatedY)
        if self.moveIsOutOfBounds(self.x, self.y): self.playerDies()
        return self.x, self.y