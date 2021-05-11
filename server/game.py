from board import Board
from round import Round
import time


class Game:
    def __init__(self, id, players):
        self.id = id
        self.players = players
        self.board = Board()
        self.round = None
        self.wait_for_scoreboard = False
        self.wipe_board = False
        self.point_threshold = 20
        self.start_new_round()

    def start_new_round(self):
        self.wait_for_scoreboard = True
        time.sleep(4)
        self.wait_for_scoreboard = False
        self.wipe_board = True
        time.sleep(1)
        self.wipe_board = False
        try:
            self.round = Round(self.players, self)
            self.board.clear_board()
            for p in self.players:
                p.player_restart()
        except Exception as e:
            self.end_game()

    def player_make_move(self, player, x, y, vis):
        self.board.draw_move(player, x, y, vis, self.round)

    def player_disconnected(self, player):
        if player in self.players:
            self.players.remove(player)
        else:
            raise Exception("Player not in game")
        if len(self.players) < 2:
            self.end_game()

    def get_player_scores(self):
        return [(player.name, player.get_score()) for player in self.players]

    def end_game(self):
        print(f'[Game] game {self.id} ended')
        for player in self.players:
            player.game = None

    def get_draw_package(self):
        return [player.path for player in self.players]

    def round_ended(self):
        self.start_new_round()
