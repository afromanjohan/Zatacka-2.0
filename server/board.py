import pygame


class Board:
    def __init__(self):
        self.WIDTH = 1300
        self.HEIGHT = 1000
        self.board = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.board.fill((0, 0, 0))

    def draw_move(self, player, x, y, vis, rnd):
        (posx, posy) = player.get_pos()
        posx = int(posx)
        posy = int(posy)
        value = self.board.get_at((posx, posy))[0:3]
        color = (0, 0, 0)
        if vis is True:
            color = player.color
            try:
                pygame.draw.line(self.board, color, (int(x), int(y)), (posx, posy), 3)
            except Exception as e:
                # Might possibly catch index out of bounds exceptions on the edge of the board
                print(e)
        if value != (0, 0, 0) or self.out_of_bounds(player.get_pos()):
            rnd.player_dies(player)
            # player.player_died()  # fails here

    def clear_board(self):
        self.board.fill((0, 0, 0))

    def get_board(self):
        return self.board

    def out_of_bounds(self, pos):
        if 0 < pos[0] < self.WIDTH and 0 < pos[1] < self.HEIGHT:
            return False
        return True
