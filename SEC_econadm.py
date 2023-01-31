import discord
from discord import app_commands as apc
from discord.ext import commands
import random
from LIB_config import bot, manager, mod_manager
from LIB_conctDB import Economy

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

class admeconomy(apc.Group):
    """economy commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot
        
    @apc.command(name="добавить_монеты")
    async def add_money(self, interaction: discord.Interaction, user: discord.User = None, money: int = 1):
        """
        Добавление монет участнику (нужна роль Менеджера):
        
        :param user: Участник (по умолчанию - Вы).
        :param money: Кол-во монет (по умолчанию 1).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        if user == None:
            user = interaction.user
        Embed.title = f"Монеты {user.name}:"
        await interaction.response.defer()
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        #проверки
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        elif money == 0:
            Embed.description = "Прибавлять такое количество монет - бессмысленно"
        else:
            Economy.writeUserID(UserID=user.id)
            #заполнение если всё верно
            Economy.BDcommand.table = "Money"
            Economy.BDcommand.columns.append("Money")
            Economy.BDcommand.condition.append(f"UserID = {user.id}")
            
            result = Economy.bdselect()
            if str(result) == "[]":
                Economy.BDcommand.columns = ["UserID", "Money"]
                Economy.BDcommand.data = [f"'{user.id}'", money]
                result = Economy.bdinsert()
            else:
                Economy.BDcommand.data.append(f"= Money + {money}")
                result = Economy.bdupdate()
            if result == True:
                Embed.description = f"Монет выдано `{money}`!"
            else:
                Embed.description = str(result)
        await interaction.followup.send(embed=Embed)

    @apc.command(name="создать_предмет")
    async def create_item(self, interaction: discord.Interaction, item: str, cost: int, descr: str = "Новый предмет"):
        """
        Создание предмета (нужна роль Менеджера):
        
        :param item: Название.
        :param cost: Стоимость.
        :param descr: Описание (по умолчанию 'Новый предмет').
        """
        #стандартное начало
        Economy.BDcommand.clear()
        Embed.title = "Предметы:"
        item.lower()
        item.capitalize()
        await interaction.response.defer()
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        #проверки
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        elif cost < 0:
                Embed.description = "Цену меньше нуля - ставить нельзя!"
        else:
            #если всё хорошо
            Economy.BDcommand.table = "Items"
            Economy.BDcommand.columns.append("ItemID")
            Economy.BDcommand.condition.append(f"ItemID = '{item}|'")
            
            result = Economy.bdselect()

            if str(result) == "[]":
                Economy.BDcommand.columns = ["ItemID", "`Description`", "Cost"]
                Economy.BDcommand.data = [f"'{item}|'", f"'{descr}|'", f"{cost}"]
                result = Economy.bdinsert()
                if result == True:
                    Embed.description = f"Предмет `{item}` с ценой `{cost}` добавлен.\nОписание гласит: `{descr}`"
                else:
                    Embed.description = str(result) + " `i`"
            else:
                Economy.BDcommand.columns = ["`Description`", "Cost"]
                Economy.BDcommand.data = [f"= '{descr}|'", f" = {cost}"]
                result = Economy.bdupdate()
                if result == True:
                    Embed.description = f"Предмет `{item}` с ценой `{cost}` обновлён.\nОписание гласит: `{descr}`"
                else:
                    Embed.description = str(result) + " `u`"
        await interaction.followup.send(embed=Embed)

    @apc.command(name="удалить_предмет")
    async def delete_item(self, interaction: discord.Interaction, item: str):
        """
        Удаление предмета (нужна роль Менеджера):
        
        :param item: Название предмета.
        """
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
        Embed.title = "Предметы:"
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
            Economy.BDcommand.table = "Items"
            Economy.BDcommand.columns.append("ItemID")
            Economy.BDcommand.condition.append(f"ItemID = '{item}|'")
            
            result = Economy.bdselect()
            if str(result) == "[]":
                Embed.description = f"Предмета с именем `{item}` - не найдено!"
            else:
                Economy.BDcommand.table = "Inventory"
                Economy.bddelete()
                
                Economy.BDcommand.table = "Items"
                result = Economy.bddelete()
                if result == True:    
                    Embed.description = f"Предмет `{item}` - удалён!"
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)

    @apc.command(name="выдать_предмет")
    async def add_item(self, interaction: discord.Interaction, item: str, user: discord.User = None, count: int = 1):
        """
        Выдача предмета участнику (нужна роль Менеджера):
        
        :param item: Название.
        :param user: Участник (по умолчанию - Вы).
        :param count: Количество (по умолчанию 1)."""
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
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
        elif count < 0:
            Embed.description = "Нельзя выдать предмет в таком количестве!"
        else:
            #если всё правильно
            Economy.BDcommand.table = "Items"
            Economy.BDcommand.columns.append("Cost")
            Economy.BDcommand.condition = [f"ItemID = '{item}|'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) == "[]":
                Embed.description = f"Предмета с названием `{item}` нет!"
            else:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("UserID")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
                
                result = Economy.bdselect()
                Economy.BDcommand.clear()    
                if str(result) == "[]":
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns = ["UserID", "ItemID", "Count"]
                    Economy.BDcommand.data = [f"'{user.id}'", f"'{item}|'", f"'{count}'"]
                    
                    result = Economy.bdinsert()
                    Economy.BDcommand.clear()
                else:
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns.append("Count")
                    Economy.BDcommand.data.append(f"= Count + {count}")
                    Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}`, добавлен."
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)
        
    @apc.command(name="изъять_предмет")
    async def remove_item(self, interaction: discord.Interaction, item: str, user: discord.User = None, count: int = -1):
        """
        Изъятие предмета у участника (нужна роль Менеджера):
        
        :param item: Название.
        :param user: Участник (по умолчанию - Вы).
        :param count: Количество (по умолчанию 1).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
        user = interaction.user
        Embed.title = f"Изъятие {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        elif count < -1:
            Embed.description = "Нельзя изъять предмет в таком количестве!"
        else:
            Economy.BDcommand.table = "Inventory"
            Economy.BDcommand.columns.append("ItemID")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) == "[]":
                Embed.description = f"Предмета с названием `{item}` у участника нет!"
            else:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("Count")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
            
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                counts = ""
                for Item in str(result):
                        if Item.isnumeric():
                            counts += Item
                counts = int(counts)
                if (counts - count) < 0 or count < 0:
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
            
                    result = Economy.bddelete()
                    Economy.BDcommand.clear()
                    if result == True:
                        Embed.description = f"Предмет `{item}` был польностью изъят!"
                    else:
                        Embed.description = str(result) + "`d`"
                else:
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns.append("Count")
                    Economy.BDcommand.data.append(f"= Count - {count}")
                    Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}|'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                    if result == True:
                        Embed.description = f"Предмет `{item}` - изъят, в количестве `{count}`!"
                    else:
                        Embed.description = str(result) + "`u`"
        await interaction.followup.send(embed=Embed)
