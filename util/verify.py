from interactions import *
import os
import random
import json

buttons = [
    Button(style=ButtonStyle.GREEN, label="✅", custom_id="accept_v"),
    Button(style=ButtonStyle.GRAY, label="✖️", custom_id="deny_1_v"),
    Button(style=ButtonStyle.GRAY, label="✖️", custom_id="deny_2_v"),
    Button(style=ButtonStyle.GRAY, label="✖️", custom_id="deny_3_v"),
    Button(style=ButtonStyle.GRAY, label="✖️", custom_id="deny_4_v"),
]

embed = Embed(
    title="🎀 Verification",
    description="Click the ✅ button to verify yourself",
    color=Color.from_hex("#ae3a7e"),
    images=[
        "https://cdn.discordapp.com/attachments/1160669869566591037/1175894331551400086/imagefinal.png?ex=656ce3ef&is=655a6eef&hm=fc0810be446c91272f20450450b5ab470d184d8f30146ef1edadb9f1ad5c6144&"
    ],
)
embed.set_footer(text="Enjoy your stay!")

failed_attempters = {}


class Verify(Extension):
    @slash_command(
        name="init_verify", description="Initialize the verification message"
    )
    # @check(is_owner())
    async def init_verify(self, ctx: InteractionContext):
        global webhook
        # webhook = Webhook.from_url(
        #     url="https://discord.com/api/webhooks/1178441928052838531/tLqdnwUUvI70lUJyjqbsLiJ6wSFN_sdsUD9Wk_j0b_j0hlvUQFV3hQq4sMZmMo6YVo9s", client=self.bot
        # )
        webhook = self.bot.get_channel(1165407072129658960)
        components = ActionRow(*buttons)
        await ctx.send("Yippee", ephemeral=True)
        await webhook.send(embed=embed, components=components)

    @listen()
    async def on_component(self, ctx: ComponentContext):
        event_id = ctx.ctx.custom_id
        if event_id.endswith("_v"):
            if event_id.startswith("accept"):
                await ctx.ctx.send("Verified!", ephemeral=True)
                failed_attempters[ctx.ctx.author.id] = 0
                await ctx.ctx.author.add_roles([1160239355969941639])
            if event_id.startswith("deny"):
                if failed_attempters.get(ctx.ctx.author.id, 0) > 1:
                    try:
                        await ctx.ctx.author.send(
                            "Denied! You have been kicked from the server for too many failed attempts!"
                        )
                    except:
                        pass
                    await ctx.ctx.message.guild.kick(
                        ctx.ctx.author, reason="Too many failed verification attempts"
                    )
                    await self.bot.get_channel(1160669915754278982).send(
                        f"Kicked {ctx.ctx.author.mention} for too many failed verification attempts"
                    )
                    failed_attempters[ctx.ctx.author.id] = 0
                    return
                elif failed_attempters.get(ctx.ctx.author.id, 0) > 0:
                    await ctx.ctx.send(
                        "Denied! ⚠️ Last attempt! ⚠️",
                        ephemeral=True,
                    )
                else:
                    await ctx.ctx.send("Denied!", ephemeral=True)
                failed_attempters[ctx.ctx.author.id] = (
                    failed_attempters.get(ctx.ctx.author.id, 0) + 1
                )

            random.shuffle(buttons)
            components = ActionRow(*buttons)

            await ctx.ctx.message.edit(embed=embed, components=components)


def setup(bot):
    Verify(bot)
