import discord, asyncio
from async_timeout import timeout
from discord import app_commands as apc
from discord.ext import commands
from LIB_conctDB import Moderation
from datetime import date
from LIB_config import derectory
from random import randint


#---Массивы для проверок---
mass_tug = ["xcore ты говорить умеешь", "xcore ты умеешь говорить", 
"xcore, ты умеешь говорить", "xcore, ты говорить умеешь", "xcore можешь что-нибудь сказать",
"xcore, можешь сказать что-нибудь", "xcore можешь сказать что-нибудь", "xcore, можешь что-нибудь сказать"]
mass_lust = ["<:lasttimoha:1008363099188891778>", "<:lastsans:852915030504767508>",
"<:xasrielpleasured:989914068225781792>", "😳", "16+", "18+"]
mass_sheip = ["шейп", "шэйп", "shape"]
mass_parody = ["кор превратился в паци?", "xcore - пародия на паци", "паци и есть кор",
"xcore превратился в паци?", "паци и есть xcore"]
#---Переменные "Ты умеешь говорить?"---
prv_tug_bool = False
prv_tug_user = 0
prv_tug_chan = 0
prv_tug_mess_id = 0
prv_tug_mess_id2 = 1

Embed = discord.Embed(
    title="Ответ!",
    description="Сообщение!",
    color=0xAF69EF,
)

class events(apc.Group):
    """moderation commands"""
    def __init__(self, Bot: commands.Bot):
        super().__init__()
        self.Bot = Bot
        Bot = Bot

        #Событие: присоединение участника

        async def on_member_join(member: discord.Member):
            channel = Bot.get_channel(1044011594188861580) #member.guild.system_channel

            Embed.title="Новый участник!"
            Embed.description=f"{member.name}"
            
            await channel.send(embed=Embed)

        #Событие: отправка сообщения
        @Bot.event
        async def on_message(message: discord.Message):
            await Bot.process_commands(message)
            audit_chan = Bot.get_channel(1044011594188861580)
            Embed.title="Новое сообщение!"
            if (message.author.id != 1035628913696710827) and (message.channel.id != 1044011594188861580):
                print(f'Message from {message.author}: {message.content} (#{message.channel})')
                
                url = message.jump_url
                if message.embeds != [] and message.content == "":
                    app = [Embed, message.embeds[0]]
                    Embed.description=f"Автор: {message.author}\nКанал: <#{message.channel.id}>\n Тип: __**Эмбед от бота**__\nСсылка: {url}"
                    await audit_chan.send(embeds=app)
                else:
                    Embed.description=f"Автор: {message.author}\nКанал: <#{message.channel.id}>\nСообщение: <{message.content}>\nСсылка: {url}"
                    await audit_chan.send(embed=Embed)
            
            #---Открытие веток анкет--
            if (message.channel.id == 1001797311367757885 or message.channel.id == 969484285306339368) and message.content.startswith("Анкета"):
                
                index = message.content.find("Имя:")
                strok = message.content[index+4:len(message.content)]
                name = strok.split("\n")[0]
                
                index = message.content.find("АВ:")
                strok = message.content[index+4:len(message.content)]
                au = strok.split("\n")[0]
                
                tread = await message.create_thread(name=f"Проверка -{name} ({au})")
                role = message.guild.get_role(958765340240773160)
                if role == None:
                    role = message.guild.get_role(1068488124583399464)
                await message.author.add_roles(role)
                await message.add_reaction("🤖")
                await tread.send("Ваша проверка скоро начнётся. Ожидайте. . .")
                if message.attachments == []:
                    await tread.send("У вашей анкеты нет арта! Пожалуйста, отправьте его в эту ветку!")
            
            # ---Привет---
            if message.content.find("Привет") != -1 or message.content.find("привет") != -1:
                await message.add_reaction("👋")
        
            
            if message.channel.id == 970176267850776606 and message.author.id != 1035628913696710827:
                
                #Всякие переменные
                Shaip = False
                Lust = False
                Parody = False
                
                # ---Ты умеешь говорить?---
                global prv_tug_bool
                global prv_tug_user
                global prv_tug_chan
                global prv_tug_mess_id
                global prv_tug_mess_id2
                if message.reference != None:
                    prv_tug_mess_id2 = message.reference.message_id
                if (prv_tug_bool == True and prv_tug_user == message.author.id and prv_tug_chan == message.channel.id):
                    Embed.title=""
                    mes = message.content
                    if message.content.lower().find("скажи") != -1:
                        mes = message.content[message.content.lower().find("скажи") + 6:]
                    Embed.description = mes
                    await message.channel.send(embed=Embed, reference=message)
                    prv_tug_bool = False
                else:
                    for tug in mass_tug:
                        if message.content.lower().find(tug) != -1:
                            prv_tug_bool = True
                            prv_tug_user = message.author.id
                            prv_tug_chan = message.channel.id
                            prv_tug_mess_id = message.id
                            await message.channel.send("А что надо сказать?", reference=message)
                
                # ---Пародия на Паци---
                for parody in mass_parody:
                    if message.content.lower().find(parody) != -1:
                        await message.channel.send("Сам такой-", reference=message)
                
                #---Lust---
                for lust in mass_lust:
                    if message.content.lower().find(lust) != -1:
                        Lust = True
                if Lust == True:
                    await message.channel.send(file=discord.File('XCorn.png'), reference=message)
                    Lust = False
                
                #---Shape---
                if message.id == 1:
                    for shape in mass_sheip:
                        if message.content.lower().find(shape) != -1:
                            Shaip = True
                    if Shaip == True:
                        ran = randint(1, 2)
                        await message.channel.send(file=discord.File(f"{ran}sheip.png"), reference=message)
                        Shaip = False
                    
        @Bot.event
        async def on_guild_channel_create(channel: discord.TextChannel):
            if channel.category_id == 888504823488602144:
                history = channel.history(1)
                await discord.Message(history[0]).add_reaction('🔄')
                
        #@Bot.event
        #async def on_thread_create(thread: discord.Thread):
            
                
        @Bot.event
        async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
            if user.id == 704408267907924058 and reaction.message.channel.id == 970176267850776606:
                    await reaction.message.channel.send(f"Паци ставит {reaction.emoji}")