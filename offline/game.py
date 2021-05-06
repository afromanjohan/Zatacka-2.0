import pygame
import sys
import pickle

from pygamemisc.color import colorTransformer as ct
from pygamemisc.button import Button
from pygamemisc.textblit import Textblit
from offline.player import Player as Player
import time


class Game:
    def __init__(self, window, numOfPlayers):
        self.win = window
        self.BG = ct("Black")
        self.w, self.h = pygame.display.get_surface().get_size()
        self.clock = pygame.time.Clock()
        self.tickrate = 40
        self.remainingRounds = 15
        self.playerList = []
        self.colors = ["Red", "Cyan", "Yellow", "Pink", "Green", "Blue", "Orange"]
        self.controllerList = [(pygame.K_LEFT, pygame.K_RIGHT), (pygame.K_q, pygame.K_a), (pygame.K_z, pygame.K_x),
                               (pygame.K_1, pygame.K_2), (pygame.K_KP6, pygame.K_KP9), (pygame.K_v, pygame.K_b), (pygame.K_KP0, pygame.K_KP_ENTER)]

        for i in range(numOfPlayers):
            p = Player(0, self.controllerList[i][0], self.controllerList[i][1], self.w, self.h, self.colors[i])
            self.playerList.append(p)

        self.gameLoop()

    def gameLoop(self):
        runRound = True
        self.win.fill(self.BG)
        self.drawWindow()
        self.remainingRounds -= 1
        if self.remainingRounds == 0:
            self.drawEndScreen()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()
        alivePlayers = list(self.playerList)
        self.prepareRound()
        while runRound and alivePlayers:
            self.clock.tick(self.tickrate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runRound = False
                    pygame.quit()
            try:
                keys = pygame.key.get_pressed()
            except pygame.error:
                pygame.quit()
            for index, player in enumerate(alivePlayers):
                if keys[player.left]:
                    player.doMove(player.left, self.win)
                elif keys[player.right]:
                    player.doMove(player.right, self.win)
                else:
                    player.doMove(0, self.win)
                if player.alive is False:
                    alivePlayers.pop(index)
                    if len(alivePlayers) == 1:
                        if len(self.playerList) is not 1:
                            p = alivePlayers.pop()
                            p.score += 1
                            print(p.name)

            self.drawWindow()
        self.scoreScreen()

    def scoreScreen(self):
        self.win.fill(ct("Black"))
        restartButton = Button(self.w // 2 - 150, self.h // 2 - 37, 300, 75, ct("Red"), ct("Black"), "New round", True)
        restartButton.draw(self.win)
        for index, player in enumerate(self.playerList):
            textblit = Textblit(player.name + ": " + str(player.score), 500,
                                100 + index * 40, player.color, "calibri", 20)
            textblit.blitText(self.win)
        self.drawWindow()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if restartButton.isOver(pos):
                        self.win.fill(ct("Black"))
                        self.gameLoop()

    def prepareRound(self):
        for player in self.playerList:
            player.startNewRound()

    def drawWindow(self):
        try:
            pygame.display.update()
        except pygame.error:
            pygame.quit()

    def drawEndScreen(self):
        winner = self.playerList[0]
        for i in range(1, len(self.playerList)):
            if self.playerList[i] > winner:
                winner = self.playerList[i]
        self.win.fill(self.BG)
        t = Textblit(f'The winner is: {winner.name}', 500, 500, ct(winner.name), "calibri", 50)
        t.blitText(self.win)
        self.drawWindow()

