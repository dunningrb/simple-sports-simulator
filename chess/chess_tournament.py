from league.league import League
from chess.chess_player import ChessPlayer
from utils.utils import rand

import math


class ChessTournament(League):
    def __init__(self, *, name, season, rotations, results_file, players):

        super(ChessTournament, self).__init__(
            name=name, season=season, rotations=rotations, results_file=results_file, members=players, 
            member_type=ChessPlayer
        )

        self.elo_avg = sum([p.elo for p in self.members.values()]) / len(self.members)
        self.win_factors = (0.0198, 0.00687, 0.000421)

        self.option_methods['Standing'] = self.print_standing
        self.option_methods['Play Next Match'] = self.play_next_match

        self.print_menu()

    @property
    def standing(self):
        def _sort_items(p):
            return {'W': p.wins, 'L': p.losses, 'PTS': p.points, 'SBS': p.sonneborn_berger, 'WB': p.wins_black}

        return {k: v for k, v in sorted({p: _sort_items(p) for p in self.members.values()}.items(),
                                        key=lambda x: (x[1]['PTS'], x[1]['W'], x[1]['SBS'], x[1]['WB'], -x[1]['L']),
                                        reverse=True)}

    def play_next_match(self):
        details = self.next_game_details()

        if details is None:
            print(f'No remaining matches.')
            return

        round_no = details['round-no']
        game_no = details['game-no']
        white = self.members[details['home-name']]
        black = self.members[details['away-name']]

        elo_diff = abs(white.elo - black.elo)
        elo_avg = min((white.elo + black.elo) / 2, self.elo_avg)

        e = 1 / (1 + 10 ** (-elo_diff / 400))
        pw = 1 / (1 + math.exp(self.win_factors[0] - self.win_factors[1] * elo_diff + self.win_factors[2] * elo_avg))
        pd = (1 - pw) * 2 * (e - pw) / (1 - pw)

        if white.elo > black.elo:
            pw_1 = pw
        else:
            pw_1 = (1 - pw - pd)

        pw_1 += 0.03
        pd += pw_1
        rn = rand()

        if 0 <= rn < pw_1:
            white_result = 1
            black_result = 0
            print(f'Round {round_no}, Game No {game_no}: {white.name} defeats {black.name} with the white pieces.')
        elif pw_1 <= rn < pw_1 + pd:
            white_result = black_result = 0.5
            print(f'Round {round_no}, Game No {game_no}: {white.name} and {black.name} play to a draw.')
        else:
            white_result = 0
            black_result = 1
            print(f'Round {round_no}, Game No {game_no}: {white.name} defeats {black.name} with the black pieces.')

        line = f'{round_no},{game_no},{white.name},{white_result},{black.name},{black_result}\n'
        with open(self.results_file, 'a') as f:
            f.write(line)

        white.update_results(
            game_id=game_no, location='white', opponent=black.name, score_for=white_result, score_against=black_result)
        black.update_results(
            game_id=game_no, location='black', opponent=white.name, score_for=black_result, score_against=white_result)

        self.print_standing()

    def print_standing(self):
        max_len = -1
        for name in self.members:
            max_len = max(max_len, len(name))

        sp3 = ' ' * 3
        sp4 = ' ' * 4
        standing_str = 'Name ' + ' ' * (max_len - 1)
        standing_str += 'W' + sp3 + 'L' + sp3 + 'D' + sp3 + 'PTS' + sp3 + 'SBS' + sp4 + 'WB\n'
        standing_str += '-' * len(standing_str)
        standing_str += '\n'

        for player in self.standing:
            standing_str += (player.name + ' ' * (4 + max_len - len(player.name)) +
                             str(player.wins) + ' ' * (4 - len(str(player.wins))) +
                             str(player.losses) + ' ' * (4 - len(str(player.losses))) +
                             str(player.ties) + ' ' * (4 - len(str(player.ties))) +
                             str(player.points) + ' ' * (6 - len(str(player.points))) +
                             str(player.sonneborn_berger) + ' ' * (7 - len(str(player.sonneborn_berger))) +
                             str(player.wins_black) + '\n')

        print(f'{"=" * 78}\n{self.name} Current Standing:\n\n{standing_str}\n\n{"=" * 78}\n')
