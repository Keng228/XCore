import discord
from discord import app_commands as apc
from discord.ext import commands
from LIB_conctDB import Economy
from LIB_config import bot, manager, mod_manager
from datetime import datetime, date as Date

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

class admquest(apc.Group):
    """economy commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot

    @apc.command(name="создать_квест")
    async def create_quest(self, interaction: discord.Interaction, name: str, reward: int, date: str, descr: str = "Новый квест", multi: bool = False):
        """
        Создание квеста (нужна роль Менеджера):
        
        :param name: Название.
        :param reward: Стоимость.
        :param date: До какой даты будет доступен квест.
        :param descr: Описание (по умолчанию 'Новый предмет').
        :param multi: Будет ли квест многоразовым (по умолчанию нет).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        Embed.title = "Квесты:"
        name.lower()
        name.capitalize()
        await interaction.response.defer()
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        #проверки
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        elif reward < 0:
                Embed.description = "Награду меньше нуля - ставить нельзя!"
        else:
            #если всё хорошо
            Embed.set_footer(text = f"Модератор: {interaction.user.name}")
            Economy.BDcommand.table = "Quest"
            Economy.BDcommand.columns.append("QName")
            Economy.BDcommand.condition.append(f"QName = '{name}'")
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()

            current_datetime = datetime.now()
            i = 0
            dd = ""
            mm = ""
            yyyy = current_datetime.year
            arr = [dd, mm]
            for numb in date:
                if numb.isdigit():
                    arr[i] += numb
                else:
                    i += 1
            data = Date(year=yyyy, month=int(arr[1]), day=int(arr[0]))
            date = str(data.year) + "-" + arr[1] + "-" + arr[0]
            unix = int(datetime(year=yyyy, month=int(arr[1]), day=int(arr[0]), hour=0, minute=0, second=0, microsecond=0).timestamp())
            
            if str(result) == "[]":
                if multi == False:
                    progress = 0
                    Economy.BDcommand.table = "Quest"
                    Economy.BDcommand.columns = ["QName", "QDescription", "Reward", "QTime", "Multiply", "Progress"]
                    Economy.BDcommand.data = [f"'{name}'", f"'{descr}'", f"{reward}", f"'{date}'", f"{multi}", f"'{progress}'"]
                else:
                    Economy.BDcommand.table = "Quest"
                    Economy.BDcommand.columns = ["QName", "QDescription", "Reward", "QTime", "Multiply"]
                    Economy.BDcommand.data = [f"'{name}'", f"'{descr}'", f"{reward}", f"'{date}'", f"{multi}"]
                result = Economy.bdinsert()
                Economy.BDcommand.clear()
                if result == True:
                    if multi:
                        Embed.description = f"Многоразовый квест `{name}` с наградой `{reward}` добавлен.\nОписание гласит: `{descr}`\nКвест доступен до <t:{unix}:D>"
                    else:
                        Embed.description = f"Одноразовый квест `{name}` с наградой `{reward}` добавлен.\nОписание гласит: `{descr}`\nКвест доступен до <t:{unix}:D>"
                else:
                    Embed.description = str(result) + " `i`"
            else:
                if result == True:
                    if multi:
                        Economy.BDcommand.table = "Quest"
                        Economy.BDcommand.columns = ["QDescription", "Reward", "QTime", "Multiply", "Progress"]
                        Economy.BDcommand.data = [f"= '{descr}'", f" = {reward}", f" = '{date}'", f" = {multi}", f" = NULL"]
                        Economy.BDcommand.condition.append(f"QName = '{name}'")
                        result = Economy.bdupdate()
                        Economy.BDcommand.clear()
                        Embed.description = f"Многоразовый квест `{name}` с наградой `{reward}` обновлён.\nОписание гласит: `{descr}`\nКвест доступен до <t:{unix}:D>"
                    else:
                        Economy.BDcommand.table = "Quest"
                        Economy.BDcommand.columns = ["QDescription", "Reward", "QTime", "Multiply", "Progress"]
                        Economy.BDcommand.data = [f"= '{descr}'", f" = {reward}", f" = '{date}'", f" = {multi}", f" = 0"]
                        Economy.BDcommand.condition.append(f"QName = '{name}'")
                        result = Economy.bdupdate()
                        Economy.BDcommand.clear()
                        Embed.description = f"Одноразовый квест `{name}` с наградой `{reward}` обновлён.\nОписание гласит: `{descr}`\nКвест доступен до <t:{unix}:D>"
                else:
                    Embed.description = str(result) + " `u`"
        await interaction.followup.send(embed=Embed)

    @apc.command(name="удалить_квест")
    async def delete_quest(self, interaction: discord.Interaction, name: str):
        """
        Удаление предмета (нужна роль Менеджера):
        
        :param name: Название квеста.
        """
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        Embed.title = "Квесты:"
        await interaction.response.defer()
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        #проверка
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            #если всё хорошо
            Embed.set_footer(text = f"Модератор: {interaction.user.name}")
            Economy.BDcommand.table = "Quest"
            Economy.BDcommand.columns.append("QName")
            Economy.BDcommand.condition.append(f"QName = '{name}'")
            
            result = Economy.bdselect()
            if str(result) == "[]":
                Embed.description = f"Квеста с именем `{name}` - не найдено!"
            else:
                Economy.BDcommand.table = "UsersQuest"
                Economy.bddelete()
                
                Economy.BDcommand.table = "Quest"
                result = Economy.bddelete()
                if result == True:    
                    Embed.description = f"Квест `{name}` - удалён!"
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)

    @apc.command(name="выдать_квест")
    async def add_quest(self, interaction: discord.Interaction, name: str, user: discord.User = None):
        """
        Выдача квеста участнику (нужна роль Менеджера):
        
        :param name: Название.
        :param user: Участник (по умолчанию - Вы)."""
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        if user == None:
            user = interaction.user
        Embed.title = f"Добавление {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        #проверка
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            #если всё правильно
            Embed.set_footer(text = f"Модератор: {interaction.user.name}")
            Economy.BDcommand.table = "Quest"
            Economy.BDcommand.columns = ["QName", "Progress"]
            Economy.BDcommand.condition = [f"QName = '{name}'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) == "[]":
                Embed.description = f"Квеста с названием `{name}` нет!"
            else:
                progress = result[0][1]
                Economy.BDcommand.table = "UsersQuest"
                Economy.BDcommand.columns.append("UserID")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
                
                result = Economy.bdselect()
                Economy.BDcommand.clear()    
                if str(result) == "[]":
                    Economy.BDcommand.table = "UsersQuest"
                    Economy.BDcommand.columns = ["UserID", "QName", "Progress"]
                    Economy.BDcommand.data = [f"'{user.id}'", f"'{name}'", f"{progress}"]
                    
                    result = Economy.bdinsert()
                    Economy.BDcommand.clear()
                else:
                    Embed.description = f"Квест с названием `{name}` - уже есть!"
                if result == True:
                    Embed.description = f"Квест с названием `{name}` - добавлен!"
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)
        
    @apc.command(name="изъять_квест")
    async def remove_quest(self, interaction: discord.Interaction, name: str, user: discord.User = None):
        """
        Изъятие квеста у участника (нужна роль Менеджера):
        
        :param name: Название.
        :param user: Участник (по умолчанию - Вы).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        if user == None:
            user = interaction.user
        Embed.title = f"Изъятие квеста {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            Embed.set_footer(text = f"Модератор: {interaction.user.name}")
            Economy.BDcommand.table = "UsersQuest"
            Economy.BDcommand.columns.append("QName")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) == "[]":
                Embed.description = f"Квеста с названием `{name}` у участника нет!"
            else:
                Economy.BDcommand.table = "UsersQuest"
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
        
                result = Economy.bddelete()
                Economy.BDcommand.clear()
                
                Economy.BDcommand.table = "Quest"
                Economy.BDcommand.columns.append("Multiply")
                Economy.BDcommand.condition = [f"QName = '{name}'"]
            
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                
                if result[0][0] == False:
                    Economy.BDcommand.table = "Quest"
                    Economy.BDcommand.columns.append("Progress")
                    Economy.BDcommand.data.append(f"= 0")
                    Economy.BDcommand.condition = [f"QName = '{name}'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Квест с названием `{name}` - был изъят!"
                else:
                    Embed.description = str(result) + "`d`"
        await interaction.followup.send(embed=Embed)

    @apc.command(name="закончить_квест")
    async def end_quest(self, interaction: discord.Interaction, name: str, user: discord.User = None):
        """
        Закончить квест участника (нужна роль Менеджера):
        
        :param name: Название.
        :param user: Участник (по умолчанию - Вы).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        if user == None:
            user = interaction.user
        Embed.title = f"Конец квеста {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            Embed.set_footer(text = f"Модератор: {interaction.user.name}")
            Economy.BDcommand.table = "UsersQuest"
            Economy.BDcommand.columns.append("QName")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) == "[]":
                Embed.description = f"Квеста с названием `{name}` у участника нет!"
            else:
                Economy.BDcommand.table = "Quest"
                Economy.BDcommand.columns.append("Multiply")
                Economy.BDcommand.condition = [f"QName = '{name}'"]
            
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                
                if result[0][0] == False:
                    Economy.BDcommand.table = "UsersQuest"
                    Economy.BDcommand.condition = [f"QName = '{name}'"]
                    
                    result = Economy.bddelete()
                    Economy.BDcommand.clear()
                    
                    Economy.BDcommand.table = "Quest"
                    Economy.BDcommand.condition = [f"QName = '{name}'"]
                    
                    result = Economy.bddelete()
                    Economy.BDcommand.clear()
                else:
                    Economy.BDcommand.table = "UsersQuest"
                    Economy.BDcommand.columns.append("Progress")
                    Economy.BDcommand.data.append(f"= 0")
                    Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Квест с названием `{name}` - был закончен!"
                else:
                    Embed.description = str(result) + "`d`"
        await interaction.followup.send(embed=Embed)
