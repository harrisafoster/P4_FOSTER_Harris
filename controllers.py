from player import Player
from tournament import Tournament
import views
import datetime
import operator
import itertools


def generate_tournament_object():
    tournament_object = Tournament('tournaments.json')
    return tournament_object


def access_tournament_object(name_of_tournament):
    tournament_object = generate_tournament_object()
    tournament_instance = tournament_object.db_tournaments.search(tournament_object.query['name_of_tournament'] ==
                                                                  name_of_tournament)
    tournament_object.name_of_tournament = tournament_instance[0]['name_of_tournament']
    tournament_object.location = tournament_instance[0]['location']
    tournament_object.start_date = tournament_instance[0]['start_date']
    tournament_object.end_date = tournament_instance[0]['end_date']
    tournament_object.nb_rounds = tournament_instance[0]['nb_rounds']
    tournament_object.round_descriptions = tournament_instance[0]['round_descriptions']
    tournament_object.player_emails = tournament_instance[0]['player_emails']
    tournament_object.player_instances = tournament_instance[0]['player_instances']
    tournament_object.time_ctrl = tournament_instance[0]['time_ctrl']
    tournament_object.description = tournament_instance[0]['description']
    tournament_object.done = tournament_instance[0]['done']
    tournament_object.round_instances = tournament_instance[0]['round_instances']
    tournament_object.match_instances = tournament_instance[0]['match_instances']
    return tournament_object


def generate_player_object():
    player_object = Player('players.json')
    return player_object


def get_new_player_data():
    player_object = generate_player_object()
    while True:
        try:
            email = input("Enter player's email address: ")
            assert '@' in email
        except AssertionError:
            print('Please enter a valid email address.')
            continue
        if email in player_object.get_player_emails():
            print('This email is already assigned to another user.')
            continue
        else:
            break
    last_name = input("Enter last name: ").upper()
    first_name = input("Enter first name: ").capitalize()
    date_of_birth = input("Enter date of birth (format dd/mm/yyyy): ")
    sex = input("Enter sex of player: ")
    while True:
        try:
            ranking = int(input("Enter ranking of participant: "))
        except ValueError:
            print('Please enter only numerical values. ')
            continue
        else:
            break
    player_object.create_player(email, last_name, first_name, date_of_birth, sex, ranking)


def update_player_data():
    player_object = generate_player_object()
    if len(player_object.db_players.all()) > 0:
        player_email_addresses = player_object.get_player_emails()
        views.show_players(player_object.read_player_list())
        while True:
            try:
                email = input("Which player would you like to edit? "
                              "(enter the player's email address to access the correct player instance.) ")
                assert email in player_email_addresses
            except AssertionError:
                print('Sorry, you need to enter an email address that is currently present in the database.')
                views.show_players(player_object.read_player_list())
                continue
            else:
                views.show_one_player(player_object, email)
                break

        fields_to_edit = input("Which fields would you like to edit?"
                               "\n (1) last_name "
                               "\n (2) first_name "
                               "\n (3) date_of_birth "
                               "\n (4) sex "
                               "\n (5) ranking"
                               "\n (6) email"
                               "\n Enter only the numerical values of the fields "
                               "that you would like to edit. (ex. 1 2 3)"
                               "\n Input:  ")
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
        player_object.update_player(email, last_name, first_name, date_of_birth, sex, ranking, new_email)
    else:
        print("There aren't any players saved in the database.")


def update_player_rankings():
    player_object = generate_player_object()
    views.show_players(player_object.read_player_list())
    confirm = input("Would you like to update all player rankings? (y/n) ")
    if confirm == 'y':
        for player in player_object.db_players.all():
            views.show_one_player(player_object, player['email'])
            while True:
                try:
                    new_ranking = int(input("Enter the player's new ranking: "))
                except ValueError:
                    print('Please enter only numerical values. ')
                    continue
                else:
                    player_object.update_ranking(player['email'], new_ranking)
                    break


def remove_player():
    player_object = generate_player_object()
    if len(player_object.db_players.all()) > 0:
        player_email_addresses = player_object.get_player_emails()
        views.show_players(player_object.read_player_list())
        while True:
            try:
                email = input("Which player would you like to delete? "
                              "(enter the player's email address to access the correct player instance.) ")
                assert email in player_email_addresses
            except AssertionError:
                print('Sorry, you need to enter an email address that is currently present in the database.')
                views.show_players(player_object.read_player_list())
                continue
            else:
                player_object.delete_player(email)
                break
    else:
        print("There aren't any players saved in the database.")


def populate_player_instances(name_of_tournament):
    tournament = generate_tournament_object().read_one_tournament(name_of_tournament)[0]
    player_instances = []
    for email in tournament['player_emails']:
        player_instances.append(generate_player_object().read_one_player(email)[0])
    player_instances.sort(key=operator.itemgetter('ranking'))
    filtered_player_instances = []
    local_player_index = 0
    for player_instance in player_instances:
        local_player_index += 1
        filtered_player = {'local_player_index': local_player_index,
                           'email': player_instance['email'],
                           'first_name': player_instance['first_name'],
                           'points': 0}
        filtered_player_instances.append(filtered_player)
    generate_tournament_object().update_player_instances(filtered_player_instances, name_of_tournament)


def get_new_tournament_data():
    tournament_object = generate_tournament_object()
    name_of_tournament = str(input('Enter name of tournament: ')) + ' ' + str(
        datetime.date.today().strftime("%d/%m/%y"))
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
        try:
            nb_players = int(input('Enter how many players are playing in this tournament: '))
        except ValueError:
            print('Please enter only whole number values. ')
            continue
        else:
            break
    views.show_players(generate_player_object().read_player_list())
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
            if email not in generate_player_object().get_player_emails():
                add_new_player = input('This email address matches no saved users, add a new user with this email? ('
                                       'y/n): ')
                if add_new_player == 'y':
                    get_new_player_data()
                    player_emails.append(generate_player_object().read_one_player(email)[0]['email'])
                    counter += 1
                continue
            else:
                counter += 1
                player_emails.append(email)
                break
    while True:
        try:
            time_ctrl = input("Type of time control (Bullet, Blitz, ou Coup Rapide): ")
            assert time_ctrl in ["Bullet", "Blitz", "Coup Rapide"]
        except AssertionError:
            print("Please select one of the available options.")
            continue
        else:
            break
    description = input('Enter the description of the tournament: ')
    tournament_object.create_tournament(name_of_tournament, location, nb_rounds, player_emails, time_ctrl, description)
    populate_player_instances(name_of_tournament)

# TODO brouillon ci-dessous, à retravailler

def get_local_player_index_numbers(tournament_object):
    local_player_index_numbers = []
    for player in tournament_object.player_instances:
        local_player_index_numbers.append(player['local_player_index'])
    return local_player_index_numbers

tournament_object = access_tournament_object("Name 23/02/21")

def generate_round_1_matches(tournament_object):
    nb_players = len(tournament_object.player_instances)
    local_player_index_numbers = get_local_player_index_numbers(tournament_object)
    top_half = local_player_index_numbers[0:int(nb_players / 2)]
    bottom_half = local_player_index_numbers[int(nb_players / 2):nb_players]
    round_matches = []
    for local_player_index in top_half:
        round_matches.append((local_player_index, bottom_half[local_player_index-1]))
    tournament_object.round_descriptions = [round_matches, ]


generate_round_1_matches(tournament_object)

def point_counter(tournament_object, round_number):
    current_round_matches = tournament_object.round_descriptions[round_number-1]
    for match in current_round_matches:
        winner = int(input(f"Winner? {match[0]} or {match[1]}: "))
        if winner == match[0]:
            for player_instance in tournament_object.player_instances:
                if player_instance['local_player_index'] == match[0]:
                    player_instance['points'] += 1
        if winner == match[1]:
            for player_instance in tournament_object.player_instances:
                if player_instance['local_player_index'] == match[1]:
                    player_instance['points'] += 1

point_counter(tournament_object, 1)

def next_round_matches(tournament_object):
    matches = []
    tournament_object.player_instances.sort(key=operator.itemgetter('points'), reverse=True)
    local_player_index_numbers = get_local_player_index_numbers(tournament_object)
    test_list = list(itertools.chain.from_iterable(tournament_object.round_descriptions))
    print(test_list)
    for round in tournament_object.round_descriptions:
        for match in round:
            for player in match:
                print(player)

next_round_matches(tournament_object)