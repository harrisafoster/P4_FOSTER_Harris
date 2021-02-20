from tinydb import TinyDB, Query, where

# TODO Updates Views

class Player:
    query = Query()

    def __init__(self, email, last_name, first_name, date_of_birth, sex, ranking):
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking

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

    @classmethod
    def create_player(cls, email, last_name, first_name, date_of_birth, sex, ranking):
        db_players = TinyDB('players.json')
        player = cls(email, last_name, first_name, date_of_birth, sex, ranking)
        db_players.insert(player.serialize_player())

    @classmethod
    def read_one_player(cls, email):
        db_players = TinyDB('players.json')
        return db_players.search(Player.query.email == email)

    @classmethod
    def read_player_list(cls):
        db_players = TinyDB('players.json')
        players = []
        for player in db_players.all():
            players.append(player)
        return players

    @classmethod
    def update_player(cls, email, last_name, first_name, date_of_birth, sex, ranking, new_email):
        db_players = TinyDB('players.json')
        if last_name:
            db_players.update({'last_name': last_name}, Player.query["email"] == email)
        if first_name:
            db_players.update({'first_name': first_name}, Player.query["email"] == email)
        if date_of_birth:
            db_players.update({'date_of_birth': date_of_birth}, Player.query["email"] == email)
        if sex:
            db_players.update({'sex': sex}, Player.query["email"] == email)
        if ranking:
            db_players.update({'ranking': ranking}, Player.query["email"] == email)
        if new_email:
            db_players.update({'email': new_email}, Player.query["email"] == email)

    @classmethod
    def update_ranking(cls, email, new_ranking):
        db_players = TinyDB('players.json')
        db_players.update({'ranking': new_ranking}, Player.query["email"] == email)

    @classmethod
    def get_player_emails(cls):
        db_players = TinyDB('players.json')
        player_emails = []
        for player in db_players.all():
            player_emails.append(player['email'])
        return player_emails

    @classmethod
    def delete_player(cls, email):
        db_players = TinyDB('players.json')
        db_players.remove(where('email') == email)
