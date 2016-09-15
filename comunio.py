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
    self.__dict__ = {value:key for value, key in enumerate(arg)}

  def __getattr__(self, name):
    if name in self:
      return name
    raise AttributeError

POSITION_TYPE = Enum(["S", "M", "D", "GK"])
POSITION_STR = {POSITION_TYPE.S: "Striker", 
                POSITION_TYPE.M: "Middlefielder",
                POSITION_TYPE.D: "Defender",
                POSITION_TYPE.GK: "Goal Keeper"}

OWNER_TYPE = Enum(["M", "U", "C"])
OWNER_STR = {OWNER_TYPE.M: "Me", OWNER_TYPE.U: "User", OWNER_TYPE.C: "Computer"}

class Player(object):
  """docstring for Player"""
  def __init__(self, name, position, owner='M', value=0, point=0):
    self._name = name
    self._owner = OWNER_TYPE[owner]
    self._value = value
    self._point = point
    self._position = POSITION_TYPE[position]

  # properties
  @property
  def name(self):
    return _name
  @property
  def owner(self):
    return _owner

  @property
  def value(self):
    return _value

  @property
  def point(self):
    return _point

  @property
  def position(self):
    return _position

  def __str__(self):
    return "Player {0}: (owner: {1}) (value: {2}) (point:{3}) (position: {4})" \
      .format(self.name, OWNER_STR[self.owner], \
              self.value, self.point, POSITION_STR[self.position])


class Team:
  def __init__(self, teamfile = 'team', balance=0):
    self._balance = balance
    self._players = {}
    with open(teamfile, 'r') as f:
      reader = csv.reader(f,  delimiter=',')
      header = reader[0]
      for line in reader:
        self._players[line[]] = 



def main():
  team = Team()

if __name__ == "__main__":
  main()








