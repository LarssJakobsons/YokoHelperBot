from interactions import *
import os
import random

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
    images=["https://cdn.discordapp.com/attachments/1160669869566591037/1175894331551400086/imagefinal.png?ex=656ce3ef&is=655a6eef&hm=fc0810be446c91272f20450450b5ab470d184d8f30146ef1edadb9f1ad5c6144&"]
)
embed.set_footer(text="Enjoy your stay!")


class Verify(Extension):
    @slash_command(
        name="init_verify", description="Initialize the verification message"
    )
    # @check(is_owner())
    async def init_verify(self, ctx: InteractionContext):
        components = ActionRow(*buttons)
        await ctx.send("Yippee", ephemeral=True)
        await ctx.channel.send(embed=embed, components=components)

    @listen()
    async def on_component(self, ctx: ComponentContext):
        event_id = ctx.ctx.custom_id
        if event_id.endswith("_v"):
            if event_id.startswith("accept"):
                await ctx.ctx.send("Verified!", ephemeral=True)
            if event_id.startswith("deny"):
                await ctx.ctx.send("Denied!", ephemeral=True)

            random.shuffle(buttons)
            components = ActionRow(*buttons)

            await ctx.ctx.message.edit(embed=embed, components=components)


def setup(bot):
    Verify(bot)
