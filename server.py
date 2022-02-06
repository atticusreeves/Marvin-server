import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
#import os
import pandas as pd
import wikipedia
from dotenv import load_dotenv
from neuralintents import GenericAssistant
import nltk
import requests, json
#Atticusr31!
###-------DIRECT DATA-------
Help_list = {
    "?marvin": "talk to marvin",
    "?help": "help",
    "?search": "search something on Wikipedia",
    "ping": "the ping",
    "?clear": "clear message (elder, administrator)",
    "?spam": "spam (administrator)",
    "?weather": "weather"
}


nltk.download('omw-1.4')
chatbot = GenericAssistant('intents.json')

#save + train models
chatbot.train_model()
chatbot.save_model()


client = commands.Bot(command_prefix = '?')
API_KEY = 'OTEyMDI1ODIzMzY2NzcwNzY5.YZp8PA.cJk_nAPzIEdXgC-LpQup0xVPjpE'
status = cycle(['Music', 'Minecraft'])
#found bug ->
#data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSakkbs0Zra08HISjFjptCBxc3y52B4xA5uPITV84Yfe5o1xV0eD88Mj3NrlWzc2hcGR3rTC1BsEhJ2/pub?gid=0&single=true&output=csv', sep=",")

load_dotenv()
@client.event
async def on_ready():
    change_status.start()
    print('Marvin has entered the chat')
#@client.command()
#async def clear(ctx, amount=5):
    #await ctx.channel.purge(limit=amount)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("?marvin"):
        response = chatbot.request(message.content[:1234567])
        await message.channel.send(response)
    elif message.content.startswith("?clear"):
        await message.channel.purge(limit=5)
    elif '?search' in message.content:
        search = wikipedia.summary(message.content, sentences='2')
        await message.channel.send(f'here : {search}')
    elif message.content.startswith("?help"):
        await message.channel.send(f':\n {Help_list}\n')
    elif message.content.startswith("?spam"):
        spam_bug_fix = message.content.replace("?spam", "")
        for i in range(10):
            await message.channel.send(f"spamming:\n {spam_bug_fix}")
    elif message.content.startswith("?ping"):
        await message.channel.send(f'Ping is {round(client.latency * 1000)}ms')
    elif message.content.startswith("?weather"):
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        CITY = "Indianapolis"
        API_KEY = "94cebd7308ad000152e32ac01b35188b"
        URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            report = data['weather']
            await message.channel.send(f'--(Indianapolis)--\n {main} \n -------------------')
    else:
        pass

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#ERROR WITH .CLEAR NEEDS DEBUGGING!!!!!

#dictionary (will soon be part of ai)

client.run(API_KEY)
