import discord
from discord import app_commands as apc
from discord.ext import commands
from LIB_conctDB import Moderation
from datetime import date
from LIB_config import bot, moderator, helper, Alpha
from datetime import datetime, date as Date

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="",
    color=0xAF69EF,
)

class moderation(apc.Group):
    """moderation commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot

        #Команда: LazyBones

        @Bot.hybrid_command()
        async def lazy(ctx: commands.Context):
            await ctx.send(f'Bones: <@502089481277669389>')

        #Команда: LazyBones

        @Bot.hybrid_command()
        async def evil(ctx: commands.Context):
            await ctx.send(f'Roma: <@340583226487865344>')
            
        #Команда: LazyBones

        @Bot.hybrid_command()
        async def ne1(ctx: commands.Context):
            await ctx.send(f'Donation: <@411827954990055424>')
    #Команда: warn
    @apc.command(name="варн")
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str, grade: int):
        """Выдать варн определённому пользователю"""
        #стандартное начало
        Moderation.BDcommand.clear()
        await interaction.response.defer()
        channel = interaction.channel
        Embed.title = f"Выдача варна"
        curent_date = datetime.now()
        unix = int(curent_date.timestamp())
        manage_role = False
        Moderation.writeUserID(UserID=user.id)
        for role in interaction.user.roles:
            if role.id == moderator or role.id == helper:
                manage_role = True
                
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            Moderation.BDcommand.table = "ListWarns"
            Moderation.BDcommand.columns = ["UserID", "WarnTime", "Grade", "TextProtocol"]
            Moderation.BDcommand.data = [f"'{user.id}'", f"'{unix}'", grade, f"'{reason}'"]
            
            result = Moderation.bdinsert()
            Moderation.BDcommand.clear()
            if result == True:
                Embed.description = f"""**Юзер:** <@{user.id}>
                **Дата выдачи:** <t:{unix}:D>
                **Степень:** `{grade}`"""
                Embed.add_field(name="Причина:", value=f"`{reason}`")
            else:
                Embed.description = str(result)
            Embed.set_footer(text=f"mod: {interaction.user.name}")
            
            grading = 0
            result = Moderation.warns(user=user)
            for warn in result:
                grading += int(warn[2])
            if grading >= 10:
                Moderation.BDcommand.table = "ListWarns"
                Moderation.BDcommand.condition = [f"UserID = {user.id}"]
                
                result = Moderation.bddelete()
                Moderation.BDcommand.clear()
                await channel.send("```Достигнуто максимальное количество нарушений!```")
        await interaction.followup.send(embed=Embed)
        Embed.description = ""
        Embed.clear_fields()
        Embed.remove_footer()

    #Команда: warns
    @apc.command(name="варны")
    async def warns(self, interaction: discord.Interaction, user: discord.User = None):
        """Просмотреть варны"""
        #стандартное начало
        Moderation.BDcommand.clear()
        await interaction.response.defer()
        if user == None:
            user = interaction.user
        Embed.title = f"Список варнов {user.name}:"
        result = Moderation.warns(user=user)
        if str(result) != "[]":
            i = 1
            for res in result:
                Embed.add_field(name=f"Предупреждение №{i}", value=f"Дата: <t:{res[1]}:D>\nСтепень: `{res[2]}`\nПричина:\n<{res[3]}>")
                i += 1
        else:
            Embed.description = "Варнов нет!"
        await interaction.followup.send(embed=Embed)
        Embed.clear_fields()

    #Команда: rules
    @apc.command(name="просмотр_правил")
    async def rules(self, interaction: discord.Interaction):
        """Просмотреть список кратких правил со степенями нарушений"""
        #стандартное начало
        manage_role = False
        for role in interaction.user.roles:
            if role.id == moderator or role.id == helper:
                manage_role = True
                
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            Moderation.BDcommand.clear()
            await interaction.response.defer()
            Embed.title = f"Список правил:"
            
            Moderation.BDcommand.table = "Warns"
            Moderation.BDcommand.columns = ["ID", "WarnName", "Grade"]
            Moderation.BDcommand.addition = "ORDER BY ID"
            
            result = Moderation.bdselect()
            Moderation.BDcommand.clear()
            arrs = list()
            i = 0
            j = 0
            warns = list()
            Warn = ""
            for warns in result:
                i += 1
                arrs.append(warns)
            if str(result) != "[]":
                while j < i:
                    Warn += f"""**№**`{arrs[j][0]}`
                    **Формулировка:**`{arrs[j][1]}`
                    **Степень:** `{arrs[j][2]}`"""
                    Warn += "\n\n"
                    j += 1
                Embed.description = Warn
            else:
                Embed.description = "Правил нет!"
        await interaction.followup.send(embed=Embed)

    #Команда: del_warn
    @apc.command(name="удалить_варн")
    async def del_warn(self, interaction: discord.Interaction, number: int, user: discord.User = None): 
        """Удаление варна определённого пользователя"""
        #стандартное начало
        Moderation.BDcommand.clear()
        await interaction.response.defer()
        if user == None:
            user = interaction.user
        Embed.title = f"Удаление варна {user.name}:"
        manage_role = False
        Moderation.writeUserID(UserID=user.id)
        for role in interaction.user.roles:
            if role.id == 1050882740897198173:
                manage_role = True
                
        if manage_role == False:
            Embed.description = "Не подходящая роль!"
        else:
            Moderation.BDcommand.table = "ListWarns"
            Moderation.BDcommand.columns = ["ID", "UserID", "WarnID", "WarnTime", "Grade", "TextProtocol"]
            Moderation.BDcommand.condition.append(f"UserID = {user.id}")
            Moderation.BDcommand.addition = "ORDER BY ID"
            
            result = Moderation.bdselect()
            Moderation.BDcommand.clear()
            i = 0
            j = 0
            arrs = list()
            warns = list()
            for warns in result:
                i += 1
                arrs.append(warns)
            if number > len(arrs):
                Embed.description = f"Варна с таким номером у <@{user.id}> - нет!"
            if str(result) != "[]":
                Moderation.BDcommand.table = "ListWarns"
                Moderation.BDcommand.condition = [f"UserID = {user.id}", f"AND ID = {arrs[number - 1][0]}"]
                
                result = Moderation.bddelete()
                Moderation.BDcommand.clear()
                if result == True:
                    Embed.description = f"Варн №{number} - удалён!"
                else:
                    Embed.description = str(result)
            else:
                Embed.description = "Варнов и так нет!"
        await interaction.followup.send(embed=Embed)
        
    @apc.command(name="lol")
    async def lol(self, interaction: discord.Interaction):
        """Роли"""
        await interaction.response.defer()

        roles = interaction.guild.get_role(814247807145869322)
        del_rol = interaction.guild.get_role(927164106312675359)
        lol = 0
        for member in interaction.guild.members:
            for role in member.roles:
                if role == del_rol:
                    await member.add_roles(roles)
                    await member.remove_roles(del_rol)
                    
                    lol += 1
        
        await interaction.followup.send(lol)
        Embed.clear_fields()