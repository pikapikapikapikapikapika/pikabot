import shelve

class Whomst(object):
  def __init__(self, shelfname):
    self.shelfname = shelfname

  def get(self, game):
    with shelve.open(self.shelfname) as whomst:
      return whomst.get(game, [])

  def user_for_game(self, user, game):
    with shelve.open(self.shelfname) as whomst:
      return game in whomst and user.mention in whomst[game]

  def update(self, user, game):
    self.add_game(game)
    is_opted_in = self.user_for_game(user, game)
    with shelve.open(self.shelfname) as whomst:
      if is_opted_in:
        whomst[game] = [u for u in whomst[game] if u != user.mention]
      else:
        whomst[game] = whomst[game] + [user.mention]

  def add_game(self, game):
    with shelve.open(self.shelfname) as whomst:
      if game not in whomst:
        whomst[game] = []
    
  def remove_game(self, game):
    with shelve.open(self.shelfname) as whomst:
      whomst.pop(game)

  def games(self):
    with shelve.open(self.shelfname) as whomst:
      return [k for k in whomst.keys()]
