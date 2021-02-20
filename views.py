from player import Player


def show_players():
    for player in Player.read_player_list():
        print(player)


def show_one_player(email):
    print(Player.read_one_player(email))
