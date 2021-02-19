from tinydb import TinyDB, Query, where

# TODO Updates Views

class Player:
    def __init__(self, player_index, last_name, first_name, birthday, sex, ranking, points):
        self.player_index = player_index
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday
        self.sex = sex
        self.ranking = ranking
        self.points = points

    @classmethod
    def get_all_players(cls):
        db_players = TinyDB('players.json')
        result = []
        for item in db_players.all():
            player = Player(item['Player ID'], item['Last name'], item["First name"], item['Birth date'], item['Sex'], item['Ranking'], item['Points'])
            result.append(player)
        return result
