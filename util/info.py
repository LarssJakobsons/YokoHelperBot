from interactions import *

color = Color.from_hex("#e7a1ff")

info_main = Embed(
    title="<a:icon:1176932612535758931> Information <a:icon:1176932612535758931>",
    description="""
**💕Our server is a cute wholesome server based on helping people and their mental health, while having a fun relaxing side for people to enjoy💕**
❕ This channel is used to provide information regarding Yoko.
🍙 Press the buttons below for more information!
︰๑‧˚₊꒷꒦₊˚꒷————꒰ఎ ♡ ໒꒱ ꒷˚₊੭————꒷꒦₊˚๑‧˚₊︰
""",
    color=color,
    images=[
        "https://media.discordapp.net/attachments/999867567093067797/1140053139324670052/2997795E-50AF-4AC4-A326-F6B82BF99BFB.png?width=636&height=25"
    ],
)

info_staff = Embed(
    title="🛠 Staff 🛠",
    description="""
    <@1026931524928536699> - Owner and creator
    <@737983831000350731> - Mod and Developer
    """,
    images=[
        "https://media.discordapp.net/attachments/999867567093067797/1140053139324670052/2997795E-50AF-4AC4-A326-F6B82BF99BFB.png?width=636&height=25"
    ],
    color=color,
)

info_achievements = Embed(
    title="🏅 Achievements and Levels 🏅",
    description="""
<@&1166018762827378698> - Ability to view icon and decor channels
<@&1166018785933795389> - Ability to send links and media
<@&1166018803377913866> - Ability to use external emotes and stickers
<@&1166018820415172670> - Albility to change your nickname
<@&1166018836278038629> - Ability to add your own emote
<@&1166018852065386536> - Ability to receive a custom colour role
""",
    images=[
        "https://media.discordapp.net/attachments/999867567093067797/1140053139324670052/2997795E-50AF-4AC4-A326-F6B82BF99BFB.png?width=636&height=25"
    ],
    footer=EmbedFooter(text="More roles coming soon!"),
    color=color,
)

info_booster = Embed(
    title="💎 Booster perks 💎",
    description="""
- Special role and colour customised by you for you.

- Ability to change nickname

- Able to use external emotes and stickers

- Media and link permission

- 2 entries for giveaways.
""",
    images=[
        "https://media.discordapp.net/attachments/999867567093067797/1140053139324670052/2997795E-50AF-4AC4-A326-F6B82BF99BFB.png?width=636&height=25"
    ],
    footer=EmbedFooter(text="Bruh yui idk what to put here"),
    color=color,
)

buttons = [
    Button(style=ButtonStyle.GRAY, emoji="🛠", custom_id="staff_i", label="Staff"),
    Button(
        style=ButtonStyle.GRAY,
        emoji="🏅",
        custom_id="achievements_i",
        label="Achievements and Levels",
    ),
    Button(
        style=ButtonStyle.GRAY,
        emoji="<a:icon:1176932612535758931>",
        custom_id="booster_i",
        label="Booster perks",
    ),
]


class Info(Extension):
    @slash_command(name="init_info", description="Initialize the info message")
    # @check(is_owner())
    async def init_info(self, ctx: InteractionContext):
        components = ActionRow(*buttons)
        await ctx.send("Yippee", ephemeral=True)
        await ctx.channel.send(embed=info_main, components=components)

    @listen()
    async def on_component(self, ctx: ComponentContext):
        event_id = ctx.ctx.custom_id
        if event_id.endswith("_i"):
            if event_id.startswith("staff"):
                await ctx.ctx.send(embed=info_staff, ephemeral=True)
            if event_id.startswith("achievements"):
                await ctx.ctx.send(embed=info_achievements, ephemeral=True)
            if event_id.startswith("booster"):
                await ctx.ctx.send(embed=info_booster, ephemeral=True)


def setup(bot):
    Info(bot)
