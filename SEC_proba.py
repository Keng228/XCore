import discord
from discord import app_commands as apc
from discord.ext import commands
import aiohttp
import random
from LIB_config import bot as Bot

Embed = discord.Embed(
    title="Стандартный эмбед!",
    color=0xAF69EF,
)

emb = discord.Embed(
    title="Стандартный эмбед!",
    color=0xAF69EF,
)

class general(apc.Group):
    """Manage general commands"""
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot


    @apc.command(name="привет")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hello')

    @apc.command(name="версия")
    async def version(self, interaction: discord.Interaction):
        """Показывает версию бота"""
        await interaction.response.send_message('Сейчас работает версия бота 0.5.5.\nЕсли вы увидели ошибку или бот не работает - обратитесь к @X.Vovi#6455')
        
    @apc.command(name="лис")
    async def rand_fox(self, interaction: discord.Interaction):
        await interaction.response.defer()
        Embed.title = "Лисёнок!"
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/fox')
            foxjson = await request.json()
            Embed.set_image(url=foxjson['link'])
        await interaction.followup.send(embed=Embed)
        
    @apc.command(name="собакен")
    async def rand_dog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        Embed.title = "Собачка!"
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
            Embed.set_image(url=dogjson['link'])
        await interaction.followup.send(embed=Embed)
            
    @apc.command(name="ящерица")
    async def rand_lizard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        Embed.title = "Ящерица!"
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://loremflickr.com/json/500/500/lizard')
            lizardjson = await request.json()
            Embed.set_image(url=lizardjson['file'])
        await interaction.followup.send(embed=Embed)

    @apc.command(name="по_теме")
    async def rand_image(self, interaction: discord.Interaction, theme: str = "X-tale"):
        await interaction.response.defer()
        Embed.title = "Изображение!"
        Embed.description = f"{theme}"
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://loremflickr.com/json/500/500/{theme}')
            lizardjson = await request.json()
            Embed.set_image(url=lizardjson['file'])
        await interaction.followup.send(embed=Embed)
        
    #Команда: rand

    @apc.command()
    async def rand(self, interaction: discord.Interaction, rand1: int, rand2: int):
        """Выдача рандомного числа"""
        rand3 = random.randint(rand1, rand2)

        Embed.title="Рандом!"
        Embed.description=f"Полученное число = ||{rand3}||"
        await interaction.response.send_message(embed=Embed)

    #Команда: banana

    @apc.command()
    async def banana(self, interaction: discord.Interaction):
        """BANANA"""
        await interaction.response.send_message(':banana:')
        
    #Команда: ping
    @apc.command(name="пинг")
    async def ping(self, interaction: discord.Interaction):
        """Присылает состояние сигнала с ботом"""
        Embed.title = "**Пинг бота**"
        Embed.description = f"""**{Bot.ws.latency * 1000:.0f} мс**
        **Пользователь:** <@{interaction.user.id}>
        **Канал: <#{interaction.channel_id}>**"""
        await interaction.response.send_message(embed=Embed)