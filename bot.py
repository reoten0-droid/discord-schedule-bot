import discord
import requests
import os

TOKEN = os.getenv("TOKEN")
GAS_URL = os.getenv("GAS_URL")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot起動")

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.name == "予定書き込み":

        try:
            parts = message.content.split(" ")

            data = {
                "date": parts[0],
                "time": parts[1],
                "who": parts[2],
                "content": " ".join(parts[3:])
            }

            requests.post(GAS_URL, json=data)

            await message.add_reaction("✅")

        except:
            await message.channel.send("書き方：2026/03/20 18:00 あにき 買い物")

client.run(TOKEN)
