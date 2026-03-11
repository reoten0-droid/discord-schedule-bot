import discord
import requests
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GAS_URL = os.getenv("GAS_WEBHOOK_URL")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TARGET_CHANNEL_NAME = "予定書き込み"

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.guild:
        return

    if message.channel.name != TARGET_CHANNEL_NAME:
        return

    try:
        lines = message.content.replace("：", ":").split("\n")
        data = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        date = data.get("日付", "")
        time = data.get("時間", "")
        who = data.get("誰", "")
        content = data.get("内容", "")

        if not date or not time or not who or not content:
            raise ValueError("必要項目不足")

        payload = {
            "date": date,
            "time": time,
            "who": who,
            "content": content
        }

        response = requests.post(GAS_URL, json=payload, timeout=10)

        if response.status_code == 200:
            await message.add_reaction("✅")
        else:
            await message.channel.send("登録に失敗したよ。GAS側を確認してね。")
            print("GASエラー:", response.status_code, response.text)

    except Exception as e:
        await message.channel.send(
            "書き方はこちらです。\n"
            "日付:2026/03/29\n"
            "時間:11:00\n"
            "誰:あにき\n"
            "内容:退去立会"
        )
        print("Error:", e)

client.run(TOKEN)
