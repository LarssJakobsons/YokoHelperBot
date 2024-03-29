from interactions import *

color = Color.from_hex("#e7a1ff")

info_main = [
    Embed(
        images=[
            "https://media.discordapp.net/attachments/1160669900516380795/1179132192203477063/bvcrn3y8.png?ex=6578ab6d&is=6566366d&hm=95fde5ce6c04b5a6c1d8fba0a22a013cdb4c39406b8031b40f523b6a615c71cf&=&format=webp&quality=lossless&width=1104&height=433"
        ],
        color=color,
    ),
    Embed(
        title="<a:icon:1176932612535758931> Information <a:icon:1176932612535758931>",
        description="""
⨯ . ⁺ ✦ ⊹ ꙳ ⁺ ‧ ⨯. ⁺ ✦ ⊹ . * ꙳ ✦ ⊹⨯ . ⁺ ✦ ⊹ ꙳ ⁺ ‧ ⨯. ⁺ ✦ ⊹ . * ꙳ ✦ ⊹
‧˚₊꒷୭୧︵︵✦︰Yoko ︰✦︵︵˚₊੭
**<a:2f2_0DecorButterfly:1185131268715843665> Our server is a cute wholesome server based on helping people and their mental health, while having a fun relaxing side for people to enjoy <a:2f2_0DecorButterfly:978400622611144724>**
<a:pink_heart~1t:1165567880528674867> This channel is used to provide information regarding Yoko.
🍙 Press the buttons below for more information!
︰๑‧˚₊꒷꒦₊˚꒷————꒰ఎ ♡ ໒꒱ ꒷˚₊੭————꒷꒦₊˚๑‧˚₊︰
""",
        color=color,
        images=[
            "https://media.discordapp.net/attachments/999867567093067797/1140053139324670052/2997795E-50AF-4AC4-A326-F6B82BF99BFB.png?width=636&height=25"
        ],
    ),
]

info_staff = Embed(
    title="🛠 Staff 🛠",
    description="""
    <@1026931524928536699> - Owner and creator
    <@737983831000350731> - Co owner and developer
    <@1175399006696902726> - Head mod
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
        global webhook
        # webhook = Webhook.from_url(
        #     url="https://discord.com/api/webhooks/1166005308922015744/9dR8f120iQW_Tg6T1XmaCVQUH5zrUWJh44_lYiuMrFtwQ7ahFch_mZLKa5FQw_LobIOq",
        #     client=self.bot,
        # )
        webhook = self.bot.get_channel(1160670578181681172)
        components = ActionRow(*buttons)
        await ctx.send("Yippee", ephemeral=True)
        await webhook.send(embed=info_main, components=components)

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
