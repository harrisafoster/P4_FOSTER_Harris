from tinydb import TinyDB, Query, where
import datetime


class Match:
    query = Query()

    def __init__(self, round_number, match_number, date, start_of_match, end_of_match, players, winner, time_ctrl):
        self.round_number = round_number
        self.match_number = match_number
        self.date = date
        self.start_of_match = start_of_match
        self.end_of_match = end_of_match
        self.players = players
        self.winner = winner
        self.time_ctrl = time_ctrl

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

    # TODO test
    @classmethod
    def create_match(cls, round_number, match_number, winner, current_round_instance, duration):
        date = str(current_round_instance.date)
        start_of_match = current_round_instance.start_of_round
        players = current_round_instance.matches[match_number - 1]
        time_ctrl = current_round_instance.time_ctrl
        end_of_match = current_round_instance.start_of_round + datetime.timedelta(hours=duration)
        match_instance_data = Match(
            round_number, match_number, date, start_of_match, end_of_match, players, winner, time_ctrl)
        return match_instance_data

    # TODO test
    @classmethod
    def read_one_match(cls, round_number, match_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        return db_tournaments.search(
            where('tournament_name') == tournament.name
            and where('round_number' == round_number)
            and where('match_number' == match_number))

    # TODO test
    @classmethod
    def read_all_matches(cls, tournament):
        db_tournaments = TinyDB('tournaments.json')
        current_tournament = db_tournaments.search(Match.query.tournament_name == tournament.name)
        return current_tournament['match_instances']

    # TODO test
    @classmethod
    def update_match(cls, round_number, match_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        placement = round_number * 4
        db_tournaments.update({'match_instances'[placement - match_number]:
                                   tournament.match_instances[placement - match_number]},
                              Match.query["Name of tournament: "] == tournament.name)

    # TODO test
    @classmethod
    def delete_round(cls, round_number, match_number, tournament):
        db_tournaments = TinyDB('tournaments.json')
        db_tournaments.remove(
            where('tournament_name') == tournament.name
            and where('round_number') == round_number
            and where('match_number') == match_number)
