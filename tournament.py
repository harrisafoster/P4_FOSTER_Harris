from tinydb import TinyDB, Query, where
import datetime
import operator


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

    # TODO test
    def already_played(self, new_match):
        if new_match in [match for round in self.round_descriptions for match in round]:
            return True
        else:
            return False

    # TODO test
    def swiss_method(self):
        matches = []
        for player_instance in self.player_instances:
            new_player_a = {"local_player_id": player_instance["local_player_id"],
                            "ranking": player_instance["ranking"],
                            "first_name": player_instance["first_name"],
                            "email": player_instance["email"]}
            if new_player_a not in [match for round in matches for match in round]:
                for other_player_instance in self.player_instances:
                    new_player_b = {"local_player_id": other_player_instance["local_player_id"],
                                    "ranking": other_player_instance["ranking"],
                                    "first_name": other_player_instance["first_name"],
                                    "email": other_player_instance["email"]}
                    if new_player_b != new_player_a and new_player_b not in [match for round in matches for match in
                                                                             round]:
                        if not self.already_played([new_player_a, 'vs.', new_player_b]) and not self.already_played(
                                [new_player_b, 'vs.', new_player_a]):
                            matches.append([new_player_a, 'vs.', new_player_b])
                            break
        return matches

    # TODO test
    def get_and_filter_players(self):
        db_players = TinyDB('players.json')
        players = []
        index = 0
        for email in self.player_emails:
            for player in db_players:
                if player['email'] == email:
                    player['ranking'] = int(player['ranking'])
                    players.append(player)
        players.sort(key=operator.itemgetter('ranking'))
        filtered_players = []
        for player in players:
            index += 1
            email = player["email"]
            ranking = player["ranking"]
            first_name = player["first_name"]
            filtered_player = {"local_player_id": index,
                               "ranking": ranking,
                               "first_name": first_name,
                               "email": email,
                               "points": 0}
            filtered_players.append(filtered_player)
        filtered_players.sort(key=operator.itemgetter('local_player_id'))
        self.player_instances = filtered_players

    # TODO test
    def round_1_matches(self):
        if not self.round_descriptions:
            self.get_and_filter_players()
            players_without_points = []
            for player_instance in self.player_instances:
                player_without_points = {"local_player_id": player_instance["local_player_id"],
                                         "ranking": player_instance["ranking"],
                                         "first_name": player_instance["first_name"],
                                         "email": player_instance["email"]}
                players_without_points.append(player_without_points)
            round_descriptions = [
                [players_without_points[0], 'vs.', players_without_points[4]],
                [players_without_points[1], 'vs.', players_without_points[5]],
                [players_without_points[2], 'vs.', players_without_points[6]],
                [players_without_points[3], 'vs.', players_without_points[7]]
            ]
            self.round_descriptions = [round_descriptions, ]

    # TODO finish & divide this function
    '''def initialize_next_round(self, round_number):'''