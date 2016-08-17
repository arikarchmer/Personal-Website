
import csv


class Player():

    def __init__(self, playername, vor, adp, adpdiff, dropoff, risk, picked, playerposition):
        self.playername = playername
        self.vor = float(vor)
        self.adp = float(adp) if not adp == 'null' else 1000
        self.adpdiff = float(adpdiff) if not adpdiff == 'null' else 0
        self.dropoff = float(dropoff) if not dropoff == 'null' else 0
        self.risk = float(risk) if not risk == 'null' else 1000
        self.picked = picked
        self.playerposition = playerposition
        self.score = self.get_pick_score()

    def __repr__(self):
        return self.playerposition + ', ' + self.playername + ', score: ' + str(self.get_pick_score()) + \
               ', adp: ' + str(self.adp) + ", adpdiff: " + str(self.adpdiff) + ', dropoff: ' + str(self.dropoff) + ', risk: ' + str(self.risk)

    def get_pick_score(self):
        vor = float(self.vor) / 12
        sleeper_score = (pick_num - (float(self.adp) + float(self.adpdiff))) if float(self.adp) - pick_num < 12 else -12
        dropoff = float(self.dropoff) / 12
        risk = 5 - self.risk / pick_num / 12 if not self.risk == 'null' else 0

        return vor + sleeper_score + dropoff + risk + float(pick_num / 12)


def read(projections):
    with open(projections) as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_players.append(Player(row['playername'], row['vor'],
                row['adp'], row['adpdiff'], row['dropoff'], row['risk'], row['picked'], row['playerposition']))


def calc():
    players = []
    global all_players
    for p in all_players:
        if p.picked == 'FALSE':
            str_adp = p.adp
            str_adp_diff = p.adpdiff
            if not str_adp_diff == 'null' and not str_adp == 'null':
                adp = float(str_adp)
                if adp < 144:
                    players.append(p)
    rb = 1
    wr = 1
    qb = 1
    te = 1
    for p in sorted(players, key=lambda p: p.get_pick_score(), reverse=True):
        if p.playerposition == 'RB' and rb < 6:
            print(str(rb) + ' ' + p.__repr__())
            rb += 1
        if p.playerposition == 'WR' and wr < 6:
            print(str(wr) + ' ' + p.__repr__())
            wr += 1
        if p.playerposition == 'QB' and qb < 4:
            print(str(qb) + ' ' + p.__repr__())
            qb += 1
        if p.playerposition == 'TE' and te < 4:
            print(str(te) + ' ' + p.__repr__())
            te += 1


def new_pick():
    global pick_num
    pick_num += 1
    player = raw_input('pick: ')
    for p in all_players:
        if p.playername == player:
            print('picked ' + player)
            p.picked = 'TRUE'
    return player


def draft():
    print('================================================ ' + str(pick_num) + ' ===============================================')
    calc()
    new_pick()
    draft()


if __name__ == '__main__':
    pick_num = 1
    all_players = []
    read('FF_projections.csv')
    draft()