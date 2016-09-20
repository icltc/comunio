import csv

# class to read csv file into structured object
class CsvReader:
  def __init__(self, filename, delimiter=',', quotechar='|'):
    with open(filename, 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
      rows = [row for row in spamreader]
      self._header = rows[0]
      self._rows = rows[1:]

  @property
  def header(self):
      return self._header

  @property
  def rows(self):
    return self._rows


class Enum(set):
  def __init__(self, arg):
    super(Enum, self).__init__()
    #print self.__dict__
    self.__dict__ = {value:key for key, value in enumerate(arg)}

  def __getattr__(self, name):
    if name in self:
      return name
    raise AttributeError

  def __getitem__(self, name):
    if name in self.__dict__:
      return self.__dict__[name]

    raise AttributeError

POSITION_TYPE = Enum(["S", "M", "D", "GK"])
POSITION_STR = {POSITION_TYPE.S: "Striker", 
                POSITION_TYPE.M: "Midfielder",
                POSITION_TYPE.D: "Defender",
                POSITION_TYPE.GK: "Goal Keeper"}

OWNER_TYPE = Enum(["M", "U", "C"])
OWNER_STR = {OWNER_TYPE.M: "Me", OWNER_TYPE.U: "User", OWNER_TYPE.C: "Computer"}

class Player:
  """docstring for Player"""
  def __init__(self, name, position, value=0.0, point=0.0, owner='M'):
    self.__dict__["name"] = name
    self.__dict__["owner"] = OWNER_TYPE[owner]
    self.__dict__["value"] = float(value)
    self.__dict__["point"] = float(point)
    self.__dict__["position"] = POSITION_TYPE[position]
    self.__dict__["target"] = False
    self.__dict__["recommend"] = False
    self.__dict__["cp"] = self.point * 100000 / self.value

  # properties
  def __getattr__(self, name):
    if name in self.__dict__:
      return self.__dict__[name]
    raise AttributeError

  def __str__(self):
    return "{0: <32}: {1: <10} - {2:15.0f} {3:5.0f} ({4:.4f}) {5}{6}" \
            .format(self.name + "("+ POSITION_STR[self.position] + ")", OWNER_STR[self.owner], \
              self.value, self.point, self.cp, "" if not self.target else "#", "" if not self.recommend else "*")


class Team:
  @staticmethod
  def _extract_players(teamfile):
    cR = CsvReader(teamfile)
    keys = {key:value for (value,key) in enumerate(cR.header)}
    players = [Player(row[keys['name']], row[keys['position']], \
      row[keys['value']], row[keys['point']], 'M' if 'owner' not in keys else row[keys['owner']]) 
        for row in cR.rows]
    return players

  def __init__(self, teamfile = 'team', balance=0):
    self._name = teamfile
    self._balance = balance
    self._players = self._extract_players(teamfile)
    self._value = reduce(lambda x, y: int(x) + int(y), [ i.value for i in self._players])


  @property
  def players(self):
    return self._players

  def __str__(self):
    return "Team '{2}' has balance of {0} and value of {1}\n".format(self._balance, self._value, self._name) + \
      "----------------------------------------------------------------------------------\n" + \
      "Player(position)                : Owner       -          Value Point (Point/Value)\n" + \
      "----------------------------------------------------------------------------------\n" + \
      "\n".join(str(i) for i in self._players)

  def sort(self, position = False):
    """rank the whole team or based on the position"""
    if not position:
      self._players = sorted(self._players, reverse = True, key=lambda player: player.cp)
    else:
      self._players = sorted(self._players, reverse = True, key=lambda player: (player.position, player.cp))


class Market(Team):
  def __init__(self, marketfile = 'market'):
    Team.__init__(self, marketfile)

class Formation():
  def __init__(self, defender, midfielder, striker):
    self.__dict__['gk'] = 1
    self.__dict__['striker'] = striker
    self.__dict__['midfielder'] = midfielder
    self.__dict__['defender'] = defender

  def __getattr__(self, name):
    if name in self:
      return name
    raise AttributeError

  def __setattr__(self, name, value):
    print "Forbit to change formation by individual position."
    raise AttributeError

  def __str__(self):
    return "{0}-{1}-{2}".format(self.defender, self.midfielder, self.striker)

class Comnunio:

  FORMATIONS = \
  {
    str(i):i for i in [Formation(4,4,2), Formation(3,4,3), \
                        Formation(3,5,2), Formation(4,3,3), Formation(4,5,1)]
  }

  def __init__(self):
    self.team = Team('team', 426700)
    self.market = Market('market')

  def recommend(self):
    print "recommend to buy players just based on the current market (iregardless of the position)"
    self.team.sort()
    self.market.sort()
    print "Listing the team from highest PpV(Point per Value) to lowest"
    print self.team
    print "Listing the market from highest PpV(Point per Value) to lowest"
    print self.market


  def recommend_smart(self, target = 1):
    """target is the number of worst players on each positions that we target to replace"""
    print "recommend to buy players just based on the current market ( corresponding position )"
    self.team.sort(True)
    self.market.sort(True)

    targets = []
    for key, player in enumerate(self.team.players):
      if len(targets)>target and targets[-target][0] == player.position:
        targets[-target] = [player.position, player.cp, key]
      else:
        targets.append([player.position, player.cp, key])

    for player in targets:
      # set target
      self.team.players[player[2]].target = True

      # mark recommendation
      for key, mk in enumerate(self.market.players):
        if mk.position == player[0] and mk.cp > player[1]:
          self.market.players[key].recommend = True

    print self.team
    
    print self.market

  def rebalance(self):
    print "recommend to buy players from market and sell own players to fund (stick to current formation)"

  def rebalance_smart(self):
    print "recommend to buy players from market and sell own players to fund (able to change formation)" 


def main():
  game = Comnunio()
  game.recommend_smart()

if __name__ == "__main__":
  main()








