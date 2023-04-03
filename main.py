import discord as dc
import os
from keep_alive import keep_alive
import random
from replit import db
from discord.ext import commands

last_number_of_people = 0
VOICE_CHANNEL_ID = 689208715685265436
TEXT_CHANNEL_ID = 689884353601470465

intents = dc.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

##########################################################
#              BOT COMMANDS
##########################################################

# Custom help command 
class MyHelp(commands.HelpCommand):
  async def send_bot_help(self, mapping):
      embed = dc.Embed(title="Help")
      for cog, command_list in mapping.items():
         command_signatures = [self.get_command_signature(c) for c in command_list]
         if command_signatures:
              cog_name = getattr(cog, "qualified_name", "No Category")
              embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

      channel = self.get_destination()
      await channel.send(embed=embed)

bot.help_command = MyHelp()

# add quote
@bot.command(name='repeatinred',
             description='Adds a new quote to the possible bot reply list.')
async def repeat_in_red(ctx, *args):
  new_quote = ' '.join(args)
  async with ctx.channel.typing():
    add(new_quote)
  await ctx.send("New quote added.")

def create_quote_list_embed(title):
  reply_list = db["frases"]
  embed = dc.Embed(title=title, color=0xDB9D47)
  embed.set_author(
    name="Beatrice",
    icon_url="https://pbs.twimg.com/media/E0eJWJAXMAIXCGz.jpg")
  for i, item in enumerate(reply_list):
    embed.add_field(name=str(i), value=item, inline=False)
  return embed

# edit quote
@bot.command(name='edit', description='Replaces the quote at the given index with the given quote')
async def edit(ctx, idx, *quote):
  db["frases"][int(idx)] = ' '.join(quote)
  embed = create_quote_list_embed("Quote list after modifying quote " + idx)
  await ctx.send("arreglao")
  await ctx.send(embed=embed)


# remove quote
@bot.command(name='remove',
             description='Removes a quote from the list at the given index.')
async def remove(ctx, *args):
  async with ctx.channel.typing():
    idx = int(args[0]) # Quote to remove from the list
    await ctx.send('Removing quote ' + args[0])
    db["frases"].pop(idx)
    embed = create_quote_list_embed("Quote list after removing quote " + args[0])
    await ctx.send(embed=embed)
  


# list quotes
@bot.command(name='list',
             description='Lists all possible quotes the bot can use.')
async def list(ctx, *args):
  async with ctx.channel.typing():
    embed = create_quote_list_embed("Current bot replies")
  await ctx.send(embed=embed)


# # get voice channel
# @bot.command(name='getvoice')
# async def get_voice_channel(ctx, *args):
#   print("Args: ", ' '.join(args))

# # get text channel
# @bot.command(name='gettext')
# async def get_text_channel(ctx, *args):
#   print("Args: ", ' '.join(args))

#   # change voice channel
# @bot.command(name='voice')
# async def change_voice_channel(ctx, *args):
#   print("Args: ", ' '.join(args))

# # change text channel
# @bot.command(name='text')
# async def change_text_channel(ctx, *args):
#   print("Args: ", ' '.join(args))

canales = {
  'cafeteria': 689208715685265436,
}


def add(frase):
  if ("frases" not in db.keys()):
    db["frases"] = [frase]
  else:
    db["frases"].append(frase)
  return


def choose_response(member):
  print(member.name)
  chosen_reply = random.choice(db["frases"])
  chosen_reply = chosen_reply.replace('<X>', str(member.name))
  chosen_reply += " @everyone"
  return chosen_reply


def add_new_reply(msg):
  if (msg.lower().startswith('!repeatinred')):
    return True
  else:
    return False


def show_list(msg):
  if (msg.lower().startswith('!list')):
    return True
  else:
    return False


def show(list):
  bot_replies = "Current bot replies:\n\n"
  for i, item in enumerate(list):
    bot_replies += "\t " + i + " -> " + item + "\n"
  return bot_replies


##########################################################
#              BOT EVENTS
##########################################################


@bot.event
async def on_ready():
  print("Hola: ", bot.guilds)


@bot.event
async def on_voice_state_update(member, before, after):
  global last_number_of_people

  print(member)
  channel = bot.get_channel(VOICE_CHANNEL_ID)
  members = channel.members
  print("Gente ahora: ", len(members), "  --  Gente antes: ",
        last_number_of_people)

  if (len(members) == 1 and last_number_of_people == 0):

    channel = dc.utils.get(bot.get_all_channels(), id=TEXT_CHANNEL_ID)
    bot_response = choose_response(member)
    await channel.send(bot_response)

  last_number_of_people = len(members)


keep_alive()
bot.run(os.environ['TOKEN'])
