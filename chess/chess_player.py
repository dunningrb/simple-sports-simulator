from team.team import Team


class ChessPlayer(Team):
    def __init__(self, *, name, elo):
        super(ChessPlayer, self).__init__(name=name)
        self.elo = elo

    @property
    def points(self):
        return self.wins + 0.5 * self.ties

    @property
    def sonneborn_berger(self):
        return 0

    @property
    def wins_black(self):
        return 0