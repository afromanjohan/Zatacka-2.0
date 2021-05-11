import pygame
from pygamemisc.textblit import Textblit


class Game:
    def __init__(self, win, connection=None):
        pygame.font.init()
        self.connection = connection
        self.win = win
        self.win.fill((0, 0, 0))
        print("game created")
        pygame.display.update()

    def draw(self):
        pygame.display.update()

    def blit_paths(self, response):
        for path in response:
            for i in path:
                try:
                    pygame.draw.line(self.win, i[0], i[1], i[2], 3)
                except Exception as e:
                    pass
        self.draw()

    def blit_scores(self, scores):
        self.clearBoard()
        x = 200
        y = 400
        for name, score in enumerate(scores):
            tb = Textblit(f'{name}: {score}', x, y, (100, 100, 100), size=20)
            tb.blitText(self.win)
            x += 30
        self.draw()

    def clearBoard(self):
        self.win.clear()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(40)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
            try:
                wait = self.connection.send({4: []})
                if wait:
                    scores = self.connection.send({1: []})
                    self.blit_scores(scores)

                else:
                    # Make client protocol
                    held = pygame.key.get_pressed()
                    if held[pygame.K_RIGHT] and held[pygame.K_LEFT]:
                        move = "forward"
                    elif held[pygame.K_RIGHT]:
                        move = "right"
                    elif held[pygame.K_LEFT]:
                        move = "left"
                    else:
                        move = "forward"
                    self.connection.send({0: move})

                    drawPackage = self.connection.send({2: []})
                    if drawPackage is not []:
                        self.blit_paths(drawPackage)
                    wipe_board = self.connection.send({3: []})
                    if wipe_board:
                        self.clearBoard()
                        self.draw()

            except:
                run = False
                break

        pygame.quit()
