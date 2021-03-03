from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
import views
import datetime


def get_new_player_data():
    print("Enter the new player's information below: ")
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
    return email
# Gets player data from the user, creates a new player in the database.


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
    views.show_list('Players currently in the database are: ', Player('players.json').read_player_list())
    clear_player_database = input('Would you like to clear the player database? (y/n) ')
    if clear_player_database == 'y':
        Player('players.json').delete_all_players()
    players_to_add = input('Would you like to add any players to the database? (y/n) ')
    player_emails = []
    if players_to_add == 'y':
        while True:
            number_of_players_to_add = input('How many players would you like to add? (numbers only)')
            try:
                int(number_of_players_to_add)
            except ValueError:
                print('Please enter only whole numbers. ')
                continue
            else:
                number_of_players_to_add = int(number_of_players_to_add)
                break
        for x in range(int(number_of_players_to_add)):
            player_emails.append(get_new_player_data())
    print('Please enter the email addresses of the players that are participating in this tournament.')
    while len(player_emails) < nb_players:
        while True:
            try:
                email = input("Enter player's email address: ")
                assert '@' in email
            except AssertionError:
                print('Please enter a valid email address.')
                continue
            if email in player_emails:
                print('You have already added this user to the tournament.')
                continue
            if email not in Player('players.json').get_player_emails():
                add_new_player = input('This email address matches no saved users, '
                                       'add a new user with this email? (y/n): ')
                if add_new_player == 'y':
                    get_new_player_data()
                    player_emails.append(
                        Player('players.json').read_one_player(email)[0]['email'])
                continue
            else:
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
# Gets tournament data from the user, creates a new tournament in the database.


def start_round(current_tournament, round_number):
    while True:
        try:
            start_of_round = str(input('Press y to start the round: '))
            assert start_of_round == 'y'
        except AssertionError:
            print('Please press the indicated key to start the round.')
        else:
            current_round = Round('tournaments.json').create_round(
                round_number, current_tournament)
            return current_round
# Asks the user to confirm the start of the round, generates a round object (start_time auto-generated).


def end_round(current_tournament, current_round, round_number):
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
            current_tournament.round_instances[round_number-1] = current_round.serialize_round()
            current_tournament.update_round_instances()
            current_tournament.nb_finished_matches_of_round = 0
            current_tournament.save_nb_finished_matches_of_round()
            print('Round ' + str(round_number) + ' ended: ' + current_round.end_of_round)
            break
# Asks the user to confirm the end of the round, gets total duration,
# completes round object with new info, updates database


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
# Asks the user to confirm the end of the match, gets total duration,
# completes match object with new info, updates database


def point_counter(current_tournament, round_number):
    if len(current_tournament.round_instances) < round_number:
        current_round = start_round(current_tournament, round_number)
        current_tournament.round_instances += [current_round.serialize_round()]
        current_tournament.update_round_instances()
    if not current_tournament.round_instances:
        current_round = start_round(current_tournament, round_number)
    elif current_tournament.round_instances[round_number-1]:
        current_round = Round('tournaments.json').access_round_object(round_number, current_tournament)
    match_number = current_tournament.nb_finished_matches_of_round
    current_round_matches = current_tournament.round_descriptions[round_number - 1][match_number:]
    for match in current_round_matches:
        views.show_players_in_current_match(current_tournament, match[0], match[1])
        proceed = input('(1) Declare winner or '
                        '\n(2) Save & quit tournament?'
                        '\n Input: ')
        if proceed == '2':
            if not current_tournament.round_instances:
                current_tournament.round_instances += [current_round.serialize_round()]
                current_tournament.update_round_instances()
            elif current_tournament.round_instances[round_number-1]:
                current_tournament.round_instances[round_number-1] = current_round.serialize_round()
                current_tournament.update_round_instances()
            else:
                current_tournament.round_instances += [current_round.serialize_round()]
                current_tournament.update_round_instances()
            main_menu()
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
        current_tournament.nb_finished_matches_of_round = match_number
        current_tournament.save_nb_finished_matches_of_round()
        current_tournament.update_player_instances(current_tournament.player_instances)
    end_round(current_tournament, current_round, round_number)
# Asks user for the winner of each match for specified round,
# manages/generates match/round objects,
# updates database/objects with new info.


def local_player_report_by_last_name(chosen_tournament):
    views.show_list('Players sorted by last name', chosen_tournament.sort_players_by_last_name())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()
# generates a report on all players of specified tournament sorted by last name


def local_player_report_by_relative_ranking(chosen_tournament):
    views.show_list('Players sorted by rank: ', chosen_tournament.sort_players_by_local_index())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()
# generates a report on all players of specified tournament sorted by ranking
# (relative ranking refers to the player's local index numbers)


def local_player_report_by_points(chosen_tournament):
    views.show_list('Players sorted by points: ', chosen_tournament.sort_players_by_points_descending())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()
# generates a report on all players of specified tournament
# sorted by final point count


def local_round_report(chosen_tournament):
    views.show_list('All rounds: ', Round('tournaments.json').read_all_rounds(chosen_tournament))
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()
# generates a report on all rounds of the specified tournament


def local_match_report(chosen_tournament):
    views.show_list('All matches: ', Match('tournaments.json').read_all_matches(chosen_tournament))
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_local_reports()
# generates a report on all matches of the specified tournament


def choose_and_access_tournament_for_report():
    views.show_all_tournament_names_and_dates(Tournament('tournaments.json').read_all_tournaments())
    if len(Tournament('tournaments.json').read_all_tournaments()) == 0:
        print("There are no currently saved tournaments.")
        views.when_finished()
        all_done = input()
        if all_done:
            main_menu()
    else:
        while True:
            choice = input(
                'On which tournament would you like a report? (name and date only, format: Name yyyy-mm-dd)')
            try:
                assert choice in Tournament('tournaments.json').get_tournament_names()
            except AssertionError:
                print("Sorry, you need to choose one of the available options.")
                continue
            else:
                break
        chosen_tournament = Tournament('tournaments.json').access_tournament_object(choice)
    return chosen_tournament
# shows available tournaments,
# asks user to select one of the available options,
# returns accessed tournament object.


def report_menu_local_reports():
    chosen_tournament = choose_and_access_tournament_for_report()
    while True:
        views.show_local_tournament_report_options()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if int(choice) not in range(8) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        local_player_report_by_last_name(chosen_tournament)
    if choice == 2:
        local_player_report_by_relative_ranking(chosen_tournament)
    if choice == 3:
        local_player_report_by_points(chosen_tournament)
    if choice == 4:
        local_round_report(chosen_tournament)
    if choice == 5:
        local_match_report(chosen_tournament)
    if choice == 6:
        main_menu()
    if choice == 7:
        main_report_menu()
# menu function for reports on specific tournaments


def global_report_players_by_last_name():
    views.show_list('Players sorted by last name', Player('players.json').sort_all_players_by_last_name())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        global_players_report_options()
# generates a report on all saved players sorted by last name


def global_report_players_by_ranking():
    views.show_list('Players by ranking: ', Player('players.json').sort_all_players_by_ranking())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        global_players_report_options()
# generates a report on all saved players sorted by ranking


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
# menu function for reports on all players currently present in database


def report_all_tournaments():
    for tournament in Tournament('tournaments.json').db_tournaments.all():
        views.show_tournament(tournament)
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        report_menu_global_reports()
# generates a report on all saved tournaments (prints names and dates)


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
# menu function for all global reports


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
# main menu function for reports


def add_players():
    players_to_add = input('Would you like to add any players to the database? (y/n)')
    if players_to_add == 'y':
        while True:
            number_of_players_to_add = input('How many players would you like to add? (numbers only)')
            try:
                int(number_of_players_to_add)
            except ValueError:
                print('Please enter only whole numbers. ')
                continue
            else:
                number_of_players_to_add = int(number_of_players_to_add)
                break
        for x in range(int(number_of_players_to_add)):
            get_new_player_data()
        views.when_finished()
        all_done = input()
        if all_done == 'q':
            main_menu()
        else:
            player_manipulation_menu()
    if players_to_add != 'y' or not players_to_add:
        player_manipulation_menu()
# Requests confirmation from user of add action,
# requests number to add from user
# Gets data for all new players from user,
# adds the new players to the database


def update_player():
    if len(Player('players.json').db_players.all()) > 0:
        player_email_addresses = Player('players.json').get_player_emails()
        views.show_list(None, Player('players.json').read_player_list())
        while True:
            email = input("Which player would you like to edit? "
                          "(enter the player's email address "
                          "to access the correct player instance.) ")
            try:
                assert email in player_email_addresses
            except AssertionError:
                print('Sorry, you need to enter an email address '
                      'that is currently present in the database.')
                views.show_list(None, Player('players.json').read_player_list())
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
        print('Player edited successfully.')
    else:
        print("There aren't any players saved in the database.")
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        player_manipulation_menu()
# menu for selecting a player and editing the desired fields of said player
# updates database with new info


def delete_player():
    while True:
        choice = str(input('Which player would you like to delete? (email address only)'))
        try:
            assert choice in Player('players.json').get_player_emails()
        except AssertionError:
            print('Please enter an email address that is present in the database')
            continue
        else:
            Player('players.json').delete_player(choice)
            break
    print('Player deleted. ')
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        player_manipulation_menu()
# menu for selecting a player and deleting said player
# updates database with new info


def update_all_rankings():
    for item in Player('players.json').read_player_list():
        print(item)
        while True:
            new_ranking = input("What is the player's new ranking? (numbers only)")
            try:
                int(new_ranking)
            except ValueError:
                print('Please enter whole numbers only ')
                continue
            else:
                new_ranking = int(new_ranking)
                break
        Player('players.json').db_players.update({'ranking': new_ranking},
                                                 Player('players.json').query["email"] == item['email'])
    views.show_list('New list of all players sorted by rank: ',
                    Player('players.json').sort_all_players_by_ranking())
    views.when_finished()
    all_done = input()
    if all_done == 'q':
        main_menu()
    else:
        player_manipulation_menu()
# updates all player rankings in the global database with user inputs


def player_manipulation_menu():
    views.show_list("Currently, the players saved in the database are: ",
                    Player('players.json').read_player_list())
    while True:
        views.show_player_manipulation_options()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if int(choice) not in range(6) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        update_all_rankings()
    if choice == 2:
        delete_player()
    if choice == 3:
        update_player()
    if choice == 4:
        add_players()
    if choice == 5:
        main_menu()
# menu used for manipulating player objects and database instances


def continue_tournament():
    available_options = [1, 2]
    while True:
        user_input = int(input("Would you like to: "
                               "\n (1) Proceed with the tournament"
                               "\n (2) Save your progress?"))
        try:
            assert user_input in available_options
        except AssertionError:
            print('Please enter a valid option choice')
            continue
        else:
            break
    if user_input == 1:
        return True
    if user_input == 2:
        return False
# function used to save progress
# and pause the tournament to continue at a later time/date


def execute_tournament(tournament):
    if tournament.done:
        print('This tournament has already ended.')
        pass
    views.show_list('Players present in this tournament are (local index numbers used for pairings): ',
                    tournament.player_instances)
    if not tournament.done:
        if not tournament.round_descriptions:
            tournament.generate_round_1_matches()
        while True:
            if len(tournament.round_descriptions) < tournament.nb_rounds:
                if not continue_tournament():
                    break
                views.show_list("Round " + str(len(tournament.round_descriptions))
                                + "'s matches are (by local index numbers): ",
                                tournament.round_descriptions[len(tournament.round_descriptions) - 1])
                point_counter(tournament, len(tournament.round_descriptions))
                tournament.swiss_method_pairing()
            if len(tournament.round_descriptions) == tournament.nb_rounds:
                if not continue_tournament():
                    break
                views.show_list("Round " + str(len(tournament.round_descriptions))
                                + "'s matches are (by local index numbers): ",
                                tournament.round_descriptions[len(tournament.round_descriptions) - 1])
                point_counter(tournament, len(tournament.round_descriptions))
                tournament.done = True
                tournament.end_date = str(datetime.date.today())
                tournament.update_end_date()
                tournament.update_done_status()
                print('This tournament has ended.')
                break
# runs the specified tournament from its current state until its end
# unless the user elects to save progress.


def delete_tournament():
    proceed = input('Proceed with deleting a tournament? (y/n): ')
    if proceed == 'y':
        views.show_all_tournament_names_and_dates(Tournament('tournaments.json').db_tournaments.all())
        if len(Tournament('tournaments.json').db_tournaments.all()) == 0:
            print("There are no currently saved tournaments.")
            views.when_finished()
            all_done = input()
            if all_done == 'q':
                main_menu()
            else:
                tournament_management_menu()
        else:
            while True:
                choice = input(
                    'Which tournament would you like to resume? '
                    '(name and date only, format: Name yyyy-mm-dd)')
                try:
                    assert choice in Tournament('tournaments.json').get_tournament_names()
                except AssertionError:
                    print("Sorry, you need to choose one of the available options.")
                    continue
                else:
                    break
            Tournament('tournaments.json').delete_tournament(choice)
            print('Tournament ' + choice + ' deleted.')
            views.when_finished()
            all_done = input()
            if all_done == 'q':
                main_menu()
            else:
                tournament_management_menu()
    if proceed != 'y':
        tournament_management_menu()


def resume_tournament():
    proceed = input('Proceed with resuming a tournament? (y/n): ')
    if proceed == 'y':
        views.show_all_tournament_names_and_dates(Tournament('tournaments.json').db_tournaments.all())
        if len(Tournament('tournaments.json').db_tournaments.all()) == 0:
            print("There are no currently saved tournaments.")
            views.when_finished()
            all_done = input()
            if all_done == 'q':
                main_menu()
            else:
                tournament_management_menu()
        else:
            while True:
                choice = input(
                    'Which tournament would you like to resume? '
                    '(name and date only, format: Name yyyy-mm-dd)')
                try:
                    assert choice in Tournament('tournaments.json').get_tournament_names()
                except AssertionError:
                    print("Sorry, you need to choose one of the available options.")
                    continue
                else:
                    break
            current_tournament = Tournament('tournaments.json').access_tournament_object(choice)
            execute_tournament(current_tournament)
            views.when_finished()
            all_done = input()
            if all_done == 'q':
                main_menu()
            else:
                tournament_management_menu()
    if proceed != 'y':
        tournament_management_menu()
# user selects a tournament to resume from available options
# tournament is resumed and run


def create_and_start_tournament():
    proceed = input('Proceed with creating and starting a tournament? (y/n): ')
    if proceed == 'y':
        current_tournament = Tournament('tournaments.json').access_tournament_object(get_new_tournament_data())
        execute_tournament(current_tournament)
        views.when_finished()
        all_done = input()
        if all_done == 'q':
            main_menu()
        else:
            tournament_management_menu()
    if proceed != 'y':
        tournament_management_menu()
# user creates a new tournament and enters all its data
# new tournament is run until its end or until the user elects to save progress


def tournament_management_menu():
    while True:
        views.show_tournament_management_options()
        choice = input()
        try:
            int(choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if int(choice) not in range(5) or int(choice) == 0:
            print("Sorry, you need to select one of the available options.")
            continue
        else:
            choice = int(choice)
            break
    if choice == 1:
        create_and_start_tournament()
    if choice == 2:
        resume_tournament()
    if choice == 3:
        delete_tournament()
    if choice == 4:
        main_menu()
# main menu for creating/selecting/deleting/resuming tournaments


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
    if choice == 2:
        player_manipulation_menu()
    if choice == 3:
        tournament_management_menu()
    if choice == 4:
        exit(0)
# main menu for whole program
