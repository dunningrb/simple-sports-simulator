from league.league import League
from team.team import Team
from utils.utils import rand, resolve


class BasketballTeam(Team):

    def __init__(self, *, name, a3p_for, p3p_for, a2p_for, p2p_for, aft_for, pft_for, 
                 a3p_against, p3p_against, a2p_against, p2p_against, aft_against, pft_against):
        
        super(BasketballTeam, self).__init__(name=name)
        
        self.a3p_for = a3p_for
        self.p3p_for = p3p_for
        self.a2p_for = a2p_for
        self.p2p_for = p2p_for
        self.aft_for = aft_for
        self.pft_for = pft_for
        self.a3p_against = a3p_against
        self.p3p_against = p3p_against
        self.a2p_against = a2p_against
        self.p2p_against = p2p_against
        self.aft_against = aft_against
        self.pft_against = pft_against

    @property
    def win_pct(self):
        try:
            return self.wins / self.games_played
        except ZeroDivisionError:
            return 0.000


class BasketballLeague(League):
    def __init__(self, *, name, season, rotations, results_file, teams, a3p, p3p, a2p, p2p, aft,
                 pft, home_a3p_adj=None, home_a2p_adj=None, home_aft_adj=None):
        super(BasketballLeague, self).__init__(
            name=name, season=season, rotations=rotations, results_file=results_file,
            members=teams, member_type=BasketballTeam
        )
        self.a3p = a3p
        self.p3p = p3p
        self.a2p = a2p
        self.p2p = p2p
        self.aft = aft
        self.pft = pft
        self.home_a3p_adj = home_a3p_adj if home_a3p_adj is not None else 0
        self.home_a2p_adj = home_a2p_adj if home_a2p_adj is not None else 0
        self.home_aft_adj = home_aft_adj if home_aft_adj is not None else 0

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

        table_cols = ['W', 'L', 'PCT', 'GB', 'PF', 'PA', 'PD']

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
                gb = (first_delta - (team.wins - team.losses))/2
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
        details = self.next_game_details()

        if details is None:
            print(f'No remaining games.')
            return

        round_no = details['round-no']
        game_no = details['game-no']
        home = self.members[details['home-name']]
        away = self.members[details['away-name']]

        # How many 3-point attempts for each team?
        home_3pa = resolve(self.a3p, home.a3p_for, away.a3p_against)
        away_3pa = resolve(self.a3p, away.a3p_for, home.a3p_against)

        # How many 2-point attempts for each team?
        home_2pa = resolve(self.a2p, home.a2p_for, away.a2p_against)
        away_2pa = resolve(self.a2p, away.a2p_for, home.a2p_against)

        # How many free-throw attempts for each team?
        home_fta = resolve(self.aft, home.aft_for, away.aft_against)
        away_fta = resolve(self.aft, away.aft_for, home.aft_against)

        # 3-point pct for each team
        home_3pp = resolve(self.p3p, home.p3p_for, away.p3p_against)
        away_3pp = resolve(self.p3p, away.p3p_for, home.p3p_against)

        # 2-point pct for each team
        home_2pp = resolve(self.p2p, home.p2p_for, away.p2p_against)
        away_2pp = resolve(self.p2p, away.p2p_for, home.p2p_against)

        # free-throw pct for each team
        home_ftp = resolve(self.pft, home.pft_for, away.pft_against)
        away_ftp = resolve(self.pft, away.pft_for, home.pft_against)

        home_points = 0
        for _ in range(int(home_3pa) + 1):
            if rand() <= home_3pp:
                home_points += 3

        for _ in range(int(home_2pa) + 1):
            if rand() <= home_2pp:
                home_points += 2

        for _ in range(int(home_fta) + 1):
            if rand() <= home_ftp:
                home_points += 1

        away_points = 0
        for _ in range(int(away_3pa) + 1):
            if rand() <= away_3pp:
                away_points += 3

        for _ in range(int(away_2pa) + 1):
            if rand() <= away_2pp:
                away_points += 2

        for _ in range(int(away_fta) + 1):
            if rand() <= away_ftp:
                away_points += 1

        over_times = 0
        while home_points == away_points:
            over_times += 1
            over_time = 5 / 48
            for _ in range(int(home_3pa * over_time) + 1):
                if rand() <= home_3pp:
                    home_points += 3

            for _ in range(int(home_2pa * over_time) + 1):
                if rand() <= home_2pp:
                    home_points += 2

            for _ in range(int(home_fta * over_time) + 1):
                if rand() <= home_ftp:
                    home_points += 1

            for _ in range(int(away_3pa * over_time) + 1):
                if rand() <= away_3pp:
                    away_points += 3

            for _ in range(int(away_2pa * over_time) + 1):
                if rand() <= away_2pp:
                    away_points += 2

            for _ in range(int(away_fta * over_time) + 1):
                if rand() <= away_ftp:
                    away_points += 1

        score_str = f'{home.name} {home_points} -- {away.name} {away_points}'

        if over_times > 0:
            score_str += f' ({over_times} OT)'
        print(f'\n{"*" * 100}\n'
              f'Round {round_no}, Game No {game_no}: {score_str}\n'
              f'{"*" * 100}\n')

        self.results[game_no]['home-score'] = home_points
        self.results[game_no]['away-score'] = away_points
        round_no = self.results[game_no]['round-no']

        line = f'{round_no},{game_no},{home.name},{home_points},{away.name},{away_points}\n'
        with open(self.results_file, 'a') as f:
            f.write(line)

        home.update_results(
            game_id=game_no, opponent=away, score_for=home_points, score_against=away_points
        )

        away.update_results(
            game_id=game_no, opponent=home, score_for=away_points, score_against=home_points
        )

        self.print_standings()
