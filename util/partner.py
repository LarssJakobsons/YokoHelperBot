from interactions import (
    Client,
    Button,
    VoiceState,
    slash_command,
    InteractionContext,
    context_menu,
    listen,
    Intents,
    Member,
    Embed,
    slash_option,
    Color,
    ActionRow,
    ComponentContext,
    spread_to_rows,
    ComponentContext,
    is_owner,
    OptionType,
    Permissions,
    SlashCommandChoice,
    ButtonStyle,
    check,
    Extension,
    EmbedFooter,
)
from interactions import ContextMenuContext, Message, message_context_menu
from interactions import Modal, ModalContext, ParagraphText, ShortText
import os
import re
from datetime import datetime
import json
import os


relative_path = "data/partners.json"
absolute_path = os.path.abspath(relative_path)

# Load the existing data from the JSON file
with open(absolute_path, "r", encoding="utf-8") as f:
    partner_spreadsheet = json.load(f)


async def add_partner_sheet(name, invite):
    partner_spreadsheet.append({"name": name, "invite": invite})
    with open(absolute_path, "w", encoding="utf-8") as f:
        json.dump(partner_spreadsheet, f, ensure_ascii=False, indent=4)


class partner(Extension):
    @message_context_menu(name="add partner")
    async def repeat(self, ctx: ContextMenuContext):
        addpartner = Modal(
            ShortText(
                label="Partner name",
                custom_id="name",
            ),
            ShortText(
                label="Server invite",
                custom_id="invite",
                placeholder="https://discord.gg/...",
            ),
            title="Add a partner",
            custom_id="addpartner",
        )

        total_partners = len(partner_spreadsheet)

        await ctx.send_modal(modal=addpartner)
        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(addpartner)

        # extract the answers from the responses dictionary
        server_name = modal_ctx.responses["name"]
        server_invite = modal_ctx.responses["invite"]
        if server_invite.startswith("https://discord.gg/"):
            server_invite = server_invite[19:]
        elif server_invite.startswith("https://discord.com/invite/"):
            server_invite = server_invite[26:]
        elif server_invite.startswith("discord.gg/"):
            server_invite = server_invite[11:]
        elif server_invite.startswith("discord.com/invite/"):
            server_invite = server_invite[18:]
        else:
            await modal_ctx.send("Buh what is that link that aint no invite buh", ephemeral=True)
            return
        if server_invite.endswith("/"):
            server_invite = server_invite[:-1]

        embed = Embed(
            title="New partnership!",
            description=f"""❕ Everybody say hello to our new partner, {server_name}!
❔ Total partners: {total_partners + 1}""",
            color=Color.from_hex("#ae3a7e"),
            footer=EmbedFooter(
                f"Partnered by {ctx.author.display_name}",
                icon_url=ctx.author.avatar.url,
            ),
            timestamp=datetime.utcnow(),
        )

        message: Message = ctx.target
        await message.reply(embed=embed, mention_author=False)

        await add_partner_sheet(server_name, server_invite)

        await modal_ctx.send("Partner successfully added :3", ephemeral=True)


def setup(bot):
    partner(bot)
