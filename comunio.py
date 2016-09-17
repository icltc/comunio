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
    self._name = name
    self._owner = OWNER_TYPE[owner]
    self._value = float(value)
    self._point = float(point)
    self._position = POSITION_TYPE[position]

  # properties
  @property
  def name(self):
    return self._name
  @property
  def owner(self):
    return self._owner

  @property
  def value(self):
    return self._value

  @property
  def point(self):
    return self._point

  @property
  def position(self):
    return self._position

  @property
  def cp(self):
    return self._point / self._value

  def __str__(self):
    return "Player {0}: (owner: {1}) (value: {2}) (point:{3}) (position: {4})" \
      .format(self.name, OWNER_STR[self.owner], \
              self.value, self.point, POSITION_STR[self.position])


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

  def __str__(self):
    return "Team '{2}' has balance of {0} and value of {1}\n----------------------------\n" \
      .format(self._balance, self._value, self._name) + "\n".join(str(i) for i in self._players)

  def sort(self, position = False):
    print "rank the whole team or based on the position"


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
    print "recommend to buy players just based on the current market"

  def rebalance(self):
    print "recommend to buy players from market and sell own players to fund (stick to current formation)"

  def rebalance_smart(self):
    print "recommend to buy players from market and sell own players to fund (able to change formation)" 


def main():
  game = Comnunio

if __name__ == "__main__":
  main()








