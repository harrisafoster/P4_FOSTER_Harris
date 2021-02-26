from player import Player
from tournament import Tournament
from round import Round
from match import Match
import views
import datetime


def get_new_player_data():
    while True:
        email = input("Enter player's email address: ")
        try:
            assert '@' in email
        except AssertionError:
            print('Please enter a valid email address.')
            continue
        if email in Player('players.json').get_player_emails():
            print('This email is already assigned to another user.')
            continue
        else:
            break
    last_name = input("Enter last name: ").upper()
    first_name = input("Enter first name: ").capitalize()
    date_of_birth = input("Enter date of birth (format dd/mm/yyyy): ")
    sex = input("Enter sex of player: ")
    while True:
        ranking = input("Enter ranking of participant: ")
        try:
            int(ranking)
        except ValueError:
            print('Please enter only numerical values. ')
            continue
        else:
            ranking = int(ranking)
            break
    Player('players.json').create_player(email, last_name, first_name, date_of_birth, sex, ranking)


def update_player_data():
    if len(Player('players.json').db_players.all()) > 0:
        player_email_addresses = Player('players.json').get_player_emails()
        views.show_players(Player('players.json').read_player_list())
        while True:
            email = input("Which player would you like to edit? "
                          "(enter the player's email address to access the correct player instance.) ")
            try:
                assert email in player_email_addresses
            except AssertionError:
                print('Sorry, you need to enter an email address that is currently present in the database.')
                views.show_players(Player('players.json').read_player_list())
                continue
            else:
                views.show_one_player(Player('players.json'), email)
                break
        views.show_modifiable_fields()
        fields_to_edit = input()
        if '1' in fields_to_edit:
            last_name = input("Enter the player's modified last name: ").upper()
        else:
            last_name = None
        if '2' in fields_to_edit:
            first_name = input("Enter the player's modified first name: ").capitalize()
        else:
            first_name = None
        if '3' in fields_to_edit:
            date_of_birth = input("Enter the player's modified date of birth (format dd/mm/yyyy): ")
        else:
            date_of_birth = None
        if '4' in fields_to_edit:
            sex = input("Enter the player's modified sex: ")
        else:
            sex = None
        if '5' in fields_to_edit:
            ranking = input("Enter the player's modified ranking: ")
        else:
            ranking = None
        if '6' in fields_to_edit:
            new_email = input("Enter the player's modified email address: ")
        else:
            new_email = None
        Player('players.json').update_player(email, last_name, first_name, date_of_birth, sex, ranking, new_email)
    else:
        print("There aren't any players saved in the database.")


def update_player_rankings():
    views.show_players(Player('players.json').read_player_list())
    confirm = input("Would you like to update all player rankings? (y/n) ")
    if confirm == 'y':
        for player in Player('players.json').db_players.all():
            views.show_one_player(Player('players.json'), player['email'])
            while True:
                try:
                    new_ranking = int(input("Enter the player's new ranking: "))
                except ValueError:
                    print('Please enter only numerical values. ')
                    continue
                else:
                    Player('players.json').update_ranking(player['email'], new_ranking)
                    break


def remove_player():
    if len(Player('players.json').db_players.all()) > 0:
        player_email_addresses = Player('players.json').get_player_emails()
        views.show_players(Player('players.json').read_player_list())
        while True:
            try:
                email = input("Which player would you like to delete? "
                              "(enter the player's email address to access the correct player instance.) ")
                assert email in player_email_addresses
            except AssertionError:
                print('Sorry, you need to enter an email address that is currently present in the database.')
                views.show_players(Player('players.json').read_player_list())
                continue
            else:
                Player('players.json').delete_player(email)
                break
    else:
        print("There aren't any players saved in the database.")


def get_new_tournament_data():
    name_of_tournament = str(input('Enter name of tournament: ') + ' ' + str(datetime.date.today()))
    location = input('Enter location of tournament: ')
    while True:
        try:
            nb_rounds = int(input('Enter number of rounds (default set to 4): '))
        except ValueError:
            print('Set to default round count (4)')
            nb_rounds = 4
            break
        else:
            break
    while True:
        nb_players = input('Enter how many players are playing in this tournament: ')
        try:
            int(nb_players)
        except ValueError:
            print('Please enter only whole number values. ')
            continue
        else:
            nb_players = int(nb_players)
            break
    views.show_players(Player('players.json').read_player_list())
    player_emails = []
    counter = 1
    while len(player_emails) < nb_players:
        while True:
            try:
                email = input("Enter player " + str(counter) + "'s " + "email address: ")
                assert '@' in email
            except AssertionError:
                print('Please enter a valid email address.')
                continue
            if email in player_emails:
                print('You have already added this user to the tournament.')
                continue
            if email not in Player('players.json').get_player_emails():
                add_new_player = input('This email address matches no saved users, add a new user with this email? ('
                                       'y/n): ')
                if add_new_player == 'y':
                    get_new_player_data()
                    player_emails.append(Player('players.json').read_one_player(email)[0]['email'])
                    counter += 1
                continue
            else:
                counter += 1
                player_emails.append(email)
                break
    while True:
        time_ctrl = input("Type of time control (Bullet, Blitz, ou Coup Rapide): ")
        try:
            assert time_ctrl in ["Bullet", "Blitz", "Coup Rapide"]
        except AssertionError:
            print("Please select one of the available options.")
            continue
        else:
            break
    description = input('Enter the description of the tournament: ')
    Tournament('tournaments.json').create_tournament(name_of_tournament, location, nb_rounds,
                                                     player_emails, time_ctrl, description)
    current_tournament = Tournament('tournaments.json').access_tournament_object(name_of_tournament)
    current_tournament.populate_player_instances()
    return current_tournament.name_of_tournament


def start_round(current_tournament, round_number):
    while True:
        try:
            start_of_round = str(input('Press y to start the round: '))
            assert start_of_round == 'y'
        except AssertionError:
            print('Please press the indicated key to start the round.')
        else:
            current_round = Round('tournaments.json').create_round(round_number, current_tournament)
            return current_round


def end_round(current_tournament, current_round):
    while True:
        try:
            end_current_round = str(input('Press y to end the round: '))
            assert end_current_round == 'y'
        except AssertionError:
            print('Please press the indicated key to end the round.')
        else:
            while True:
                duration = input('How long did the round last? (number of hours only in decimal form, ex. 1.5)')
                try:
                    float(duration)
                except ValueError:
                    print('Please enter a valid number.')
                    continue
                else:
                    duration = float(duration)
                    break
            end_of_round = current_round.start_of_round + datetime.timedelta(hours=duration)
            current_round.end_of_round = end_of_round.strftime("%H:%M:%S")
            current_round.start_of_round = current_round.start_of_round.strftime("%H:%M:%S")
            current_tournament.round_instances += [current_round.serialize_round()]
            current_tournament.update_round_instances()
            print('Current round ended: ' + current_round.end_of_round)
            break


def end_match(current_tournament, current_round, current_match):
    while True:
        try:
            end_current_match = str(input('Press y to enter the match duration: '))
            assert end_current_match == 'y'
        except AssertionError:
            print('Please press the indicated key to enter the match duration. ')
        else:
            while True:
                duration = input('How long did the match last? (number of hours only in decimal form, ex. 1.5)')
                try:
                    float(duration)
                except ValueError:
                    print('Please enter a valid number.')
                    continue
                else:
                    duration = float(duration)
                    break
            end_of_match = current_round.start_of_round + datetime.timedelta(hours=duration)
            current_match.end_of_match = end_of_match.strftime("%H:%M:%S")
            current_match.start_of_match = current_round.start_of_round.strftime("%H:%M:%S")
            current_tournament.match_instances += [current_match.serialize_match()]
            current_tournament.update_match_instances()
            print('Current match ended: ' + current_match.end_of_match)
            break


def point_counter(current_tournament, round_number):
    current_round = start_round(current_tournament, round_number)
    current_round_matches = current_tournament.round_descriptions[round_number - 1]
    match_number = 0
    for match in current_round_matches:
        while True:
            winner = input(f"Winner? Player {match[0]} or Player {match[1]}, or Draw: ")
            try:
                assert winner in [str(match[0]), str(match[1]), 'Draw', 'draw']
            except AssertionError:
                print('Please select one of the available options.')
                continue
            else:
                break
        while True:
            try:
                winner.capitalize()
            except AttributeError:
                break
            else:
                if winner.capitalize() == 'Draw':
                    for player_instance in current_tournament.player_instances:
                        if player_instance['local_player_index'] == match[0]:
                            player_instance['points'] += 0.5
                        if player_instance['local_player_index'] == match[1]:
                            player_instance['points'] += 0.5
                break
        while True:
            try:
                int(winner)
            except ValueError:
                break
            else:
                if int(winner) == match[0]:
                    for player_instance in current_tournament.player_instances:
                        if player_instance['local_player_index'] == match[0]:
                            player_instance['points'] += 1
                if int(winner) == match[1]:
                    for player_instance in current_tournament.player_instances:
                        if player_instance['local_player_index'] == match[1]:
                            player_instance['points'] += 1
                break
        match_number += 1
        current_match = Match('tournaments.json').create_match(round_number, match_number, winner, current_round)
        end_match(current_tournament, current_round, current_match)
    end_round(current_tournament, current_round)
    current_tournament.update_player_instances(current_tournament.player_instances)


def local_player_report_by_last_name(chosen_tournament):
    views.show_list(chosen_tournament.sort_players_by_last_name())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()


def local_player_report_by_relative_ranking(chosen_tournament):
    views.show_list(chosen_tournament.sort_players_by_local_index())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()


def local_player_report_by_points(chosen_tournament):
    views.show_list(chosen_tournament.sort_players_by_points_descending())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()


def local_round_report(chosen_tournament):
    views.show_list(Round('tournaments.json').read_all_rounds(chosen_tournament))
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()


def local_match_report(chosen_tournament):
    views.show_list(Match('tournaments.json').read_all_matches(chosen_tournament))
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()


def report_menu_local_reports():
    views.show_all_tournament_names_and_dates(Tournament('tournaments.json').read_all_tournaments())
    if len(Tournament('tournaments.json').read_all_tournaments()) == 0:
        print("There are no currently saved tournaments.")
        views.when_finished()
        all_done = input()
        if all_done:
            main_menu()
    else:
        while True:
            choice = input('On which tournament would you like a report? (name and date only, format: Name yyyy-mm-dd)')
            try:
                assert choice in Tournament('tournaments.json').get_tournament_names()
            except AssertionError:
                print("Sorry, you need to choose one of the available options.")
                continue
            else:
                break
        chosen_tournament = Tournament('tournaments.json').access_tournament_object(choice)
        while True:
            views.show_local_tournament_report_options()
            sub_choice = input()
            try:
                int(sub_choice)
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            if int(sub_choice) not in range(8) or int(sub_choice) == 0:
                print("Sorry, you need to select one of the available options.")
                continue
            else:
                sub_choice = int(sub_choice)
                break
    if sub_choice == 1:
        local_player_report_by_last_name(chosen_tournament)
    if sub_choice == 2:
        local_player_report_by_relative_ranking(chosen_tournament)
    if sub_choice == 3:
        local_player_report_by_points(chosen_tournament)
    if sub_choice == 4:
        local_round_report(chosen_tournament)
    if sub_choice == 5:
        local_match_report(chosen_tournament)
    if sub_choice == 6:
        main_menu()
    if sub_choice == 7:
        main_report_menu()


def global_report_players_by_last_name():
    views.show_list(Player('players.json').sort_all_players_by_last_name())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        global_players_report_options()


def global_report_players_by_ranking():
    views.show_list(Player('players.json').sort_all_players_by_ranking())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        global_players_report_options()


def global_players_report_options():
    while True:
        views.show_global_players_report_options()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
        if int(choice) not in range(5) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        global_report_players_by_last_name()
    if choice == 2:
        global_report_players_by_ranking()
    if choice == 3:
        main_menu()
    if choice == 4:
        report_menu_global_reports()


def report_all_tournaments():
    for tournament in Tournament('tournaments.json').db_tournaments.all():
        views.show_tournament(tournament)
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_global_reports()


def report_menu_global_reports():
    while True:
        views.show_global_report_options()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
        if int(choice) not in range(5) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        global_players_report_options()
    if choice == 2:
        report_all_tournaments()
    if choice == 3:
        main_menu()
    if choice == 4:
        main_report_menu()


def main_report_menu():
    while True:
        views.show_main_report_menu_choices()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")

        if int(choice) not in range(4) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        report_menu_global_reports()
    if choice == 2:
        report_menu_local_reports()
    if choice == 3:
        main_menu()


'''def menu_2_4():
    players_to_add = input('Would you like to add any players to the database? (y/n)')
    if players_to_add == 'y':
        number_to_add = input('How many players would you like to add? (numbers only)')
        for x in range(int(number_to_add)):
            Player.add_player(None)
        all_done = input(
            "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
        if all_done == 'q':
            main_menu()
        else:
            menu_2()
    if players_to_add == 'n' or not players_to_add:
        main_menu()


def menu_2_3():
    Player.edit_player()
    all_done = input(
        "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
    if all_done == 'q':
        main_menu()
    else:
        menu_2()


def menu_2_2():
    Player.remove_player()
    all_done = input(
        "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
    if all_done == 'q':
        main_menu()
    else:
        menu_2()


def menu_2_1():
    query = Query()
    for item in Player.db_players:
        print(item)
        new_ranking = input("What is the player's new ranking? (numbers only)")
        Player.db_players.update({'Ranking': new_ranking}, query["Player ID"] == item['Player ID'])
        players = Player.db_players.all()
        players.sort(key=operator.itemgetter('Ranking'))
        print('New list of all players sorted by rank: ')
        for player in players:
            print(player)
        all_done = input(
            "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
        if all_done == 'q':
            main_menu()
        else:
            menu_2()


def menu_2():
    print("Currently, the players saved in the database are: ")
    for item in Player.db_players.all():
        print(item)
    while True:
        try:
            sub_choice = int(input("Would you like to: "
                                   "\n (1) Edit player rankings"
                                   "\n (2) Remove a specific player"
                                   "\n (3) Edit a specific player"
                                   "\n (4) Add a player or players to the database"
                                   "\n (5) Return to the main menu"
                                   "\n Input(number of choice only): "))
        except ValueError:
            print("Sorry, I didn't understand that.")

        if sub_choice not in range(6) or sub_choice == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            break
    if sub_choice == 1:
        menu_2_1()
    if sub_choice == 2:
        menu_2_2()
    if sub_choice == 3:
        menu_2_3()
    if sub_choice == 4:
        menu_2_4()
    if sub_choice == 5:
        main_menu()


def menu_3_2():
    proceed = input('Proceed with resuming a tournament? (y/n): ')
    if proceed == 'y':
        tournament_names = []
        for item in Tournament.all_tournaments:
            tournament_names.append(item['Name of tournament: '])
        if len(tournament_names) == 0:
            print("There are no currently saved tournaments.")
            all_done = input(
                "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
            if all_done == 'q':
                main_menu()
            else:
                menu_3()
        else:
            resume_tournament()
            all_done = input(
                "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
            if all_done == 'q':
                main_menu()
            else:
                menu_3()
    if proceed != 'y':
        menu_3()


def menu_3_1():
    proceed = input('Proceed with creating and starting a tournament? (y/n): ')
    if proceed == 'y':
        create_and_start_tournament()
        all_done = input(
            "When you're finished, press q to return to the main menu or press b to return to the previous menu.")
        if all_done == 'q':
            main_menu()
        else:
            menu_3()
    if proceed != 'y':
        menu_3()


def menu_3():
    while True:
        try:
            sub_choice = int(input("Would you like to: "
                                   "\n (1) Create and start a tournament"
                                   "\n (2) Resume a tournament that has already begun"
                                   "\n (3) Return to the main menu"
                                   "\n Input(number of choice only): "))
        except ValueError:
            print("Sorry, I didn't understand that.")

        if sub_choice not in range(4) or sub_choice == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            break
    if sub_choice == 1:
        menu_3_1()
    if sub_choice == 2:
        menu_3_2()
    if sub_choice == 3:
        main_menu()'''


def main_menu():
    while True:
        views.show_main_menu_choices()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")

        if int(choice) not in range(5) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        main_report_menu()
    '''if choice == 2:
        menu_2()
    if choice == 3:
        menu_3()
    if choice == 4:
        exit(0)'''


# TODO Testes ci-dessous, algo fonctionne

'''current_tournament = Tournament('tournaments.json').access_tournament_object(get_new_tournament_data())

current_tournament.generate_round_1_matches()
point_counter(current_tournament, 1)
print('End of round 1. ')
current_tournament.swiss_method_pairing()
point_counter(current_tournament, 2)
print('End of round 2. ')
current_tournament.swiss_method_pairing()
point_counter(current_tournament, 3)
print('End of round 3. ')
current_tournament.swiss_method_pairing()
point_counter(current_tournament, 4)
print('End of round 4. ')'''

main_menu()
