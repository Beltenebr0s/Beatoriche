import discord as dc
import os
from keep_alive import keep_alive
import random
from replit import db
from dc.ext import commands

last_number_of_people = 0

client = dc.Client(intents=dc.Intents.default())
bot = commands.Bot(command_prefix='!')
# add quote
# help
# remove quote 
# list quotes 
# change voice channel 
# change text channel 

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
  # chosen_reply += " @everyone"
  return chosen_reply


def add_new_reply(msg):
  if (msg.lower().startswith('!repeatinred')):
    return True
  else:
    return False

def show_list(msg):
  if(msg.lower().startswith('!list')):
    return True
  else:
    return False
def show(list):
  bot_replies = "Current bot replies:\n\n"
  for i, item in enumerate(list):
    bot_replies += "\t " + i + " -> " + item + "\n"
  return bot_replies

@client.event
async def on_ready():
  print("Holaa")


@client.event
async def on_message(msg):
  print(msg.content)
  if (msg.author != client.user):
    if add_new_reply(msg.content):
      add(msg.content.split('!repeatinred', 1)[1])
      print(db["frases"])
    if show_list(msg.content):
      reply_list = show(db["frases"])
      await msg.channel.send(reply_list)
      


@client.event
async def on_voice_state_update(member, before, after):
  global last_number_of_people

  print(member)
  channel = client.get_channel(689208715685265436)
  members = channel.members
  print("Gente ahora: ", len(members), "  --  Gente antes: ",
        last_number_of_people)

  if (len(members) == 1 and last_number_of_people == 0):

    channel = dc.utils.get(client.get_all_channels(), id=689884353601470465)
    bot_response = choose_response(member)
    await channel.send(bot_response)

  last_number_of_people = len(members)


keep_alive()
client.run(os.environ['TOKEN'])