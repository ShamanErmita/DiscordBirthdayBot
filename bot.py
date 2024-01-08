import discord
from discord.ext import commands,tasks
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='&', intents=intents)

try:
    with open('birthdays.json','r') as file:
        birthdays_data = json.load(file)
except FileNotFoundError:
    birthdays_data = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    check_birthdays.start()

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency*1000)
    await ctx.send(f'Pong! Latência: {latency} ms')

@bot.command(name='set_birthday')
async def set_birthday(ctx, date: str, mentioned_person: discord.Member):
    username = mentioned_person.display_name
    birthdays_data[username] = {'date': date}
    save_birthdays()
    await ctx.send(f'O Aniversário de {username} que é na data {date} foi adicionado! 🥳')


@bot.command(name='list_birthdays')
async def list_birthdays(ctx):
    birthday_list = "\n".join([f"{username}: {data['date']}" for username, data in birthdays_data.items()])
    await ctx.send(f"Aniversários até agora:\n{birthday_list}")


def save_birthdays():
    with open('birthdays.json','w') as file:
        json.dump(birthdays_data,file)

@tasks.loop(hours=24)
async def check_birthdays():
    today = datetime.now().strftime('%d/%m')

    for username, birthday in birthdays_data.items():
        if birthday['date'] == today:
            channel_name = 'aniversários🎉'
            channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
            if channel:
                await channel.send(f'🎉 Parabéns {username} 🎉\n Espero que tenhas um dia top, fica bem e aproveita o teu dia 🎂\n@everyone deem aí os parabéns ❤')


bot.run('YOUR DISCORD BOT TOKEN HERE')