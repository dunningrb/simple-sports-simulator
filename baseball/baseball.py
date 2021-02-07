from league.league import League
from team.team import Team
import random


class BaseballTeam(Team):

    def __init__(self, name, pitch=3, relief=3, field=3, bat=27, power=3, speed=3):

        super(BaseballTeam, self).__init__(name=name)

        self.pitch = pitch
        self.relief = relief
        self.field = field
        self.bat = bat
        self.power = power
        self.speed = speed

    @property
    def win_pct(self):
        try:
            return self.wins / self.games_played
        except ZeroDivisionError:
            return 0.000


class BaseballLeague(League):

    def __init__(self, *, name, season, rotations, results_file, teams, home_adj=None):

        super(BaseballLeague, self).__init__(
            name=name, season=season, rotations=rotations, results_file=results_file,
            members=teams, member_type=BaseballTeam
        )

        self.home_adj = home_adj if home_adj is not None else 0

        self.option_methods['Standings'] = self.print_standings
        self.option_methods['Play Next Game'] = self.play_next_game

        self.print_menu()

    @property
    def standings(self):
        def _sort_items(t):
            return {'W': t.wins, 'L': t.losses, 'PCT': t.win_pct}

        return {k: v for k, v in
                sorted({t: _sort_items(t) for t in self.members.values()}.items(),
                       key=lambda x: (x[1]['PCT'], x[1]['W'], -x[1]['L']),
                       reverse=True)}

    def print_standings(self):
        max_len = -1
        for name in self.members:
            max_len = max(max_len, len(name))

        table_cols = ['W', 'L', 'PCT', 'GB', 'RF', 'RA', 'RD']

        sp4 = ' ' * 4

        table_str = 'Pos' + sp4 + 'Team' + ' ' * (max_len - 1)
        table_str += ''.join(col + sp4 for col in table_cols)
        table_str += '\n' + '-' * len(table_str) + '\n'

        first_delta = None
        for position, team in enumerate(self.standings, 1):
            if team.win_pct == 1:
                win_pct_str = '1.000'
            else:
                win_pct_str = '.' + f'{team.win_pct:4.3f}'.split('0.')[-1]

            if first_delta is None:
                gb_str = '---'
                first_delta = team.wins - team.losses
            else:
                gb = (first_delta - (team.wins - team.losses)) / 2
                gb_str = (f'{gb:.1f}' if gb % 1 == 0.5 else f'{gb:.0f}') if gb > 0 else '---'

            row_str = (f'{position}{" " * (6 - len(str(position)))} '
                       f'{team.name}{" " * (2 + max_len - len(str(team.name)))} '
                       f'{team.wins}{" " * (4 - len(str(team.wins)))} '
                       f'{team.losses}{" " * (4 - len(str(team.losses)))} '
                       f'{win_pct_str}{" " * (6 - len(win_pct_str))} '
                       f'{gb_str}{" " * (6 - len(gb_str))}'
                       f'{team.score_for}{" " * (5 - len(str(team.score_for)))} '
                       f'{team.score_against}{" " * (5 - len(str(team.score_against)))} '
                       f'{team.score_diff}{" " * (6 - len(str(team.score_diff)))} '
                       f'\n')
            table_str += ''.join(row_str)

        print(f'{"-" * 100}\n'
              f'{self.name} Table\n\n{table_str}\n\n'
              f'{"-" * 100}\n')

    def play_next_game(self):
        def _run_calc(*, batting, fielding):
            bat = batting.bat
            power = batting.power
            pitch = fielding.pitch

            white = random.randint(1, 6)
            red = random.randint(1, 6)
            green = random.randint(1, 6)

            total = sum([white, red, green])
            doubles = white == red or white == green or red == green
            runs = random.randint(0, 3)

            if not doubles and not total <= 10:
                pitch *= white
                runs = int(bat / pitch)

            if white == red or white == green:
                bat += power * total
                runs = int(bat / pitch)

            elif red == green:
                bat += 0.75 * power * total
                runs = int(bat / pitch)

            elif white == red == green:
                bat += 2 * power * total
                runs = int(bat / pitch)

            elif total <= 10:
                if red > green:
                    pitch -= red
                    pitch = max(pitch, 2)
                elif green > red:
                    pitch += green
                    pitch = min(pitch, 6)
                runs = int(bat / pitch)

            if runs > 8:
                overruns = runs - 8
                runs = 8 + int(random.random() * overruns)

            return runs

        details = self.next_game_details()

        if details is None:
            print(f'No remaining games.')
            return

        round_no = details['round-no']
        game_no = details['game-no']
        home = self.members[details['home-name']]
        away = self.members[details['away-name']]

        away_runs = _run_calc(batting=away, fielding=home)
        home_runs = _run_calc(batting=home, fielding=away)

        extra_innings = 0
        while away_runs == home_runs:
            extra_innings += 1
            away_runs += int(_run_calc(batting=away, fielding=home) / 9)
            home_runs += int(_run_calc(batting=home, fielding=away) / 9)

        score_str = f'{away.name} {away_runs} -- {home.name} {home_runs}'

        if extra_innings > 0:
            score_str += f' ({9 + extra_innings})'
        print(f'\n{"*" * 100}\n'
              f'Round {round_no}, Game No {game_no}: {score_str}\n'
              f'{"*" * 100}\n')

        self.results[game_no]['home-score'] = home_runs
        self.results[game_no]['away-score'] = away_runs
        round_no = self.results[game_no]['round-no']

        line = f'{round_no},{game_no},{away.name},{away_runs},{home.name},{home_runs}\n'
        with open(self.results_file, 'a') as f:
            f.write(line)

        home.update_results(game_id=game_no, opponent=away, score_for=home_runs, score_against=away_runs)
        away.update_results(game_id=game_no, opponent=home, score_for=away_runs, score_against=home_runs)

        self.print_standings()
