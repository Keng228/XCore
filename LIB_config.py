import discord
from discord.ext import commands
from discord import Activity, ActivityType
import os

#токен бота
TOKEN = "MTAzNTYyODkxMzY5NjcxMDgyNw.Grbo4M.kkQAiaRxwyiG-qiP1EKMPHSyJcVZEYCh0uUQNU"

#сервера
MY_GUILD = discord.Object(id=915117898232655882)
Alpha = discord.Object(id=814243356497412136)
Servers = [MY_GUILD, Alpha]

#стандартный эмбед
Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

#имя файла
file = "LIB_config.py"

#путь к деректории
daf = os.path.abspath(f'{file}')
j = daf.find(f'{file}')
derectory = daf[:j]

#класс бота
class MyBot(commands.Bot):
    """My Bot"""
    async def on_ready(self):
        print(f"{self.user.name} готов!")
        await self.tree.sync(guild=MY_GUILD)
        await self.tree.sync(guild=Alpha)
        await bot.change_presence(status=discord.Status.online, activity=Activity(name="кофе ☕", type=discord.ActivityType.playing))
    
#сам бот
bot = MyBot(command_prefix="XC.", help_command=None, intents=discord.Intents.all(), test_guilds=[915117898232655882, 814243356497412136])

manager = 882297247176486913

mod_manager = 1050882740897198173

moderator = 814247255128539177

helper = 957902388893732934