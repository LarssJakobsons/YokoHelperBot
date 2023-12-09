from interactions import *

embed_modmail = Embed(
    title="Modmail",
    description="Click the button below to send a message to the mod mail",
    color=Color.from_hex("#b5b5b5"),
    footer=EmbedFooter(
        text="Unnecesary reports/messages will be ignored and/or punished"
    ),
)

embed_afterclick = Embed(
    title="Please select a reason",
    description="❕ If this was a mistake, ignore this message ❕",
    color=Color.from_hex("#b5b5b5"),
    footer=EmbedFooter(
        text="Unnecesary reports/messages will be ignored and/or punished"
    ),
)

components_modmail = [Button(style=ButtonStyle.GRAY, label="📨", custom_id="modmail_m")]

components_afterclick = [
    Button(style=ButtonStyle.GRAY, label="Partering", custom_id="partner_m", emoji="🤝"),
    Button(
        style=ButtonStyle.GRAY, label="Apply for mod", custom_id="apply_m", emoji="📝"
    ),
    Button(
        style=ButtonStyle.GRAY,
        label="Report a bug/permission leak",
        custom_id="bug_m",
        emoji="🐛,,"
    ),
    Button(
        style=ButtonStyle.GRAY, label="Report a user", custom_id="report_m", emoji="⚠️"
    ),
    Button(style=ButtonStyle.GRAY, label="Other", custom_id="other_m", emoji="🗯"),
]

components_channel = [
    Button(style=ButtonStyle.RED, label="Close mail", custom_id="close_m", emoji="🔒"),
]


modal_partner = Modal(
    ParagraphText(
        label="Why do you want to partner?",
        custom_id="partner_reason",
        placeholder="I wish to partner with yoko because...",
        required=True,
    ),
    ParagraphText(
        label="Your server advertisement",
        custom_id="partner_ad",
        placeholder="...",
        required=True,
    ),
    title="Become a partner!",
    custom_id="partner",
)

modal_apply = Modal(
    ParagraphText(
        label="Why do you wish to apply?",
        custom_id="apply_reason",
        placeholder="I wish to apply for mod because...",
        required=True,
    ),
    title="Apply for mod!",
    custom_id="apply",
)

modal_bug = Modal(
    ParagraphText(
        label="Please describe the bug/permission leak!",
        custom_id="bug_reason",
        placeholder="I found a bug...",
        required=True,
    ),
    ParagraphText(
        label="Anything else we should know?",
        custom_id="bug_other",
        placeholder="...",
        required=False,
    ),
    title="Report a bug/permission leak!",
    custom_id="bug",
)

modal_report = Modal(
    ParagraphText(
        label="Please describe the user and their rule breaking!",
        custom_id="report_reason",
        placeholder="This user is breaking rule...",
        required=True,
    ),
    ShortText(
        label="User/Message id and username:",
        custom_id="report_id",
        required=False,
        placeholder="...",
    ),
    ParagraphText(
        label="Anything else we should know?",
        custom_id="report_other",
        placeholder="...",
        required=False,
    ),
    title="Report a user!",
    custom_id="report",
)

modal_other = Modal(
    ParagraphText(
        label="Please describe your problem/reason!",
        custom_id="other_reason",
        placeholder="I have a problem with...",
        required=True,
    ),
    title="Other",
    custom_id="other",
)

modmail_category_id = 1177325562713346190


class ModMail(Extension):
    @slash_command(name="init_modmail", description="Initialize the modmail message")
    # @check(is_owner())
    async def init_modmail(self, ctx: InteractionContext):
        await ctx.send("Yippee", ephemeral=True)
        await ctx.channel.send(embed=embed_modmail, components=components_modmail)

    @listen()
    async def on_component(self, ctx: ComponentContext):
        ctx = ctx.ctx
        event_id = ctx.custom_id
        if event_id.endswith("_m"):
            if event_id.startswith("modmail"):
                await ctx.send(
                    embed=embed_modmail,
                    components=components_afterclick,
                    ephemeral=True,
                )
            elif event_id.startswith("close"):
                opener_id = int(ctx.channel.topic)
                permissions = [
                    PermissionOverwrite(deny=Permissions.VIEW_CHANNEL, type=OverwriteType.MEMBER, id=opener_id),
                    PermissionOverwrite(deny=Permissions.VIEW_CHANNEL, type=OverwriteType.ROLE, id=ctx.guild.default_role.id)
                ]
                await ctx.channel.edit(permission_overwrites=permissions)
                await ctx.message.channel.send(f"{ctx.author.mention} has closed this mail")
            else:
                if event_id.startswith("partner"):
                    await ctx.send_modal(modal=modal_partner)
                    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(
                        modal_partner
                    )
                    modmail_entry = f"Partnering request by <@{ctx.author.id}>\n```{modal_ctx.responses['partner_reason']}```\n\n{modal_ctx.responses['partner_ad']}"
                    modmail_channel_name = f"{ctx.author.display_name}'s partner mail"
                if event_id.startswith("apply"):
                    await ctx.send_modal(modal=modal_apply)
                    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal_apply)
                    modmail_entry = f"Mod application by <@{ctx.author.id}>\n```{modal_ctx.responses['apply_reason']}```"
                    modmail_channel_name = (
                        f"{ctx.author.display_name}'s mod application mail"
                    )
                if event_id.startswith("bug"):
                    await ctx.send_modal(modal=modal_bug)
                    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal_bug)
                    modmail_entry = f"Bug report by <@{ctx.author.id}>\n```{modal_ctx.responses['bug_reason']}```\n\n{modal_ctx.responses['bug_other']}"
                    modmail_channel_name = (
                        f"{ctx.author.display_name}'s bug report mail"
                    )
                if event_id.startswith("report"):
                    await ctx.send_modal(modal=modal_report)
                    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal_report)
                    modmail_entry = f"User report by <@{ctx.author.id}>\n```{modal_ctx.responses['report_reason']}```\n\n```{modal_ctx.responses["report_id"]}```\n\n{modal_ctx.responses['report_other']}"
                    modmail_channel_name = (
                        f"{ctx.author.display_name}'s user report mail"
                    )
                if event_id.startswith("other"):
                    await ctx.send_modal(modal=modal_other)
                    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal_other)
                    modmail_entry = f"Other by <@{ctx.author.id}>\n```{modal_ctx.responses['other_reason']}```"
                    modmail_channel_name = f"{ctx.author.display_name}'s mail"

                permissions = [
                    PermissionOverwrite(allow=Permissions.VIEW_CHANNEL, type=OverwriteType.MEMBER, id=ctx.author.id),
                    PermissionOverwrite(deny=Permissions.VIEW_CHANNEL, type=OverwriteType.ROLE, id=ctx.guild.default_role.id)
                ]

                category = await ctx.guild.fetch_channel(modmail_category_id)


                channel = await category.create_channel(
                    name=modmail_channel_name, permission_overwrites=permissions, channel_type=ChannelType.GUILD_TEXT, topic=str(ctx.author.id)
                )
                await channel.send(modmail_entry, components=components_channel)
                await channel.send(
                    "The staff team will get back to you as soon as possible."
                )

                await modal_ctx.send(f"Your modmail has been created at <#{channel.id}>", ephemeral=True)

def setup(bot):
    ModMail(bot)
