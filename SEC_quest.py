import discord
from discord import app_commands as apc
from discord.ext import commands
from LIB_conctDB import Economy
from datetime import datetime
from LIB_config import bot, manager, mod_manager

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

bed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

class quest(apc.Group):
    """economy commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot


    @apc.command(name="доска_квестов")
    async def quest_list(self, interaction: discord.Interaction, name: str = "", reward: int = 0, descr: str = "", multi: str = "", progress: str = ""):
        """
        Просмотр всех существующих предметов (возможна сортировка).
        
        :param name: Название (не обязательно).
        :param reward: Стоимость (не обязательно).
        :param descr: Описание (не обязательно).
        :param multi: Многоразовый (не обязательно).
        :param progress: Метка о начале (не обязательно).
        """
        #стандартное начало
        Economy.BDcommand.clear()
        Embed.clear_fields()
        Embed.title = "Квесты:"
        Embed.description = ""
        await interaction.response.defer()
        #запрос
        Economy.BDcommand.table = "Quest"
        Economy.BDcommand.columns = ["QName", "QDescription", "Reward", "QTime", "Multiply", "Progress"]
            
        prv = ""
        prt = 0
        if name != "":
            Economy.BDcommand.condition.append(f"\QName = '{name}'")
            prt += 1
        if reward != 0:
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nReward = '{reward}'"
            Economy.BDcommand.condition.append(prv)
            prt += 1
        if descr != "":
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nQDescription = '{descr}'"
            prt += 1
            Economy.BDcommand.condition.append(prv)
        if multi != "":
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nMultiply = '{multi}'"
            prt += 1
            Economy.BDcommand.condition.append(prv)
        if progress != "":
            if prt > 0:
                prv += f"\nAND"
            prv += f"\nProgress = '{progress}'"
            prt += 1
            Economy.BDcommand.condition.append(prv)
        
        result = Economy.bdselect()
        if str(result) == "[]":
            if name != "" or reward != 0 or descr != "" or multi != "" or progress != "":
                Embed.description = "Квеста с такими параметрами нет!"
            if prt == 0:
                Embed.description = "Список пуст!"
        else:
            Embed.description = ""
            text = ""
            mult = ""
            for res in result:
                    if res[4] == 1 or (res[4] == 0 and res[5] == 0):
                        unix = int(datetime(year=res[3].year, month=res[3].month, day=res[3].day, 
                                            hour=0, minute=0, second=0, microsecond=0).timestamp())
                        if res[4]:
                            mult = "✅"
                        else:
                            mult = "❌"
                        text = f"Описание: \n*{res[1]}*\n"
                        text += f"Награда: **{res[2]}**\n"
                        text += f"До: <t:{unix}:D>\n"
                        text += f"Многоразовый: {mult}\n"
                        Embed.add_field(name=f"{res[0]}", value=text)
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()

    @apc.command(name="взять_листочек")
    async def get_quest(self, interaction: discord.Interaction, name: str):
        """
        Взятие квеста:
        
        :param name: Название.
        """
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        user = interaction.user
        Embed.title = f"Взять квест {user.name}:"
        await interaction.response.defer()
        Economy.writeMoney(user)
        
        Economy.BDcommand.table = "Quest"
        Economy.BDcommand.columns = ["QName", "Progress", "Multiply"]
        Economy.BDcommand.condition.append(f"QName = '{name}'")
        
        result = Economy.bdselect()
        progress = int(result[0][1])
        multiply = int(result[0][2])
        
        Economy.BDcommand.clear()
        
        if str(result) == "[]":
            Embed.description = f"Квеста с названием `{name}` нет!"
        elif progress == 1 and multiply == 0:
            Embed.description = f"Этот квест уже начат!"
        else:
            Economy.BDcommand.table = "UsersQuest"
            Economy.BDcommand.columns.append("UserID")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
    
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(result) != "[]":
                Embed.description = f"В вашем списке уже есть квест с названием `{name}`!"
            else:
                if progress == None:
                    progress = 0
                Economy.BDcommand.table = "UsersQuest"
                Economy.BDcommand.columns = ["UserID", "QName", "Progress"]
                Economy.BDcommand.data = [f"'{user.id}'", f"'{name}'", f"{progress}"]
                    
                result = Economy.bdinsert()
                Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"В ваш список был добавлен квест с названием `{name}`"
                else:
                    Embed.description = str(result)
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()

    @apc.command(name="начать_квест")
    async def start(self, interaction: discord.Interaction, name: str):
        """
        Начать квест, который был вами взят:
        :param name: Название.
        """
        #стандартное начало
        Economy.BDcommand.clear()
        name.lower()
        name.capitalize()
        user = interaction.user
        Embed.title = f"Квест для {user.name}:"
        await interaction.response.defer()
        Economy.writeUserID(UserID=user.id)
        
        Economy.BDcommand.table = "UsersQuest"
        Economy.BDcommand.columns.append("QName")
        Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
        
        result = Economy.bdselect()
        Economy.BDcommand.clear()
        if str(result) == "[]":
            Embed.description = f"Квеста с названием `{name}` у вас нет!"
        else:
            Economy.BDcommand.table = "UsersQuest"
            Economy.BDcommand.columns.append("Progress")
            Economy.BDcommand.condition = [f"UserID = '{user.id}'"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            prv = False
            for res in result:
                if res[0] == 1:
                    prv = True
                    break
            
            if prv == False:
                Economy.BDcommand.table = "Quest"
                Economy.BDcommand.columns.append("Multiply")
                Economy.BDcommand.condition = [f"QName = '{name}'"]
            
                result = Economy.bdselect()
                Economy.BDcommand.clear()
                
                if result[0][0] == False:
                    Economy.BDcommand.table = "Quest"
                    Economy.BDcommand.columns.append("Progress")
                    Economy.BDcommand.data.append(f"= 1")
                    Economy.BDcommand.condition = [f"QName = '{name}'"]
                    
                    result = Economy.bdupdate()
                    Economy.BDcommand.clear()
                    
                    Economy.BDcommand.table = "UsersQuest"
                    Economy.BDcommand.condition = [f"QName = '{name}'", f"AND UserID != '{user.id}'"]
                    
                    result = Economy.bddelete()
                    Economy.BDcommand.clear()
                
                Economy.BDcommand.table = "UsersQuest"
                Economy.BDcommand.columns.append("Progress")
                Economy.BDcommand.data.append(f"= 1")
                Economy.BDcommand.condition = [f"UserID = '{user.id}'", f"AND QName = '{name}'"]
                
                result = Economy.bdupdate()
                Economy.BDcommand.clear()
                if result == True:
                    Embed.description = f"Квест `{name}` - начат!\nСвободный <@&955092635826139206> сейчас подойдёт. . ."
                    channel = bot.get_channel(1044011409182314558)
                    await channel.send(f"<@&955092635826139206>")
                else:
                    Embed.description = str(result) + "`u`"
            else:
                Embed.description = f"Вами уже начат квест!"
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()
    
    @apc.command(name="взятые_квесты")
    async def view_quests(self, interaction: discord.Interaction, user: discord.User = None):
        """
        Просмотреть квесты, которые вы взяли (работает без роли ГМ, если смотреть свой. В других случаях - нужна роль):
        
        :param user: Пользователь (по умолчанию - Вы)."""
        #стандартное начало
        Economy.BDcommand.clear()
        if user == None:
            user = interaction.user
        Embed.title = f"Квесты {user.name}:"
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
            Embed.description = "Только Менеджер может смотреть чужие квесты!"
        else:
            #если всё хорошо
            Economy.BDcommand.table = "UsersQuest"
            Economy.BDcommand.columns = ["QName", "Progress"]
            Economy.BDcommand.condition.append(f"UserID = '{user.id}'")
            
            result = Economy.bdselect()
            namprog = result
            Economy.BDcommand.clear()
            
            Economy.BDcommand.table = "Quest"
            Economy.BDcommand.columns = ["QName", "QDescription", "Reward", "QTime", "Multiply"]
            
            result = Economy.bdselect()
            Economy.BDcommand.clear()
            if str(namprog) != "[]":
                Embed.description = ""
                text = ""
                mult = ""
                prog = ""
                i = 0
                for res in result:
                        if res[0] == namprog[i][0]:
                            unix = int(datetime(year=res[3].year, month=res[3].month, day=res[3].day, 
                                                hour=0, minute=0, second=0, microsecond=0).timestamp())
                            if res[4]:
                                mult = "✅"
                            else:
                                mult = "❌"
                            if namprog[i][1]:
                                prog = "✅"
                            else:
                                prog = "❌"
                            text = f"Описание: \n*{res[1]}*\n"
                            text += f"Награда: **{res[2]}**\n"
                            text += f"До: <t:{unix}:D>\n"
                            text += f"Многоразовый: {mult}\n"
                            text += f"Начат: {prog}"
                            Embed.add_field(name=f"{res[0]}", value=text)
                            i += 1
            else:
                Embed.description = "Ваш список квестов - пуст!"
                    
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()

    @apc.command(name="хелп")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emb = discord.Embed(
        title="Стандартный эмбед!",
        description="Сообщение!",
        color=0xAF69EF,
        )
        emb.title = f"Помощь для {interaction.user.name}"
        emb.add_field(name="доска_квестов", value="Команда для просмотра доски существующих квестов.\n"
                        + "Переменные указывать не обязательно, они отвечают за сортировку. Описание переменных есть при их вводе.")
        emb.add_field(name="взять_листочек", value="Команда взятия 'листочка' с доски квестов, который содержит всю нужную о квесте информацию.\n"
                        + "Описание переменной есть при вводе")
        emb.add_field(name="начать_квест", value="Команда для начала квеста по листочку что вы должны взять с доски командой выше.\n"
                        + "Описание переменной есть при вводе")
        emb.add_field(name="взятые_квесты", value="Команда показывает какие 'листочки' с квестами вы взяли с доски.\n"
                        + "Описание переменной есть при вводе")
        emb.set_footer(text="Если с командами возникли неполадки или вы увидели ошибку, сообщите об этом X.Vovi#6455")
        await interaction.followup.send(embed=emb)
        emb.clear_fields()