import pygame
from pygamemisc.color import colorTransformer as ct


class Button(object):
    def __init__(self, x, y, width, height, bColor, tColor=(230,130,130), text="", active=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bColor = bColor
        self.tColor = tColor
        self.text = text
        self.active = active

    def draw(self, win):
        if self.active is False:
            return
        pygame.draw.rect(win, self.bColor, (self.x, self.y, self.width, self.height))
        if self.text is not "":
            font = pygame.font.SysFont('calibri', 50)
            text = font.render(self.text, 1, self.tColor)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.active is False:
            return False
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.height + self.y:
                return True
        return False

    def toggleButton(self):
        self.active = not self.active

    def changeText(self, text):
        self.text = text
