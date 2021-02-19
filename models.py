from tinydb import TinyDB, Query, where

# TODO Updates Views

class Player:
    def __init__(self, player_index, last_name, first_name, date_of_birth, sex, ranking, points):
        self.player_index = player_index
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.points = points

    def read_player(self):
        player_data = {
            "player_index": self.player_index,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "ranking": self.ranking,
            "points": self.points
        }
        return player_data

    def update_player(self, new_last_name, new_first_name, new_date_of_birth, new_sex, new_ranking, new_points):
        self.player_index = self.player_index
        self.last_name = new_last_name
        self.first_name = new_first_name
        self.date_of_birth = new_date_of_birth
        self.sex = new_sex
        self.ranking = new_ranking
        self.points = new_points

    @staticmethod
    def delete_player(player):
        del player

player1 = Player(1, 'Foster', 'Harris', '11/01/1992', 'Male', 1, 99)

print(player1.read_player())
player1.update_player('Taylor', 'Heather', '02/05/1991', 'Female', 8, 0)
print(player1.read_player())
Player.delete_player(player1)
print(player1.read_player())
