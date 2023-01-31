import discord
from discord.ext import commands
from discord import app_commands as apc
import youtube_dl
from LIB_config import bot
from LIB_music import YTDLSource, Song, VoiceState
from LIB_music import YTDLError, DowloadError
import math

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}


ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class music(apc.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.voice_states = {}
        self.voice_state = {}

    def get_voice_state(self, ctx: commands.Context):
        #state = self.voice_states.get(ctx.guild.id)
        state = VoiceState(self.bot, ctx)
        self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Эта команда не используется в ЛС (Личные сообщения)')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        self.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Меня это пугает. Произошла какая-то ошибка: {}'.format(str(error)))
        

    @apc.command(name="подключить")
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel = None):
        """Подключение к голосовому чату"""
        Embed.title = "Музыка"
        
        if channel == None and interaction.user.voice.channel != None:
            channel = interaction.user.voice.channel
        if str(self.bot.voice_clients) != "[]":
            await self.bot.voice_clients[0].disconnect()
        if interaction.user.voice != None:
            await channel.connect()
            Embed.description=f"Подключено к: <#{channel.id}>"

        if interaction.user.voice.channel == None:
            Embed.description="Вы не подключены к голосовому чату!"
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="отключить")
    async def disconnect(self, interaction: discord.Interaction):
        """Отключение от голосового чата"""
        Embed.title = "Музыка"
        if str(self.bot.voice_clients) != "[]":
            Embed.description = f"Выход произведён из:\n<#{self.bot.voice_clients[0].channel.id}>"
            self.voice_state.songs.clear()
            await self.voice_state.stop()
        else:
            Embed.description = "Выходить неоткуда"
        await interaction.response.send_message(embed=Embed)

    @apc.command(name="плей")
    async def play(self, interaction: discord.Interaction, *, url: str):
        """Начать воспроизведение музыки по ссылке: желательно только Ютуб и Саундклауд (на счёт других очень сомневаюсь что сработает)"""
        ctx = await commands.Context.from_interaction(interaction)
        await interaction.response.defer()
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            
        try:
            source = await YTDLSource.create_source(ctx, url, loop=self.bot.loop)
            url = source.url
            Embed.description = 'Успешно добавлено {}\n'.format(str(source))
            Embed.title = "Музыка"
        except YTDLError as e:
            Embed.description = 'Произошла ошибка при обработке этого запроса: {}'.format(str(e))
        except DowloadError as e:
            Embed.description = 'Произошла ошибка при обработке этого запроса: {}'.format(str(e))
        else:
            song = Song(source)
            await self.cog_before_invoke(ctx)
            self.voice_state.voice = bot.voice_clients[0]
            await self.voice_state.songs.put(song)
        await interaction.followup.send(embed=Embed)
            
    @apc.command(name="громкость")
    async def volume(self, interaction: discord.Interaction, volume: int):
        """Устанавливает громкость музыки"""
        Embed.title = "Музыка"

        if self.bot.voice_clients[0].is_playing() == False:
            Embed.description = "Бот ничего не играет!"
            return await interaction.response.send_message(embed=Embed)

        self.bot.voice_clients[0].source.volume = volume / 100
        Embed.description = "Установленная громкость равна {}%".format(volume)
        await interaction.response.send_message(embed=Embed)

    @apc.command(name="стоп")
    async def stop(self, interaction: discord.Interaction):
        """Полностью остановить проигрывание музыки"""
        Embed.title = "Музыка"
        
        self.voice_state.songs.clear()
        self.voice_state.voice.stop()
        Embed.description = "Стоп! ⏹️"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="пауза")
    async def pause(self, interaction: discord.Interaction):
        """Приостановить проигрывание музыки"""
        Embed.title = "Музыка"
        
        self.voice_state.voice.pause()
        Embed.description = "Пауза! ⏸️"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="продолжить")
    async def resume(self, interaction: discord.Interaction):
        """Продолжить проигрывание музыки"""
        Embed.title = "Музыка"
        
        self.voice_state.voice.resume()
        Embed.description = "Продолжаем! ▶️"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="пропустить")
    async def skip(self, interaction: discord.Interaction):
        """Пропустить трек"""
        Embed.title = "Музыка"
        
        self.voice_state.skip()
        Embed.description = "Пропуск! ⏩"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="перемешка")
    async def snuffle(self, interaction: discord.Interaction):
        """Перемешать треки"""
        Embed.title = "Музыка"
        
        self.voice_state.songs.shuffle()
        Embed.description = "Перемешка! 🔀"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="цикл")
    async def loop(self, interaction: discord.Interaction):
        """Зациклить один трек"""
        Embed.title = "Музыка"
        
        self.voice_state.loop = not self.voice_state.loop
        if self.voice_state.loop == True:
            Embed.description = f"Зацикливаем! 🔁"
        else:
            Embed.description = f"Цикл выключен! ▶️"
        
        await interaction.response.send_message(embed=Embed)
        
    @apc.command(name="список")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        """Показать плейлист"""
        Embed.title = "Музыка"
        if len(self.voice_state.songs) == 0:
            Embed.description = 'В очереди нет треков. Можете добавить.'
            return await interaction.response.send_message(embed=Embed)

        items_per_page = 10
        pages = math.ceil(len(self.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(self.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        Embed.description=('**{} tracks:**\n\n{}'.format(len(self.voice_state.songs), queue))
        Embed.set_footer(text='Viewing page {}/{}'.format(page, pages))
        await interaction.response.send_message(embed=Embed)
        
        
        
        


    #@apc.command()
    #async def play(self, interaction: discord.Interaction, query: str):
    #    """Играет файл из файловой системы"""
    #    
    #    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #    self.bot.voice_clients[0].play(source=source, after=lambda e: print('Player error: %s' % e) if e else None)
    #    Embed.title = "Музыка"
    #    Embed.description = 'Now playing: {}'.format(query)
    #    await interaction.response.send_message(embed=Embed)

#    @play.before_invoke
#    @yt.before_invoke
#    @stream.before_invoke
#    async def ensure_voice(self, ctx):
#        if ctx.voice_client is None:
#            if ctx.author.voice:
#                await ctx.author.voice.channel.connect()
#            else:
#                await ctx.send("You are not connected to a voice channel.")
#                raise apc.CommandError("Author not connected to a voice channel.")
#        elif ctx.voice_client.is_playing():
#            ctx.voice_client.stop()
#
#def setup(client):
#    client.add_cog(Music(client))
#    print('Music: activated')