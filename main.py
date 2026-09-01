import discord
from discord.ext import commands
from discord import app_commands
import asyncio

import os
from dotenv import load_dotenv 

from lostcity.lostcity import LostCity

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

async def main():
    client=discord.Client(intents=intents)
    tree=app_commands.CommandTree(client)

    load_dotenv()
    bot.run(os.environ.get('TOKEN'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} \nID: {bot.user.id}')
    print('================')
    await bot.add_cog(LostCity(bot))
    synced=await bot.tree.sync()
    print("Loaded Slash Command: " + str(len(synced))) 
    
@bot.command()
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"synced: {len(synced)}")


# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
