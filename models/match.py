from tinydb import TinyDB, Query, where


class Match:
    def __init__(self, json_file):
        self.query = Query()
        self.db_tournaments = TinyDB(json_file)
        self.round_number = 0
        self.match_number = 0
        self.date = ""
        self.start_of_match = None
        self.end_of_match = None
        self.players = []
        self.winner = []
        self.time_ctrl = ""

    def serialize_match(self):
        match_data = {
            "round_number": self.round_number,
            "match_number": self.match_number,
            "date": self.date,
            "start_of_match": self.start_of_match,
            "end_of_match": self.end_of_match,
            "players": self.players,
            "winner": self.winner,
            "time_ctrl": self.time_ctrl
        }
        return match_data

    def create_match(self, round_number, match_number, winner, current_round_instance):
        self.round_number = round_number
        self.match_number = match_number
        self.date = str(current_round_instance.date)
        self.start_of_match = current_round_instance.start_of_round
        self.end_of_match = None
        self.players = current_round_instance.matches[match_number - 1]
        self.winner = winner
        self.time_ctrl = current_round_instance.time_ctrl
        return self

    def read_one_match(self, round_number, match_number, tournament_object):
        tournament_dict = self.db_tournaments.search(where('name_of_tournament') ==
                                                     tournament_object.name_of_tournament)
        match_instances = tournament_dict[0]['match_instances']
        matches_per_round = len(tournament_object.round_descriptions[0])
        return match_instances[((round_number-1) * matches_per_round) + (match_number-1)]

    def read_all_matches(self, tournament_object):
        current_tournament = self.db_tournaments.search(self.query.name_of_tournament ==
                                                        tournament_object.name_of_tournament)
        return current_tournament[0]['match_instances']
