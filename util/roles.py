from interactions import *
import os

roles = {
    "red": 1175881619958140928,
    "green": 1175881583052468264,
    "yellow": 1175881663079780423,
    "blue": 1175881732403245076,
}

embed = Embed(
    title="Roles",
    description="Click the buttons to get the role",
    color=Color.from_hex("#b5b5b5"),
)
embed.add_field(name="Roles", value="🔴 Red\n🟢 Green\n🟡 Yellow\n🔵 Blue")

buttons = [
    Button(style=ButtonStyle.GRAY, label="🔴", custom_id="red_r"),
    Button(style=ButtonStyle.GRAY, label="🟢", custom_id="green_r"),
    Button(style=ButtonStyle.GRAY, label="🟡", custom_id="yellow_r"),
    Button(style=ButtonStyle.GRAY, label="🔵", custom_id="blue_r"),
]

class Roles(Extension):
    @slash_command(name="init_roles", description="Initialize the roles message")
    # @check(is_owner())
    async def init_roles(self, ctx: InteractionContext):
        components = ActionRow(*buttons)
        await ctx.send("Yippee", ephemeral=True)
        await ctx.channel.send(embed=embed, components=components)
    
    @listen()
    async def on_component(self, ctx: ComponentContext):
        event_id = ctx.ctx.custom_id
        if event_id.endswith("_r"):
            role = ctx.ctx.guild.get_role(roles[event_id.split("_")[0]])
            if role in ctx.ctx.author.roles:
                await ctx.ctx.author.remove_roles([role])
                await ctx.ctx.send("Removed role!", ephemeral=True)
            else:
                await ctx.ctx.author.add_roles([role])
                await ctx.ctx.send("Added role!", ephemeral=True)

def setup(bot):
    Roles(bot)