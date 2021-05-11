import socket
import threading
from player import Player
from game import Game
import json
from pygamemisc.color import getNextColor


class Server(object):
    PLAYERS = 2

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, conn, player):
        """
        handles in game communication between clients
        :param conn: connection object
        :param ip: str
        :param name: str
        :return: None
        """
        while True:
            try:
                # Receive request
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                except Exception as e:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send = {p.get_name(): p.get_score() for p in player.game.players}
                            send_msg[-1] = send
                        else:
                            send_msg[-1] = f"Waiting: {len(self.connection_queue)} of {self.PLAYERS} player(s) have connected"

                    if player.game:
                        if key == 0:  # move
                            player.make_move(data["0"])

                        elif key == 1:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[1] = scores

                        elif key == 2:
                            send_msg[2] = player.game.get_draw_package() #draw package
                        elif key == 3:
                            #When to tell players to wipe board
                            send_msg[3] = player.game.wipe_board
                        elif key == 4:
                            send_msg[4] = player.game.wait_for_scoreboard

                send_msg = json.dumps(send_msg)
                conn.sendall(send_msg.encode() + ".".encode())
            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}:", e)
                break

        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(F"[DISCONNECT] {player.name} DISCONNECTED")
        conn.close()

    def handle_queue(self, player):
        """
        adds player to queue and creates new game if enough players
        :param player: Player
        :return: None
        """
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.game_id, self.connection_queue[:])
            for p in game.players:
                p.set_game(game)
            self.game_id += 1
            self.connection_queue = []
            print(f"[GAME] Game {self.game_id - 1} started...")

    def authentication(self, conn, addr):
        """
        authentication here
        :param ip: str
        :return: None
        """
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            print(f'{name} connected')
            if not name:
                raise Exception("No name received")

            conn.sendall("1".encode())
            player = Player(addr, name, getNextColor(len(self.connection_queue))[1])
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(conn, player))
            thread.start()
        except Exception as e:
            print("[2 EXCEPTION]", type(e), e)
            conn.close()

    def connection_thread(self):
        server = "192.168.0.68"
        port = 12000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(1)
        print("Waiting for a connection, Server Started")

        while True:
            conn, addr = s.accept()
            print("[CONNECT] New connection!")

            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.connection_thread)
    thread.start()