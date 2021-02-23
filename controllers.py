from player import Player
import views


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
