from tinydb import TinyDB, Query, where
import datetime


class Round:
    query = Query()

    def __init__(self, tournament_name, round_number, date, start_of_round, end_of_round, matches, time_ctrl):
        self.tournament_name = tournament_name
        self.round_number = round_number
        self.date = date
        self.start_of_round = start_of_round
        self.end_of_round = end_of_round
        self.matches = matches
        self.time_ctrl = time_ctrl

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

    # TODO improve?
    @classmethod
    def create_round(cls, round_number, tournament):
        tournament_name = tournament.name
        date = str(datetime.date.today())
        start_of_round = str(datetime.datetime.now().strftime("%H:%M:%S"))
        end_of_round = None
        matches = tournament.round_descriptions[round_number - 1]
        time_ctrl = tournament.time_ctrl
        round_instance_data = Round(tournament_name, round_number,
                                    date, start_of_round, end_of_round, matches, time_ctrl)
        return round_instance_data

    # TODO test
    @classmethod
    def read_one_round(cls, round_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        current_tournament = db_tournaments.search(Round.query.tournament_name == tournament.name)
        return current_tournament['round_instances'][round_number - 1]

    # TODO test
    @classmethod
    def read_all_rounds(cls, tournament):
        db_tournaments = TinyDB('tournaments.json')
        current_tournament = db_tournaments.search(Round.query.tournament_name == tournament.name)
        return current_tournament['round_instances']

    # TODO test
    @classmethod
    def update_round(cls, round_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        db_tournaments.update({'round_instances'[round_number - 1]: tournament.round_instances[round_number - 1]},
                              Round.query["Name of tournament: "] == tournament.name)

    # TODO test
    @classmethod
    def delete_round(cls, round_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        db_tournaments.remove(
            where('tournament_name') == tournament.name and where('round_number' == (round_number - 1)))
