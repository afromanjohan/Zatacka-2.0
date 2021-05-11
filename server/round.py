class Round():
    def __init__(self, players, game):
        self.players = players
        self.alive_players = players
        self.game = game
        self.should_end_game = False

    def player_dies(self, player):
        if player in self.alive_players:
            points = len(self.players) - len(self.alive_players)
            self.alive_players.remove(player)
            player.update_score(points)
            if player.get_score() > self.game.point_threshold:
                self.should_end_game = True
            if len(self.alive_players) == 1:
                winner = self.alive_players.pop(0)
                winner.update_score(len(self.players))
                if winner.get_score() >= self.game.point_threshold:
                    self.should_end_game = True
                self.end_round()

    def player_left(self, player):
        self.players.remove(player)
        if player in self.alive_players:
            self.alive_players.remove(player)

    def end_round(self):
        if self.should_end_game:
            self.game.end_game()
        self.game.round_ended()
