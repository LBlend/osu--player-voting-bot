from discord.ext import commands


def is_guild_member():
    def predicate(ctx):
        guild = ctx.bot.get_guild(565230012366848000)
        return ctx.author in guild.members
    return commands.check(predicate)
