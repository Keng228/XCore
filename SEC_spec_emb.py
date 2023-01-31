import discord
from discord import app_commands as apc
from discord.ext import commands
import aiohttp
import random
from LIB_config import bot as Bot

Spec_embed = discord.Embed(
    title = "Специальный эмбед!",
    description = "Вы можете поменять содержание этого эмбеда!",
    color = 0xAF69EF,
)

Embed = discord.Embed(
    title = "Специальный эмбед!",
    description = "Вы можете поменять содержание этого эмбеда!",
    color = 0xAF69EF,
)

class spec_embed(apc.Group):
    """Manage general commands"""
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        
    @apc.command()
    async def send(self, interaction: discord.Interaction):
        """Отправляет специальный эмбед"""
        channel = interaction.channel
        await interaction.response.send_message("Отправка эмбеда:")
        await channel.send(embed=Spec_embed)
        
    @apc.command()
    async def descript(self, interaction: discord.Interaction, description: str = "Вы можете поменять содержание этого эмбеда!"):
        """Изменение содержания эмбеда"""
        Spec_embed.description = description
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def color(self, interaction: discord.Interaction, color: int = 0xAF69EF):
        """Изменение цвета эмбеда"""
        Spec_embed.color = color
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def title(self, interaction: discord.Interaction, title: str = "Специальный эмбед!"):
        """Изменение заголовка эмбеда"""
        Spec_embed.title = title
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def clear(self, interaction: discord.Interaction):
        """Очистка эмбеда"""
        Spec_embed = Embed
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def add_field(self, interaction: discord.Interaction, name: str = "Строка!", description: str = "Содержание!", inline: bool = True):
        """Добавление новой спец строки"""
        Spec_embed.add_field(name=name, value=description, inline=inline)
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def remove_field(self, interaction: discord.Interaction, index: int = 0):
        """Добавление новой спец строки"""
        if index == 0:
            index = len(Spec_embed.fields)
        index -= 1
        Spec_embed.remove_field(index=index)
        await interaction.response.send_message("Получившийся эмбед:", embed=Spec_embed)
        
    @apc.command()
    async def reactoins(self, interaction: discord.Interaction):
        #channel = Bot.get_guild(814243356497412136).get_channel(818500574189977601)
        #messange = channel
        await interaction.response.send_message(content="Ыыы")