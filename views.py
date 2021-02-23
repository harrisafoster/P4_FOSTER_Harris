

def show_players(players):
    for player in players:
        print(player)


def show_one_player(player_object, email):
    print(player_object.read_one_player(email))
