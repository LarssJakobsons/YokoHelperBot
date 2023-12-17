from interactions import *


embeds_modmail = [
    Embed(
        color=Color.from_hex("#52e3ab"),
        images=["https://cdn.discordapp.com/attachments/1175837826475102241/1184908005590958160/21522863fba6eeee04b07aa57dc7b271.png?ex=658dae93&is=657b3993&hm=523a6d3848aa9736da7cef80d8a2d29cc4e09d556dd6e4e21bc90d1645260f51&"],
    ),
    Embed(
    title="<a:a_blue_star:1160835426387513424> Create a ticket! <a:a_blue_star:1160835426387513424>",
    description="Click the button below to create a ticket!",
    color=Color.from_hex("#52e3ab"),
    footer=EmbedFooter(
        text="Please use this for tickets only, not for general questions!"
    ),
    images=["https://cdn.discordapp.com/attachments/1175837826475102241/1184908211145429062/786774d88aee8486cb6106b8de8f0916.png?ex=658daec4&is=657b39c4&hm=446c5cdf4488a5be5e53e54805b2d50ebc0f5b6ea3d834bbd81bab837b1a7de5&"]
)]

embed_afterclick = Embed(
    title="<a:ramspin:1185560689998303362> Please select a reason <a:RemSpin:1180780686748176384>",
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
        emoji="🐛"
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
        label="Describe the user and their rule break!",
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

modmail_category_id = 1184943414689669190


class ModMail(Extension):
    @slash_command(name="init_modmail", description="Initialize the modmail message")
    # @check(is_owner())
    async def init_modmail(self, ctx: InteractionContext):
        await ctx.send("Yippee", ephemeral=True)
        await self.bot.get_channel(1166659449356824688).send(embed=embeds_modmail, components=components_modmail)

    @listen()
    async def on_component(self, ctx: ComponentContext):
        ctx = ctx.ctx
        event_id = ctx.custom_id
        if event_id.endswith("_m"):
            if event_id.startswith("modmail"):
                await ctx.send(
                    embed=embeds_modmail,
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
                    PermissionOverwrite(deny=Permissions.VIEW_CHANNEL, type=OverwriteType.ROLE, id=ctx.guild.default_role.id),
                    PermissionOverwrite(allow=Permissions.VIEW_CHANNEL, type=OverwriteType.ROLE, id=1162627137723977748),
                    PermissionOverwrite(allow=Permissions.VIEW_CHANNEL, type=OverwriteType.ROLE, id=1162627034334384258),
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
