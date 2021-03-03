from tinydb import TinyDB, Query
import datetime


class Round:
    def __init__(self, json_file):
        self.db_tournaments = TinyDB(json_file)
        self.query = Query()
        self.name_of_tournament = ""
        self.round_number = 0
        self.date = ""
        self.start_of_round = None
        self.end_of_round = ""
        self.matches = []
        self.time_ctrl = ""

    def serialize_round(self):
        round_data = {
            "name_of_tournament": self.name_of_tournament,
            "round_number": self.round_number,
            "date": self.date,
            "start_of_round": self.start_of_round.strftime("%H:%M:%S"),
            "end_of_round": self.end_of_round,
            "matches": self.matches,
            "time_ctrl": self.time_ctrl
        }
        return round_data
    # creation of dict from self for use in database

    def create_round(self, round_number, tournament):
        self.name_of_tournament = tournament.name_of_tournament
        self.round_number = round_number
        self.date = str(datetime.date.today())
        self.start_of_round = datetime.datetime.now()
        self.end_of_round = ""
        self.matches = tournament.round_descriptions[round_number - 1]
        self.time_ctrl = tournament.time_ctrl
        return self
    # creation of round object for use in tournaments

    def access_round_object(self, round_number, tournament):
        self.name_of_tournament = tournament.round_instances[round_number-1]['name_of_tournament']
        self.round_number = tournament.round_instances[round_number-1]['round_number']
        self.date = tournament.round_instances[round_number-1]['date']
        self.start_of_round = datetime.datetime.strptime(tournament.round_instances[round_number - 1]['start_of_round']
                                                         , '%H:%M:%S')
        self.end_of_round = tournament.round_instances[round_number-1]['end_of_round']
        self.matches = tournament.round_instances[round_number-1]['matches']
        self.time_ctrl = tournament.round_instances[round_number-1]['time_ctrl']
        return self
    # accesses a paused round

    def read_one_round(self, round_number, tournament):
        current_tournament = self.db_tournaments.search(
            self.query.name_of_tournament == tournament.name_of_tournament)
        return current_tournament[0]['round_instances'][round_number - 1]

    def read_all_rounds(self, tournament):
        current_tournament = self.db_tournaments.search(
            self.query.name_of_tournament == tournament.name_of_tournament)
        return current_tournament[0]['round_instances']
