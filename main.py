import interactions as inter
from interactions import *
import os
from dotenv import load_dotenv
import json
import asyncio
from datetime import datetime

load_dotenv()

intents: Intents = Intents.ALL

bot = inter.Client(
    sync_interactions=True, send_command_tracebacks=False, intents=intents
)

AutoRefreshMessage = None
AutoRefreshChannel = None
button = Button(style=ButtonStyle.GRAY, label="🔄", custom_id="refresh_ad")


def create_embed(goal, current):
    embed = Embed(
        title="Yoko stats",
        description=(
            f"""<a:icon:1176932612535758931> ｡⁺ ꔛ︰꒦ ꒷ ๑・── ・──・๑ ꒷ ꒦︰ꔛ ⁺ ｡<a:icon:1176932612535758931>
๑‧˚₊꒷꒦︶︶︶︶꒷꒦︶︶︶꒷꒦๑‧
ฅ ִ ֗ ۫ ִ ▹Mochi's : {current}
ฅ ִ ֗ ۫ ִ ▹Goal : {goal}
"""
        ),
        thumbnail="https://i.pinimg.com/736x/13/d2/0e/13d20ea2dee5dec738033482a8358bd4.jpg",
        images=[
            "https://i.pinimg.com/564x/8e/cd/fd/8ecdfd9fd22d5861859847c2af9959b9.jpg"
        ],
        footer=EmbedFooter(text="˚₊・︶︶︶꒦˚₊๑ Thank you for joining our community!! •.•"),
        timestamp=datetime.utcnow(),
        color=Color.from_hex("#edd1ad"),
    )
    return embed


@Task.create(IntervalTrigger(minutes=1))
async def automessage_send():
    global AutoRefreshMessage 
    if AutoRefreshMessage == None:
        AutoRefreshMessage = await AutoRefreshChannel.send(
            embed=create_embed(100, len(AutoRefreshChannel.guild.members)),
            components=ActionRow(button),
        )
    else:
        await AutoRefreshMessage.edit(
            embed=create_embed(100, len(AutoRefreshChannel.guild.members)),
            components=ActionRow(button),
        )


@listen()
async def on_component(ctx: ComponentContext):
    event_id = ctx.ctx.custom_id
    if event_id.endswith("_ad"):
        await ctx.ctx.send("Refreshed!", ephemeral=True)
        await AutoRefreshMessage.edit(
            embed=create_embed(len(AutoRefreshChannel.guild.members), 100),
            components=ActionRow(button),
        )


@listen()
async def on_ready():
    global AutoRefreshChannel
    AutoRefreshChannel = bot.get_guild(1175837825023889408).get_channel(
        1180915701884665937
    )
    print(f"Bot has logged in as {bot.user}")
    bot.load_extension("util.verify")
    bot.load_extension("util.roles")
    bot.load_extension("util.partner")
    bot.load_extension("util.info")
    bot.load_extension("util.modmail")

    automessage_send.start()
    await bot.change_presence(
        activity=Activity(
            name="you 👀",
            type=inter.ActivityType.WATCHING,
        )
    )


@slash_command(name="reload", description="Reloads an extension")
@check(is_owner())
@slash_option(
    name="extension",
    description="Extension to reload",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="verify", value="util.verify"),
        SlashCommandChoice(name="roles", value="util.roles"),
        SlashCommandChoice(name="partner", value="util.partner"),
        SlashCommandChoice(name="info", value="util.info"),
        SlashCommandChoice(name="modmail", value="util.modmail"),
    ],
)
async def reload(ctx: InteractionContext, extension: str):
    if extension is None:
        await bot.reload_extension("util.verify")
        await bot.reload_extension("util.roles")
        await bot.reload_extension("util.partner")
        await bot.reload_extension("util.info")
        await bot.reload_extension("util.modmail")
        await ctx.send("Reloaded!", ephemeral=True)
    else:
        bot.load_extension(extension)
        await ctx.send("Reloaded!", ephemeral=True)


secret_TOKEN = os.environ["TOKEN"]
bot.start(secret_TOKEN)
