import random
from game import Game
from numpy import sin, cos, deg2rad


class Player:
    def __init__(self, ip, name, color):
        self.score = 0
        self.alive = True
        self.ip = ip
        self.name = name
        self.color = color
        self.x = None
        self.y = None
        self.direction = None
        self.metronome = random.randint(0, 80)
        self.game = None
        self.steps_per_move = 3
        self.path = None
        self.player_restart()

    def set_game(self, game):
        self.game = game

    def update_score(self, x):
        self.score += x

    def get_pos(self):
        return int(self.x), int(self.y)

    def disconnect(self):
        self.game.player_disconnected(self)

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def player_died(self):
        if self.game:
            if self in self.game.alive_players:
                self.game.alive_players.remove(self)
        self.alive = False

    def player_restart(self):
        self.alive = True
        self.x = random.randint(100, 1000)
        self.y = random.randint(100, 800)
        self.direction = random.randint(0, 360)
        self.path = []

    def make_move(self, move):
        if self.alive:
            degrees = self.direction
            x = self.x
            y = self.y
            self.metronome += 1
            if move == "left":
                degrees -= 3
                calculatedX = self.steps_per_move * cos(deg2rad(degrees))
                calculatedY = self.steps_per_move * sin(deg2rad(degrees))
                self.direction -= 3
            elif move == "right":
                degrees += 3
                calculatedX = self.steps_per_move * cos(deg2rad(degrees))
                calculatedY = self.steps_per_move * sin(deg2rad(degrees))
                self.direction += 3
            else:
                calculatedX = self.steps_per_move * cos(deg2rad(degrees))
                calculatedY = self.steps_per_move * sin(deg2rad(degrees))
            calculatedX = (self.x + calculatedX)
            calculatedY = (self.y + calculatedY)
            self.x = calculatedX
            self.y = calculatedY
            vis = self.metronome % 17 in {1, 2, 3}
            if self.metronome > 100:
                self.metronome = 0
            if vis is False:
                self.path.append((self.color, self.get_pos(), (int(x), int(y))))
            else:
                self.path.append(((0, 0, 0), self.get_pos(), (int(x), int(y))))

            self.game.player_make_move(self, x, y, vis)

            if len(self.path) > 3:
                self.path = self.path[-3:]
