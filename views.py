from player import Player


def show_players():
    player_object = Player('players.json')
    for player in player_object.read_player_list():
        print(player)


def show_one_player(email):
    player_object = Player('players.json')
    print(player_object.read_one_player(email))
