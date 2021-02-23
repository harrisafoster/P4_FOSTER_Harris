def show_players(players):
    print('Currently, the saved players in the database are: ')
    for player in players:
        print(player)


def show_one_player(player_object, email):
    print(player_object.read_one_player(email))


def show_all_tournament_names(tournaments):
    for tournament in tournaments:
        print(tournament)


def show_one_tournament(tournament_object, name_of_tournament):
    print(tournament_object.read_one_tournament(name_of_tournament))
