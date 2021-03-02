def when_finished():
    print("When you're finished, press q to return to the main menu or press b to return to the previous menu.")
# 'print' of options after a menu option has been exhausted


def show_tournament(tournament):
    print(tournament['name_of_tournament'])
# shows name and date of a specified tournament


def show_one_player(player_object, email):
    print(player_object.read_one_player(email))
# shows the player associated with the specified email address


def show_all_tournament_names_and_dates(list_of_tournaments):
    print('The tournaments currently present in the database are: ')
    for tournament in list_of_tournaments:
        print(tournament['name_of_tournament'])


def show_one_tournament(tournament_object, name_of_tournament):
    print(tournament_object.read_one_tournament(name_of_tournament))
# shows a complete database entry for the specified tournament


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
# shows the aspects of a player than can be modified


def show_main_menu_choices():
    print('Would you like to '
          '\n (1) Generate a report'
          '\n (2) Edit/add players'
          '\n (3) Begin/resume/manage a tournament'
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


def show_list(message, list_to_show):
    if message:
        print(message)
    for item in list_to_show:
        print(item)
# prints specified messages
# prints the specified list item by item


def show_player_manipulation_options():
    print("Would you like to: "
          "\n (1) Edit player rankings"
          "\n (2) Delete a specific player"
          "\n (3) Edit a specific player"
          "\n (4) Add a player or players to the database"
          "\n (5) Return to the main menu"
          "\n Input(number of choice only): ")


def show_tournament_management_options():
    print("Would you like to: "
          "\n (1) Create and start a tournament"
          "\n (2) Resume a tournament that has already begun"
          "\n (3) Delete a tournament from the database"
          "\n (4) Return to the main menu"
          "\n Input(number of choice only): ")


def show_players_in_current_match(tournament, local_player_index_1, local_player_index_2):
    for player in tournament.player_instances:
        if player['local_player_index'] == local_player_index_1:
            print(player)
        if player['local_player_index'] == local_player_index_2:
            print(player)
