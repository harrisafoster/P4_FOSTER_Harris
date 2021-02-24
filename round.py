from tinydb import TinyDB, Query, where
import datetime


class Round:
    def __init__(self, json_file):
        self.db_tournaments = TinyDB(json_file)
        self.query = Query()
        self.tournament_name = ""
        self.round_number = ""
        self.date = ""
        self.start_of_round = None
        self.end_of_round = ""
        self.matches = []
        self.time_ctrl = ""

    def serialize_round(self):
        round_data = {
            "tournament_name": self.tournament_name,
            "round_number": self.round_number,
            "date": self.date,
            "start_of_round": self.start_of_round,
            "end_of_round": self.end_of_round,
            "matches": self.matches,
            "time_ctrl": self.time_ctrl
        }
        return round_data

    def create_round(self, round_number, tournament):
        self.tournament_name = tournament.name_of_tournament
        self.round_number = round_number
        self.date = str(datetime.date.today())
        self.start_of_round = datetime.datetime.now()
        self.end_of_round = ""
        self.matches = tournament.round_descriptions[round_number - 1]
        self.time_ctrl = tournament.time_ctrl
        return self

    def read_one_round(self, round_number, tournament):
        current_tournament = self.db_tournaments.search(self.query.name_of_tournament == tournament.name_of_tournament)
        return current_tournament['round_instances'][round_number - 1]

    def read_all_rounds(self, tournament):
        current_tournament = self.db_tournaments.search(self.query.name_of_tournament == tournament.name_of_tournament)
        return current_tournament['round_instances']

    def delete_round(self, round_number, tournament):
        self.db_tournaments.remove(
            where('tournament_name') == tournament.name and where('round_number') == round_number)
