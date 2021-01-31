class Team:

    def __init__(self, *, name):
        self.name = name
        self.results = dict()

    @property
    def games_played(self):
        return len(self.results)

    @property
    def score_for(self):
        return sum([r['score-for'] for r in self.results.values()])

    @property
    def score_against(self):
        return sum([r['score-against'] for r in self.results.values()])

    @property
    def score_diff(self):
        return self.score_for - self.score_against

    @property
    def wins(self):
        return sum([1 for r in self.results.values() if r['score-for'] > r['score-against']])

    @property
    def losses(self):
        return sum([1 for r in self.results.values() if r['score-for'] < r['score-against']])

    @property
    def ties(self):
        return sum([1 for r in self.results.values() if r['score-for'] == r['score-against']])

    @property
    def win_pct(self):
        try:
            return self.wins / self.games_played
        except ZeroDivisionError:
            return 0.000

    def update_results(
            self, *, date=None, game_id, location=None, opponent, score_for=None,
            score_against=None
    ):
        score_for = int(score_for) if score_for is not None else score_for
        score_against = int(score_against) if score_against is not None else score_against
        self.results[game_id] = {
            'date': date, 'location': location, 'opponent': opponent, 'score-for': score_for,
            'score-against': score_against
        }