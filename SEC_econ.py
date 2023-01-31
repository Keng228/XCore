import discord
from discord import app_commands as apc
from discord.ext import commands
from LIB_conctDB import Economy
from LIB_config import manager, mod_manager

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

class economy(apc.Group):
    """economy commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot

    @apc.command(name="баланс")
    async def view_money(self, interaction: discord.Interaction, user: discord.User = None):    
        """
        Просмотр монет участника:
        
        :param user: Участник (по умолчанию - Вы).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        if user == None:
            user = interaction.user
        await interaction.response.defer()
        Embed.title = f"Монеты {user.name}:"
        you = False
        manage_role = False
        mon_klv = ""
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        if user == interaction.user:
            you = True
        #проверка
        if (you == False) and (manage_role == False):
            Embed.description = "Только Менеджер может смотреть чужие монеты!"
        else:
            #команда
            Embed.title = f"Монеты {user.name}:"
            Economy.writeMoney(user)
            Economy.BDcommand.table = "Money"
            Economy.BDcommand.columns.append("Money")
            Economy.BDcommand.condition.append(f"UserID = {user.id}")
            
            result = Economy.bdselect()
            mon_klv = result[0][0]
            Embed.description = f"**{mon_klv}** <a:X_coin:1065524368056270919>"
        await interaction.followup.send(embed=Embed)

    @apc.command(name="лист_предметов")
    async def items_list(self, interaction: discord.Interaction, item: str = "", cost: int = 0, descr: str = ""):
        """
        Просмотр всех существующих предметов:
        
        :param item: Название (не обязательно).
        :param cost: Стоимость (не обязательно).
        :param descr: - описание (не обязательно).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        Embed.title = "Товары:"
        Embed.description = ""
        await interaction.response.defer()
        #запрос
        Economy.BDcommand.table = "Items"
        Economy.BDcommand.columns = ["ItemID", "`Description`", "Cost"]
            
        prv = ""
        prt = 0
        if item != "":
            Economy.BDcommand.condition.append(f"\nItemID = '{item}'")
            prt += 1
        if cost != 0:
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nCost = '{cost}'"
            Economy.BDcommand.condition.append(prv)
            prt += 1
        if descr != "":
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nDescription = '{descr}'"
            prt += 1
            Economy.BDcommand.condition.append(prv)
        
        result = Economy.bdselect()
        if str(result) == "[]":
            if item != "":
                Embed.description = "Предмета с таким названием нет!"
            if cost != 0:
                Embed.description = "Предмета с такой ценой нет!"
            if descr != "":
                Embed.description = "Предмета с таким описанием нет!"
            if prt == 0:
                Embed.description = "Список пуст!"
        else:
            for res in result:
                Embed.add_field(name=res[0], value=f"Цена: `{res[2]}`<a:X_coin:1065524368056270919>\n*{res[1]}*")
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()

    @apc.command(name="купить")
    async def buy(self, interaction: discord.Interaction, item: str, count: int = 1):
        """
        Покупка предмета/ов за деньги:
        
        :param item: Название.
        :param count: Количество (по умолчанию 1).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
        user = interaction.user
        Embed.title = f"Покупка {user.name}:"
        await interaction.response.defer()
        Economy.writeMoney(user)
        
        Economy.BDcommand.table = "Items"
        Economy.BDcommand.columns.append("Cost")
        Economy.BDcommand.condition.append(f"ItemID = '{item}'")
        
        result = Economy.bdselect()
        Economy.BDcommand.clear()
        if str(result) == "[]":
            Embed.description = f"Предмета с названием `{item}` нет!"
        else:
            cost = ""
            for Item in str(result):
                if Item.isnumeric():
                    cost += Item
            cost = int(cost)
            cost = cost * count
            
            Economy.BDcommand.table = "Money"
            Economy.BDcommand.columns.append("Money")
            Economy.BDcommand.condition.append(f"UserID = '{user.id}'")
        
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            money = ""
            for Item in str(result):
                if Item.isnumeric():
                    money += Item
            money = int(money)
                
            if (money - cost) < 0:
                Embed.description = f"У вас не хватает {(money - cost) * -1} <a:X_coin:1065524368056270919>"
            else:
                Economy.BDcommand.table = "Money"
                Economy.BDcommand.columns.append("Money")
                Economy.BDcommand.data.append(f"= Money - {cost}")
                
                result = Economy.bdupdate()
                Economy.BDcommand.clear()
                
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("UserID")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                if str(result) == "[]":
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns = ["UserID", "ItemID", "Count"]
                    Economy.BDcommand.data = [f"'{user.id}'", f"'{item}'", f"'{count}'"]
                    
                    result = Economy.bdinsert()
                    Economy.BDcommand.clear()
                else:
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns.append("Count")
                    Economy.BDcommand.data.append(f"= Count + {count}")
                    Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}`, куплен за `{cost}` <a:X_coin:1065524368056270919>"
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)

    @apc.command(name="использовать")
    async def use(self, interaction: discord.Interaction, item: str, count: int = 1):
        """
        Использование предмета, с дальнейшим вычетом его из инвентаря:
        :param item: Название.
        :param count: Количество (по умолчанию 1).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
        user = interaction.user
        Embed.title = f"Инвентарь {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        
        Economy.BDcommand.table = "Inventory"
        Economy.BDcommand.columns.append("ItemID")
        Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
        result = Economy.bdselect()
        Economy.BDcommand.clear()
        if str(result) == "[]":
            Embed.description = f"Предмета с названием `{item}` у вас нет!"
        else:
            Economy.BDcommand.table = "Inventory"
            Economy.BDcommand.columns.append("Count")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            counts = ""
            for Item in str(result):
                    if Item.isnumeric():
                        counts += Item
            counts = int(counts)
            if (counts - count) == -1:
                Embed.description = "У вас не хватает 1 предмета!"
            elif (counts - count) < -1:
                Embed.description = f"У вас не хватает {(counts - count) * -1} предметов!"
            elif (counts - count) == 0:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
                result = Economy.bddelete()
                Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}` - использован!"
                else:
                    Embed.description = str(result) + "`d`"
            else:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("Count")
                Economy.BDcommand.data.append(f"= Count - {count}")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
                
                result = Economy.bdupdate()
                Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}` - использован!"
                else:
                    Embed.description = str(result) + "`u`"
        await interaction.followup.send(embed=Embed)
    
    @apc.command(name="просмотр_инвентаря")
    async def view_inventory(self, interaction: discord.Interaction, user: discord.User = None):
        """
        Просмотреть инвентарь (работает без роли Менеджера, если смотреть свой. В других случаях - нужна роль):
        
        :param user: Пользователь (по умолчанию - Вы)."""
        #стандартное начало
        Economy.BDcommand.clear()
        if user == None:
            user = interaction.user
        Embed.title = f"Инвентарь {user.name}:"
        Embed.description = ""
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        you = False
        manage_role = False
        for role in interaction.user.roles:
            if role.id == manager or role.id == mod_manager:
                manage_role = True
        if user == interaction.user:
            you = True
        #проверка
        if (you == False) and (manage_role == False):
            Embed.description = "Только Менеджер может смотреть чужой инвентарь!"
        else:
            #если всё хорошо
            Economy.BDcommand.table = "Inventory"
            Economy.BDcommand.columns = ["ItemID", "Count"]
            Economy.BDcommand.condition.append(f"UserID = '{user.id}'")
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            
            Economy.BDcommand.table = "Items"
            Economy.BDcommand.columns = ["ItemID", "Description"]
            
            result2 = Economy.bdselect()
            Economy.BDcommand.clear()
            
            if str(result) == "[]":
                Embed.description = "Этот инвентарь пуст!"
            else:
                for res in result:
                    for res2 in result2:
                        if res[0] == res2[0]:
                            Embed.add_field(name=f"{res[1]} - {res[0]}", value=f"{res2[1]}")
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()
        
    @apc.command(name="передать_предмет")
    async def give_item(self, interaction: discord.Interaction, item: str, recip_user: discord.User, count: int = 1):
        """
        Передать предмет другому участнику:
        
        :param item: Название.
        :param user: Участник которому хотите передать предмет.
        :param count: Количество (по умолчанию 1).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        item.lower()
        item.capitalize()
        user = interaction.user
        Embed.title = f"Передача {user.name} —> {recip_user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        Economy.writeUserID(UserID=recip_user.id)
        
        Economy.BDcommand.table = "Inventory"
        Economy.BDcommand.columns.append("ItemID")
        Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
        result = Economy.bdselect()
        Economy.BDcommand.clear()
        if str(result) == "[]":
            Embed.description = f"Предмета с названием `{item}` у вас нет!"
        else:
            Economy.BDcommand.table = "Inventory"
            Economy.BDcommand.columns.append("Count")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            counts = ""
            for Item in str(result):
                    if Item.isnumeric():
                        counts += Item
            counts = int(counts)
            if (counts - count) == -1:
                Embed.description = "У вас не хватает 1 предмета!"
            elif (counts - count) < -1:
                Embed.description = f"У вас не хватает {(counts - count) * -1} предметов!"
            elif (counts - count) == 0:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
        
                result = Economy.bddelete()
                Economy.BDcommand.clear()
                
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}` —> передан <@{recip_user.id}>!"
                else:
                    Embed.description = str(result) + "`d`"
            else:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("Count")
                Economy.BDcommand.data.append(f"= Count - {count}")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND ItemID = '{item}'"]
                
                result = Economy.bdupdate()
                Economy.BDcommand.clear()
                
                if result == True:
                    Embed.description = f"Предмет `{item}`, в количестве `{count}` —> передан <@{recip_user.id}>!"
                else:
                    Embed.description = str(result) + "`u`"
            if result == True:
                Economy.BDcommand.table = "Inventory"
                Economy.BDcommand.columns.append("Count")
                Economy.BDcommand.condition = [f"UserID = '{recip_user.id}'", f"AND ItemID = '{item}'"]
            
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                if str(result) == "[]":
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns = ["UserID", "ItemID", "Count"]
                    Economy.BDcommand.data = [f"'{recip_user.id}'", f"'{item}'", f"'{count}'"]
                    
                    result = Economy.bdinsert()
                    Economy.BDcommand.clear()
                else:
                    Economy.BDcommand.table = "Inventory"
                    Economy.BDcommand.columns.append("Count")
                    Economy.BDcommand.data.append(f"= Count + {count}")
                    Economy.BDcommand.condition = [f"UserID = '{recip_user.id}'", f"AND ItemID = '{item}'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                
        await interaction.followup.send(embed=Embed)

    @apc.command(name="хелп")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emb = discord.Embed(
        title="Стандартный эмбед!",
        description="Сообщение!",
        color=0xAF69EF,
        )
        emb.title = f"Помощь для {interaction.user.name}"
        emb.add_field(name="баланс", value="Команда для просмотра количества ваших монет (смотреть чужой баланс можно только ГМ).")
        emb.add_field(name="лист_предметов", value="Команда просмотра ассортимента предметов в магазине.\n"
                        + "Переменные казывать не обязательно, они отвечают только за сортировку. Описания переменных есть при вводе.")
        emb.add_field(name="купить", value="Команда для покупки предмета из листа предметов.\n"
                        + "Описание переменных есть при вводе")
        emb.add_field(name="использовать", value="Команда для использования купленного предмета.\n"
                        + "Описание переменных есть при вводе")
        emb.add_field(name="просмотр_инвентаря", value="Команда для просмотра приобретённых вами предметов (смотреть чужой инвентарь можно только ГМ).\n"
                        + "Описание переменной есть при вводе")
        emb.add_field(name="передать_предмет", value="Команда для передачи предмета другому игроку.\n"
                        + "Описание переменных есть при вводе")
        emb.set_footer(text="Если с командами возникли неполадки, вы увидели ошибку или есть вопросы сообщите об этом X.Vovi#6455")
        await interaction.followup.send(embed=emb)
        emb.clear_fields()