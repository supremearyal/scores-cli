import urllib.request
import datetime
import json

scores_url = 'http://data.nba.com/jsonp/5s/json/cms/noseason/scores/gametracker.json?callback=jsonCB'

class Score:
    def __init__(self, home, away, home_score, away_score, period, time_left, game_start):
        self.home = home
        self.away = away
        self.home_score = home_score
        self.away_score = away_score
        self.period = period
        self.time_left = time_left
        self.game_start = game_start
        self.game_over = len(self.time_left) == 0

    def __str__(self):
        a = self.home
        b = self.away
        sa = self.home_score
        sb = self.away_score
        if sb > sa:
            a, b = b, a
            sa, sb = sb, sa
        if self.game_over:
            final_fmt = '{} - {} \t[{}]\n{} - {}'
            return final_fmt.format(a, sa, self.period, b, sb)
        else:
            live_fmt = '{} - {} \t[{} ({})]\n{} - {}'
            return live_fmt.format(a, sa, self.period, self.time_left, b, sb)

with urllib.request.urlopen(scores_url) as f:
    response = f.read().decode('utf-8').replace('jsonCB(', '').strip()[:-2]
    parsed_response = json.loads(response)
    games = parsed_response['sports_content']['game']
    scores = []
    for game in games:
        home = game['home']['abbreviation'].strip()
        home_score = game['home']['score'].strip()
        home_score = 0 if home_score == '' else int(home_score)
        away = game['visitor']['abbreviation'].strip()
        away_score = game['visitor']['score'].strip()
        away_score = 0 if away_score == '' else int(away_score)
        period = game['period_time']['period_status'].strip()
        time_left = game['period_time']['game_clock'].strip()
        game_date = game['date'].strip()
        game_time = game['time'].strip()
        game_start = datetime.datetime(int(game_date[:4]),
                                       int(game_date[4:6]),
                                       int(game_date[6:]),
                                       int(game_time[:2]),
                                       int(game_time[2:]))
        scores.append(Score(home, away, home_score, away_score, period, time_left, game_start))

    today = sorted([s.game_start for s in scores])[-1]
    today_scores = [s for s in scores if today.date() == s.game_start.date()]
    print('\n\n'.join(str(score) for score in today_scores))
