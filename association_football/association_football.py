from league.league import League
from team.team import Team
import os


class AssociationFootballClub(Team):
    def __init__(self, *, name, avg_shots_for, goal_pct_for, avg_shots_against, goal_pct_against):
        super(AssociationFootballClub, self).__init__(name=name)
        self.avg_shots_for = avg_shots_for
        self.goal_pct_for = goal_pct_for
        self.avg_shots_against = avg_shots_against
        self.goal_pct_against = goal_pct_against

    @property
    def points(self):
        return 3 * self.wins + self.ties


class AssociationFootballLeague(League):
    def __init__(self, *, name, season, home_adj=None, rotations, results_file, avg_shots,
                 goal_pct, teams):
        super(AssociationFootballLeague, self).__init__(
            name=name, season=season, rotations=rotations, results_file=results_file,
            teams=teams, teams_type=AssociationFootballClub
        )
        self.avg_shots = avg_shots
        self.goal_pct = goal_pct
        self.home_adj = home_adj if home_adj is not None else 0

        self.option_methods['Table'] = self.print_table
        self.option_methods['Play Next Game'] = self.play_next_match

        self.print_menu()
        
    @property
    def table(self):
        def _sort_items(t):
            return {'W': t.wins, 'L': t.losses, 'PTS': t.points, 'GD': t.score_diff}

        return {
            k: v for k, v in sorted(
                {t: _sort_items(t) for t in self.teams.values()}.items(),
                key=lambda x: (x[1]['PTS'], x[1]['W'], -x[1]['L'], x[1]['GD']), reverse=True
            )
        }
    
    def print_table(self):
        max_len = -1
        for name in self.teams:
            max_len = max(max_len, len(name))

        table_cols = ['GP', 'W', 'L', 'D', 'PTS', 'GF', 'GA', 'GD']

        sp4 = ' ' * 4

        table_str = 'Pos' + sp4 + 'Club' + ' ' * (max_len - 1)
        table_str += ''.join(col + sp4 for col in table_cols)
        table_str += '\n' + '-' * len(table_str) + '\n'

        for position, team in enumerate(self.table, 1):
            row_str = (f'{position}{" " * (6 - len(str(position)))} '
                       f'{team.name}{" " * (3 + max_len - len(str(team.name)))} '
                       f'{team.games_played}{" " * (4 - len(str(team.games_played)))} '
                       f'{team.wins}{" " * (4 - len(str(team.wins)))} '
                       f'{team.losses}{" " * (4 - len(str(team.losses)))} '
                       f'{team.ties}{" " * (4 - len(str(team.ties)))} '
                       f'{team.points}{" " * (6 - len(str(team.points)))} '
                       f'{team.score_for}{" " * (5 - len(str(team.score_for)))} '
                       f'{team.score_against}{" " * (5 - len(str(team.score_against)))} '
                       f'{team.score_diff}{" " * (6 - len(str(team.score_diff)))} '
                       f'\n')
            table_str += ''.join(row_str)

        print(f'{"-" * 100}\n'
              f'{self.name}\n\n{table_str}\n\n'
              f'{"-" * 100}\n')

    def play_next_match(self):

        def _resolve(lg_rt, t1_rt, t2_rt):
            return lg_rt + (t1_rt + t2_rt - 2 * lg_rt)

        def _rand():
            """Return a random number between 0 and 1."""
            return int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)

        details = self.next_game_details()

        if details is None:
            print(f'No remaining matches.')
            return

        round_no = details['round-no']
        game_no = details['game-no']
        home = self.teams[details['home-name']]
        away = self.teams[details['away-name']]

        # How many shots for each team?
        home_shots = _resolve(self.avg_shots, home.avg_shots_for, away.avg_shots_against)
        away_shots = _resolve(self.avg_shots, home.avg_shots_against, away.avg_shots_for)

        # Goal pct for each team?
        home_goal_pct = _resolve(self.goal_pct, home.goal_pct_for, away.goal_pct_against)
        away_goal_pct = _resolve(self.goal_pct, home.goal_pct_against, away.goal_pct_for)

        home_goals = 0
        for i in range(int(home_shots) + self.home_adj):
            if _rand() <= home_goal_pct:
                home_goals += 1

        away_goals = 0
        for i in range(int(away_shots) - self.home_adj):
            if _rand() <= away_goal_pct:
                away_goals += 1

        score_str = f'{home.name} {home_goals} -- {away.name} {away_goals}'
        print(f'\n{"*" * 100}\n'
              f'Round {round_no}, Game No. {game_no}: {score_str}.\n'
              f'{"*" * 100}\n')

        self.results[game_no]['home-score'] = home_goals
        self.results[game_no]['away-score'] = away_goals
        round_no = self.results[game_no]['round-no']

        line = f'{round_no},{game_no},{home.name},{home_goals},{away.name},{away_goals}\n'
        with open(self.results_file, 'a') as f:
            f.write(line)

        home.update_results(
            game_id=game_no, opponent=away, score_for=home_goals, score_against=away_goals
        )

        away.update_results(
            game_id=game_no, opponent=home, score_for=away_goals, score_against=home_goals
        )

        self.print_table()
