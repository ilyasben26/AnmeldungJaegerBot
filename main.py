import discord
from discord.ext import tasks
import os
import json
from datetime import datetime
import asyncio
import pytz
from driver_func import check, check_all
from format_func import format_data, check_availability

BerlinTz = pytz.timezone("Europe/Berlin")

#run keep alive
import keep_alive

keep_alive.keep_alive()

# load the data file
with open('instructions.json') as json_file:
  data = json.load(json_file)

# Discord Part
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  send_message.start()


@tasks.loop(minutes=5)
async def send_message():
  channel_debug = discord.utils.get(client.get_all_channels(), name='debug')
  current_time = datetime.now(BerlinTz)
  formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
  await channel_debug.send(f'{formatted_time}: Checking all cities ...')
  response_task = asyncio.create_task(check_all(data))
  await response_task
  #response = await check_all()
  response = response_task.result()
  city_availability = check_availability(response)
  await channel_debug.send(city_availability)
  await channel_debug.send(response)
  for entry in city_availability:
    if entry['send_msg_flag'] == True:
      print(entry['city'], "is available")
      channel_city = discord.utils.get(client.get_all_channels(),
                                       name=entry['city'].lower())
      filtered_response = [
        element for element in response
        if element['city'].lower() == entry['city'].lower()
      ]
      formatted_output = format_data(filtered_response)
      await channel_city.send(formatted_output)
    else:
      print(entry['city'], "is NOT available")


@send_message.before_loop
async def before_send_message():
  await client.wait_until_ready()


client.run(os.environ['TOKEN'])
