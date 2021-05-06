import pygame, sys, pickle
from offline.game import Game
from pygamemisc.button import Button
from pygamemisc.textblit import Textblit
from pygamemisc.color import colorTransformer as ct
from pygamemisc.color import getNextColor as getPlayingColor


class Menu:
    BG = (0, 0, 0)

    def __init__(self):
        self.WIDTH = 1300
        self.HEIGHT = 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ""
        self.name_font = pygame.font.SysFont("calibri", 80)
        self.title_font = pygame.font.SysFont("calibri", 100)
        self.enter_font = pygame.font.SysFont("calibri", 60)
        self.localButton = Button(400, 500, 500, 80, ct("red"), ct("black"), "Play offline on one PC", False)
        self.multiPlayerButton = Button(400, 700, 500, 80, ct("red"), ct("black"), "Play online", False)

    def drawNameInput(self):
        self.win.fill(self.BG)
        title = self.title_font.render("Achtung die Kurve: Zatacka", 1, (255, 0, 0))
        self.win.blit(title, (self.WIDTH/2 - title.get_width()/2, 50))
        name = self.name_font.render("Type a Name: " + self.name, 1, (255,255,255))
        self.win.blit(name, (100, 400))
        pygame.display.update()

    def drawLocalOrOnline(self):
        self.win.fill(self.BG)
        title = self.title_font.render("Achtung die Kurve: Zatacka", 1, (255, 200, 200))
        self.win.blit(title, (self.WIDTH / 2 - title.get_width() / 2, 50))
        self.localButton.draw(self.win)
        self.multiPlayerButton.draw(self.win)
        pygame.display.update()

    def drawLocalOptionsScreen(self, buttons):
        self.win.fill(self.BG)
        title = self.title_font.render("Achtung die Kurve: Zatacka", 1, (255, 0, 0))
        self.win.blit(title, (self.WIDTH / 2 - title.get_width() / 2, 50))
        for button in buttons:
            button.draw(self.win)

        for i in range(self.numPlayers):
            color = getPlayingColor(i)
            p = self.controllerList[i]
            t = Textblit(f'{color[0]}: {p}', 200, 300 + 60*i, color[1], size=30)
            t.blitText(self.win)
        pygame.display.update()


    
    def typing(self, char):
        if char == "backspace":
            if len(self.name) > 0:
                self.name = self.name[:-1]
        elif char == "space":
            self.name += " "
        elif len(char) == 1:
            self.name += char

        if len(self.name) >= 20:
            self.name = self.name[:20]

    def runNameMenu(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(40)
            self.drawNameInput()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.name) > 1:
                            run = False
                    else:
                        key_name = pygame.key.name(event.key)
                        self.typing(key_name)
        self.runGameModeScreen()

    def runGameModeScreen(self):
        self.localButton.toggleButton()
        self.multiPlayerButton.toggleButton()
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(40)
            self.drawLocalOrOnline()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.localButton.isOver(pos):
                        #start a local game
                        run = False
                        print("Pressed local")
                        self.localButton.toggleButton()
                        self.multiPlayerButton.toggleButton()
                        self.localOptionsScreen()
                    elif self.multiPlayerButton.isOver(pos):
                        print("pressed multiplayer")
                        #start client that connects to server

    def localOptionsScreen(self):
        run = True
        clock = pygame.time.Clock()
        morePlayersButton = Button(200, 900, 300, 80, ct("red"), ct("black"), "Add player", True)
        fewerPlayersButton = Button(700, 900, 300, 80, ct("red"), ct("black"), "Remove player", True)
        startGameButton = Button(500, 600, 300, 80, ct("yellow"), ct("black"), "Start Game", True)
        buttons = [morePlayersButton, fewerPlayersButton, startGameButton]

        self.numPlayers = 1
        self.controllerList = [("LEFT", "RIGHT"), ("q", "a"), ("z", "x"),
                               ("1", "2"), ("KP6", "KP9"), ("v", "b"), ("KP0", "KP_ENTER")]
        while run:
            clock.tick(40)
            self.drawLocalOptionsScreen(buttons)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if morePlayersButton.isOver(pos):
                        print("Pressed add player")
                        if self.numPlayers < 7: self.numPlayers += 1

                    elif fewerPlayersButton.isOver(pos):
                        print("Pressed fewer players")
                        if self.numPlayers > 1: self.numPlayers -= 1
                    elif startGameButton.isOver(pos):
                        game = Game(self.win, self.numPlayers)



if __name__ == "__main__":
    pygame.font.init()
    main = Menu()
    main.runNameMenu()