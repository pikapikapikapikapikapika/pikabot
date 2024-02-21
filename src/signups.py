import discord
import dotenv
import os

from . import whomst

dotenv.load_dotenv()

PIKABOT_WHOMST = os.getenv('PIKABOT_WHOMST')

whomst = whomst.Whomst(PIKABOT_WHOMST)

class GameButton(discord.ui.Button):
  def __init__(self, user, game):
    discord.ui.Button.__init__(self)
    self.user = user
    self.game = game

    self.label = game
    self.style = (
      discord.ButtonStyle.green
      if whomst.user_for_game(user, game)
      else discord.ButtonStyle.primary
    )

  async def callback(self, interaction):
    whomst.update(interaction.user, self.game)
    await interaction.response.edit_message(view=GameView(self.user))

class GameView(discord.ui.View):
  def __init__(self, user):
    discord.ui.View.__init__(self)
    self.user = user
    for game in whomst.games():
      self.add_item(GameButton(user, game))
