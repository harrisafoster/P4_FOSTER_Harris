from tinydb import TinyDB, Query, where
import datetime
import itertools
import operator
from random import shuffle
from player import Player


class Tournament:
    def __init__(self, json_file):
        self.db_tournaments = TinyDB(json_file)
        self.query = Query()
        self.name_of_tournament = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.nb_rounds = 0
        self.round_descriptions = []
        self.player_emails = []
        self.player_instances = []
        self.time_ctrl = ""
        self.description = ""
        self.done = None
        self.round_instances = []
        self.match_instances = []

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

    def access_tournament_object(self, name_of_tournament):
        tournament_instance = self.db_tournaments.search(self.query['name_of_tournament'] ==
                                                         name_of_tournament)
        self.name_of_tournament = tournament_instance[0]['name_of_tournament']
        self.location = tournament_instance[0]['location']
        self.start_date = tournament_instance[0]['start_date']
        self.end_date = tournament_instance[0]['end_date']
        self.nb_rounds = tournament_instance[0]['nb_rounds']
        self.round_descriptions = tournament_instance[0]['round_descriptions']
        self.player_emails = tournament_instance[0]['player_emails']
        self.player_instances = tournament_instance[0]['player_instances']
        self.time_ctrl = tournament_instance[0]['time_ctrl']
        self.description = tournament_instance[0]['description']
        self.done = tournament_instance[0]['done']
        self.round_instances = tournament_instance[0]['round_instances']
        self.match_instances = tournament_instance[0]['match_instances']
        return self

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

    def update_player_instances(self, player_instances):
        self.db_tournaments.update({'player_instances': player_instances},
                                   self.query["name_of_tournament"] == self.name_of_tournament)

    def update_round_descriptions(self):
        self.db_tournaments.update({'round_descriptions': self.round_descriptions},
                                   self.query["name_of_tournament"] == self.name_of_tournament)

    def update_round_instances(self):
        self.db_tournaments.update({'round_instances': self.round_instances},
                                   self.query["name_of_tournament"] == self.name_of_tournament)

    def update_match_instances(self):
        self.db_tournaments.update({'match_instances': self.match_instances},
                                   self.query["name_of_tournament"] == self.name_of_tournament)

    def update_end_date(self):
        self.db_tournaments.update({'end_date': self.end_date},
                                   self.query['name_of_tournament'] == self.name_of_tournament)

    def update_done_status(self):
        self.db_tournaments.update({'done': self.done},
                                   self.query['name_of_tournament'] == self.name_of_tournament)

    def get_local_player_index_numbers(self):
        local_player_index_numbers = []
        for player in self.player_instances:
            local_player_index_numbers.append(player['local_player_index'])
        return local_player_index_numbers

    def check_if_already_played(self, new_match):
        if new_match in list(itertools.chain.from_iterable(self.round_descriptions)):
            return True
        else:
            return False

    def sort_players_by_points_descending(self):
        self.player_instances.sort(key=operator.itemgetter('local_player_index'))
        self.player_instances.sort(key=operator.itemgetter('points'), reverse=True)
        return self.player_instances

    def sort_players_by_local_index(self):
        self.player_instances.sort(key=operator.itemgetter('local_player_index'))
        return self.player_instances

    def sort_players_by_last_name(self):
        self.player_instances.sort(key=operator.itemgetter('last_name'))
        return self.player_instances

    def sort_players_by_points_ascending(self):
        self.player_instances.sort(key=operator.itemgetter('local_player_index'))
        self.player_instances.sort(key=operator.itemgetter('points'))

    def generate_round_1_matches(self):
        nb_players = len(self.player_instances)
        local_player_index_numbers = self.get_local_player_index_numbers()
        local_player_index_numbers.sort()
        top_half = local_player_index_numbers[0:int(nb_players / 2)]
        bottom_half = local_player_index_numbers[int(nb_players / 2):nb_players]
        round_matches = []
        for local_player_index in top_half:
            round_matches.append((local_player_index, bottom_half[local_player_index - 1]))
        self.round_descriptions = [round_matches, ]

    def make_new_matches_for_swiss(self, local_player_index_numbers):
        matches = []
        for player_a in local_player_index_numbers:
            if player_a not in list(itertools.chain.from_iterable(matches)):
                for player_b in local_player_index_numbers:
                    if player_b != player_a and player_b not in list(itertools.chain.from_iterable(matches)):
                        if not self.check_if_already_played((player_a, player_b)) \
                                and not self.check_if_already_played([player_a, player_b])\
                                and not self.check_if_already_played((player_b, player_a))\
                                and not self.check_if_already_played([player_b, player_a]):
                            matches.append((player_a, player_b))
                            break
        return matches

    def swiss_method_pairing(self):
        self.sort_players_by_points_descending()
        local_player_index_numbers = self.get_local_player_index_numbers()
        new_matches = self.make_new_matches_for_swiss(local_player_index_numbers)
        if len(new_matches) == len(local_player_index_numbers) / 2:
            self.round_descriptions += [new_matches]
            self.update_round_descriptions()
        else:
            self.sort_players_by_points_ascending()
            local_player_index_numbers = self.get_local_player_index_numbers()
            new_matches = self.make_new_matches_for_swiss(local_player_index_numbers)
            if len(new_matches) == len(local_player_index_numbers) / 2:
                self.round_descriptions += [new_matches]
                self.update_round_descriptions()
            else:
                shuffle(self.get_local_player_index_numbers())
                local_player_index_numbers = (self.get_local_player_index_numbers())
                new_matches = self.make_new_matches_for_swiss(local_player_index_numbers)
                if len(new_matches) == len(local_player_index_numbers) / 2:
                    self.round_descriptions += [new_matches]
                    self.update_round_descriptions()

    def populate_player_instances(self):
        tournament = self.read_one_tournament(self.name_of_tournament)[0]
        player_object = Player('players.json')
        player_instances = []
        for email in tournament['player_emails']:
            player_instances.append(player_object.read_one_player(email)[0])
        player_instances.sort(key=operator.itemgetter('ranking'))
        filtered_player_instances = []
        local_player_index = 0
        for player_instance in player_instances:
            local_player_index += 1
            filtered_player = {'local_player_index': local_player_index,
                               'email': player_instance['email'],
                               'last_name': player_instance['last_name'],
                               'first_name': player_instance['first_name'],
                               'points': 0,
                               'current_ranking': player_instance['ranking']}
            filtered_player_instances.append(filtered_player)
        self.update_player_instances(filtered_player_instances)

    def delete_round(self, round_number):
        del self.round_descriptions[round_number-1]
        del self.round_instances[round_number-1]
        self.update_round_descriptions()
        self.update_round_instances()
        self.match_instances = list(filter(lambda i: i['round_number'] != round_number, self.match_instances))
        self.update_match_instances()

    def delete_match(self, round_number, match_number):
        tournament_dict = self.db_tournaments.search(where('name_of_tournament') ==
                                                     self.name_of_tournament)
        match_instances = tournament_dict[0]['match_instances']
        matches_per_round = len(self.round_descriptions[0])
        del match_instances[((round_number-1) * matches_per_round) + (match_number-1)]
        self.match_instances = match_instances
        self.update_match_instances()
        del self.round_descriptions[round_number-1][match_number-1]
        self.update_round_descriptions()
        del self.round_instances[round_number-1]['matches'][match_number - 1]
        self.update_round_instances()
