from tinydb import TinyDB, Query, where
import operator


class Player:
    def __init__(self, json_file):
        self.db_players = TinyDB(json_file)
        self.query = Query()
        self.email = ""
        self.last_name = ""
        self.first_name = ""
        self.date_of_birth = ""
        self.sex = ""
        self.ranking = 0

    def serialize_player(self):
        player_data = {
            "email": self.email,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "ranking": self.ranking
        }
        return player_data

    def create_player(self, email, last_name, first_name, date_of_birth, sex, ranking):
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.db_players.insert(self.serialize_player())

    def read_one_player(self, email):
        return self.db_players.search(self.query.email == email)

    def read_player_list(self):
        return self.db_players.all()

    def update_player(self, email, last_name, first_name, date_of_birth, sex, ranking, new_email):
        if last_name:
            self.db_players.update({'last_name': last_name}, self.query["email"] == email)
        if first_name:
            self.db_players.update({'first_name': first_name}, self.query["email"] == email)
        if date_of_birth:
            self.db_players.update({'date_of_birth': date_of_birth}, self.query["email"] == email)
        if sex:
            self.db_players.update({'sex': sex}, self.query["email"] == email)
        if ranking:
            self.db_players.update({'ranking': ranking}, self.query["email"] == email)
        if new_email:
            self.db_players.update({'email': new_email}, self.query["email"] == email)

    def update_ranking(self, email, new_ranking):
        self.db_players.update({'ranking': new_ranking}, self.query["email"] == email)

    def get_player_emails(self):
        player_emails = []
        for player in self.db_players.all():
            player_emails.append(player['email'])
        return player_emails

    def delete_player(self, email):
        self.db_players.remove(where('email') == email)

    def sort_all_players_by_ranking(self):
        list_of_players = self.db_players.all()
        list_of_players.sort(key=operator.itemgetter('ranking'))
        return list_of_players

    def sort_all_players_by_last_name(self):
        list_of_players = self.db_players.all()
        list_of_players.sort(key=operator.itemgetter('last_name'))
        return list_of_players
