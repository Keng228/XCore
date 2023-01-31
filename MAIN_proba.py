import discord
from LIB_config import TOKEN, MY_GUILD, Alpha, bot
import SEC_proba, SEC_mod, SEC_mus, SEC_econ, SEC_spec_emb, SEC_econadm, SEC_questsadm, SEC_quest, SEC_events

Embed = discord.Embed(
    title="Стандартный эмбед!",
    description="Сообщение!",
    color=0xAF69EF,
)

@bot.tree.command(guilds=[MY_GUILD, Alpha])
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'Modify {number=} {string=}', ephemeral=True)

@bot.tree.command(guilds=[MY_GUILD, Alpha], name="хелп")
async def help(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.defer()
    Embed.title = f"Помощь для {interaction.user.name}"
    Embed.description = "Я - бот XCore. Сейчас я нахожусь на стадии открытого тестирования. Если у тебя возникли вопросы или есть предложения - обратись к <@788883589987172442>"
    await interaction.followup.send(embed=Embed)



bot.tree.add_command(SEC_proba.general(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_mod.moderation(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_mus.music(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_econ.economy(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_econadm.admeconomy(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_spec_emb.spec_embed(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_questsadm.admquest(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_quest.quest(bot), guilds=[MY_GUILD, Alpha])
bot.tree.add_command(SEC_events.events(bot), guilds=[MY_GUILD, Alpha])

if __name__ == "__main__":
    bot.run(TOKEN)