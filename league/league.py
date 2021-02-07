from pathlib import Path
from string import ascii_uppercase

import interactive
import settings


class League:

    def __init__(self, *, name, season, rotations, results_file, members=None, member_type):
        self.name = name
        self.season = season
        self.rotations = rotations
        self.results_file = results_file
        self.members = members
        self.member_type = member_type
        self.exit_options = ['Q', 'q']
        self.option_methods = {
            'Next Game Details': self.print_next_game,
            'Games This Round': self.print_games_this_round
        }

        self.members = {name: member_type(name=name, **team) for name, team in members.items()}

        self.members = {
            k: v for k, v in sorted(
                self.members.items(), key=lambda item: item[1].name, reverse=False
            )
        }

        self.results = dict()
        self.build_results()
        self.load_results()

    def build_results(self):
        schedule_map = dict()
        num_members = len(self.members)

        if num_members % 2 == 1:
            key = (num_members, num_members + 1)
            letter = ascii_uppercase[num_members]
            schedule_map[letter] = 'BYE'
        else:
            key = (num_members - 1, num_members)

        schedule_table = settings.SCHEDULE_TABLES[key]
        rounds_per_rotation = len(schedule_table)
        letters = ascii_uppercase
        game_no = 0

        for rotation in range(self.rotations):
            for (letter, team) in zip(letters, [t.name for t in self.members.values()]):
                schedule_map[letter] = team

            for round_base, pairings in schedule_table.items():
                if rotation % 2 == 0:
                    pairings = pairings[::-1].replace(' ,', ', ')

                tokens = pairings.split(',')
                round_no = round_base + rotation * rounds_per_rotation

                for token in tokens:
                    subtokens = token.split('-')
                    home_name = schedule_map[subtokens[0]]
                    away_name = schedule_map[subtokens[1]]

                    if 'BYE' in [home_name, away_name]:
                        continue

                    game_no += 1

                    self.results[game_no] = {
                        'round-no': round_no, 'game-no': game_no, 'home-name': home_name, 'home-score': None,
                        'away-name': away_name, 'away-score': None
                    }

    def load_results(self):
        try:
            r_path = Path(self.results_file).resolve(strict=True)
        except FileNotFoundError:
            return
        else:
            with open(r_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                _, game_no, home_name, home_score, away_name, away_score = line.strip().split(',')

                game_no = int(game_no)

                self.results[game_no]['home-score'] = home_score
                self.results[game_no]['away-score'] = away_score

                self.members[home_name].update_results(
                    game_id=game_no, opponent=away_name, score_for=home_score, score_against=away_score)

                self.members[away_name].update_results(
                    game_id=game_no, opponent=home_name, score_for=away_score, score_against=home_score)

    def next_game_details(self):
        for game_no, details in self.results.items():
            if details['home-score'] is None:
                return details

    def print_menu(self):
        allowed_options = list()

        menu = (f'\n{"*" * 100}'
                f'\n{self.season} {self.name}\n'
                f'\nEnter your selection:')

        for key, option_name in enumerate(self.option_methods, 1):
            allowed_options.append(str(key))
            menu += f'\n\t[{key}] {option_name}'

        menu += (f'\n\t[{",".join([c for c in self.exit_options])}] Exit program.'
                 f'\n{"*" * 100}')

        option_map = {k: v for k, v in zip(allowed_options, self.option_methods.values())}
        interactive.clear_screen()

        while True:
            option_map[
                interactive.get_user_option(
                    prompt=menu, exit_options=self.exit_options, allowed_options=allowed_options
                )
            ]()

    def print_next_game(self):
        details = self.next_game_details()

        if details is None:
            print(f'No remaining games.')
            return

        print(f'NEXT GAME: Round {details["round-no"]}, Game No. {details["game-no"]}'
              f'\n\n\t{details["away-name"]} @ {details["home-name"]}.')

    def print_games_this_round(self):
        details = [self.next_game_details()]
        current_round = details[0]['round-no']

        for game_no, results in self.results.items():
            if current_round == results['round-no']:
                details.append(results) if results not in details else details

        details_str = f'THIS ROUND\'S GAMES: Round {current_round}\n'

        for d in details:
            details_str += f'\n\tGame {d["game-no"]}: {d["away-name"]} @ {d["home-name"]}'
            if d['home-score'] is not None:
                details_str += f' (result: {d["away-name"]} {d["away-score"]} -- {d["home-name"]} {d["home-score"]})'

        print(details_str)
