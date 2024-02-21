import discord
import dotenv
import os

from discord.ext import commands

from src import whomst, signups

dotenv.load_dotenv()

PIKABOT_KEY = os.getenv('PIKABOT_KEY')
PIKABOT_GUILDS = [int(guild_id) for guild_id in os.getenv('PIKABOT_GUILDS').split(',')]
PIKABOT_WHOMST = os.getenv('PIKABOT_WHOMST')

whomst = whomst.Whomst(PIKABOT_WHOMST)
bot = discord.Bot()

def game_autocomplete(ctx):
  return [game for game in whomst.games() if ctx.value in game]

@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")

@bot.slash_command(
  name='listgames',
  description='list games',
  guild_ids=PIKABOT_GUILDS,
)
async def listgames_cmd(ctx):
  print(f'received /listgames - {ctx.user.name}')
  await ctx.send_response(f'{", ".join(whomst.games())}', ephemeral=True)

@bot.slash_command(
  name='addgame',
  description='add game to list',
  guild_ids=PIKABOT_GUILDS,
  options=[discord.Option(name='game', description='game', required=True)],
)
async def addgame_cmd(ctx, game):
  print(f'received /addgame {game} - {ctx.user.name}')
  whomst.add_game(game)
  await ctx.send_response(f'added {game}', ephemeral=True)

@bot.slash_command(
  name='removegame',
  description='remove game from list',
  guild_ids=PIKABOT_GUILDS,
  options=[discord.Option(name='game', autocomplete=game_autocomplete, required=True)],
)
async def removegame_cmd(ctx, game):
  print(f'received /removegame {game} - {ctx.user.name}')
  whomst.remove_game(game)
  await ctx.send_response(f'removed {game}', ephemeral=True)
  
@bot.slash_command(
  name='setup',
  description='Opt in to pings for games',
  guild_ids=PIKABOT_GUILDS,
)
async def setup_cmd(ctx):
  print(f'received /setup - {ctx.user.name}')
  await ctx.send_response('Opt in to pings for games:', ephemeral=True, view=signups.GameView(ctx.user))

@bot.slash_command(
  name='w',
  description='short for "when"',
  guild_ids=PIKABOT_GUILDS,
  options=[discord.Option(name='game', autocomplete=game_autocomplete, default='games')],
)
@bot.slash_command(
  name='when',
  description='ping people who might be up for games',
  guild_ids=PIKABOT_GUILDS,
  options=[discord.Option(name='game', autocomplete=game_autocomplete, default='games')],
)
@commands.cooldown(1, 10, commands.BucketType.try_value)
async def when_cmd(ctx, game):
  print(f'received /when {game} - {ctx.user.name}')
  gamers = whomst.get(game)
  interaction = await ctx.send_response(f'when {game} {" ".join(gamers)}')
  response = await interaction.original_response()

  emoji = (
    discord.utils.get(ctx.guild.emojis, name='greenman')
    or discord.utils.get(ctx.guild.emojis, name='itiswhatitis')
  )
  await response.add_reaction(emoji)


bot.run(PIKABOT_KEY)