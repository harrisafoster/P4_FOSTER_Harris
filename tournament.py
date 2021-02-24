from tinydb import TinyDB, Query, where
import datetime


class Tournament:
    def __init__(self, json_file):
        self.db_tournaments = TinyDB(json_file)
        self.query = Query()
        self.name_of_tournament = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.nb_rounds = 0
        self.round_descriptions = ""
        self.player_emails = ""
        self.player_instances = ""
        self.time_ctrl = ""
        self.description = ""
        self.done = None
        self.round_instances = ""
        self.match_instances = ""

    def serialize_tournament(self):
        tournament_data = {
            "name_of_tournament": self.name_of_tournament,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "nb_rounds": self.nb_rounds,
            "round_descriptions": self.round_descriptions,
            "player_emails": self.player_emails,
            "player_instances": self.player_instances,
            "time_ctrl": self.time_ctrl,
            "description": self.description,
            "done": self.done,
            "round_instances": self.round_instances,
            "match_instances": self.match_instances
        }
        return tournament_data

    def create_tournament(self, name_of_tournament, location, nb_rounds, player_emails, time_ctrl, description):
        self.name_of_tournament = name_of_tournament
        self.location = location
        self.start_date = str(datetime.date.today())
        self.end_date = None
        self.nb_rounds = nb_rounds
        self.round_descriptions = []
        self.player_emails = player_emails
        self.player_instances = []
        self.time_ctrl = time_ctrl
        self.description = description
        self.done = None
        self.round_instances = []
        self.match_instances = []
        self.db_tournaments.insert(self.serialize_tournament())
        return name_of_tournament

    def get_tournament_names(self):
        tournament_names = []
        for tournament in self.db_tournaments.all():
            tournament_names.append(tournament['name_of_tournament'])
        return tournament_names

    def read_all_tournaments(self):
        return self.db_tournaments.all()

    def read_one_tournament(self, name_of_tournament):
        return self.db_tournaments.search(self.query.name_of_tournament == name_of_tournament)

    def delete_tournament(self, name_of_tournament):
        self.db_tournaments.remove(where('name_of_tournament') == name_of_tournament)

    def update_player_instances(self, player_instances, name_of_tournament):
        self.db_tournaments.update({'player_instances': player_instances},
                                   self.query["name_of_tournament"] == name_of_tournament)

    def update_round_descriptions(self):
        self.db_tournaments.update({'round_descriptions': self.round_descriptions},
                                   self.query["name_of_tournament"] == self.name_of_tournament)
