def when_finished():
    print("When you're finished, press q to return to the main menu or press b to return to the previous menu.")


def show_tournament(tournament):
    print(tournament['name_of_tournament'])


def show_players(players):
    print('Currently, the saved players in the database are: ')
    for player in players:
        print(player)


def show_one_player(player_object, email):
    print(player_object.read_one_player(email))


def show_all_tournament_names_and_dates(list_of_tournaments):
    for tournament in list_of_tournaments:
        print(tournament['name_of_tournament'] + ' ' + tournament['start_date'])


def show_one_tournament(tournament_object, name_of_tournament):
    print(tournament_object.read_one_tournament(name_of_tournament))


def show_modifiable_fields():
    print("Which fields would you like to edit?"
          "\n (1) last_name "
          "\n (2) first_name "
          "\n (3) date_of_birth "
          "\n (4) sex "
          "\n (5) ranking"
          "\n (6) email"
          "\n Enter only the numerical values of the fields "
          "that you would like to edit. (ex. 1 2 3)"
          "\n Input:  ")


def show_main_menu_choices():
    print('Would you like to '
          '\n (1) Generate a report'
          '\n (2) Edit/add players'
          '\n (3) Begin/resume a tournament'
          '\n (4) Exit this program'
          '\n Input(number of choice only): ')


def show_main_report_menu_choices():
    print("Would you like to generate a "
          "\n (1) Global report (all tournaments/players)"
          "\n (2) Local report (within a specific tournament)"
          "\n (3) Return to the main menu"
          "\n Input(number of choice only): ")


def show_global_report_options():
    print("Would you like "
          "\n (1) a report on all players "
          "\n (2) a list of all tournaments "
          "\n (3) to return to main menu"
          "\n (4) to return to the previous menu"
          "\n Input(number of choice only): ")


def show_global_players_report_options():
    print("Would you like "
          "\n (1) an alphabetical list of all players"
          "\n (2) a list of all players by rank order"
          "\n (3) return to main menu"
          "\n (4) return to the previous menu"
          "\n Input(number of choice only): ")


def show_local_tournament_report_options():
    print("From this tournament would you like: "
          "\n (1) A list of the players by alphabetical order"
          "\n (2) A list of the players by rank order"
          "\n (3) A list of the players by final point count"
          "\n (4) A list of all of the rounds of this tournament"
          "\n (5) A list of all of the matches played in this tournament"
          "\n (6) To return to the main menu"
          "\n (7) To return to the previous menu"
          "\n Input(number choice only): ")


def show_list(list_to_show):
    for item in list_to_show:
        print(item)
