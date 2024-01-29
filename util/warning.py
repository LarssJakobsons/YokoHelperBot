from interactions import *
import re
from datetime import timedelta, datetime

guild = 1175837825023889408
warning1 = 1195849756010893422
warning2 = 1195849793180794960
warning3 = 1195849815653884006
warning4 = 1195849834746351727

re_td = re.compile(r"(\d+)(w|d|h|m)")
units = {
    "w": "weeks",
    "d": "days",
    "h": "hours",
    "m": "minutes",
}


def to_timedelta(string):
    total_seconds = 0
    matches = re_td.findall(string)
    if not matches:
        return 404
    try:
        for val, u in matches:
            val = int(val)
            if u == "w":
                total_seconds += val * timedelta(weeks=1).total_seconds()
            else:
                total_seconds += val * timedelta(**{units[u]: 1}).total_seconds()
    except:
        return 400

    if total_seconds > 60 * 60 * 24 * 7:
        return 429
    else:
        return timedelta(seconds=0)


class Warning(Extension):
    @slash_command(name="warn", description="Warn a user")
    @slash_option(
        name="user",
        description="User to warn",
        required=True,
        opt_type=OptionType.USER,
    )
    @slash_option(
        name="reason",
        description="Reason for warning",
        required=True,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="duration",
        description="Duration of warning (e.g. 1d, 1w, 1h, 1min)",
        required=False,
        opt_type=OptionType.STRING,
    )
    async def warn(
        self, ctx: InteractionContext, user: User, reason: str, duration: str = None
    ):
        if self.bot.get_guild(guild).get_role(warning4) in user.roles:
            timeout_till = None
            await ctx.send("Banned user :3", ephemeral=True)
            await ctx.channel.send(
                f'{user.mention} has been banned from the server for "{reason}".'
            )
            await user.send(f'You have been banned from the server for "{reason}".')
            await user.ban(reason="Exceeded maximum number of warnings")
        elif self.bot.get_guild(guild).get_role(warning3) in user.roles:
            timeout_till = datetime.now() + timedelta(days=7)
            await ctx.send("Warned user :3 (4th)", ephemeral=True)
            await user.add_role(self.bot.get_guild(guild).get_role(warning4))
            await ctx.channel.send(f"{user.mention} has been warned for {reason}.")
            await user.send(f'You have been warned for "{reason}".')
        elif self.bot.get_guild(guild).get_role(warning2) in user.roles:
            timeout_till = datetime.now() + timedelta(days=5)
            await ctx.send("Warned user :3 (3rd)", ephemeral=True)
            await user.add_role(self.bot.get_guild(guild).get_role(warning3))
            await ctx.channel.send(f"{user.mention} has been warned for {reason}.")
            await user.send(f'You have been warned for "{reason}".')
        elif self.bot.get_guild(guild).get_role(warning1) in user.roles:
            timeout_till = datetime.now() + timedelta(days=1)
            await ctx.send("Warned user :3 (2nd)", ephemeral=True)
            await user.add_role(self.bot.get_guild(guild).get_role(warning2))
            await ctx.channel.send(f"{user.mention} has been warned for {reason}.")
            await user.send(f'You have been warned for "{reason}".')
        else:
            timeout_till = datetime.now() + timedelta(hours=1)
            await ctx.send("Warned user :3 (1st)", ephemeral=True)
            await user.add_role(self.bot.get_guild(guild).get_role(warning1))
            await ctx.channel.send(f"{user.mention} has been warned for {reason}.")
            await user.send(f'You have been warned for "{reason}".')

        if duration != None:
            if to_timedelta(duration) == 404:
                await ctx.send(
                    "No known matches in duration prompt. Using default timeout times.",
                    ephemeral=True,
                )
                user.timeout(timeout_till, reason=reason)
            elif to_timedelta(duration) == 400:
                await ctx.send(
                    "Invalid duration in duration prompt. Using default timeout times.",
                    ephemeral=True,
                )
                user.timeout(timeout_till, reason=reason)
            elif to_timedelta(duration) == 429:
                await ctx.send(
                    "Duration too long for a timeout in duration prompt. Using max timeout time (7 days).",
                    ephemeral=True,
                )
                user.timeout(datetime.now() + timedelta(days=7), reason=reason)
            else:
                timeout_till = datetime.now() + to_timedelta(duration)
                await user.timeout(timeout_till, reason=reason)
        else:
            await user.timeout(timeout_till, reason=reason)


def setup(bot):
    Warning(bot)
