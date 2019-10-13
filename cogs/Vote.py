from discord.ext import commands
import discord

import pymongo
from codecs import open

from cogs.utils import Defaults, Checks, OsuUtils


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_users = pymongo.MongoClient(bot.database)['osu-top-players-voting']['users']

    @Checks.is_guild_member()
    @commands.dm_only()
    @commands.command()
    async def stem(self, ctx, posisjon: int, *, spiller: str):
        """Gi en spiller en stemme"""

        query = {'_id': ctx.author.id}
        try:
            db_user = self.db_users.find_one(query)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        spiller = spiller.lower()

        if posisjon > 10 or posisjon < 1:
            return await Defaults.error_warning_send(ctx, text='Du kan bare sette rangering mellom 1-10')
        
        if db_user is None:
            self.db_users.insert_one({
                '_id': ctx.author.id,
                '1': None,
                '2': None,
                '3': None,
                '4': None,
                '5': None,
                '6': None,
                '7': None,
                '8': None,
                '9': None,
                '10': None})
            db_user = self.db_users.find_one(query)

        with open('./assets/top_50_norway.txt', 'r', encoding='utf-8') as f:
            top_50_norway = [line.rstrip('\r\n') for line in f]

        if spiller not in top_50_norway:
            return await Defaults.error_warning_send(ctx, text='Brukeren er ikke på [lista](https://gist.github.com/ + '
                                                               'LBlend/6cc58ee838d928032df48740c313fec6)')

        for key, value in db_user.items():
            if value == spiller:
                self.db_users.update_one(query, {'$set': {f'{key}': None}})

        self.db_users.update_one(query, {'$set': {f'{posisjon}': spiller}})

        spiller = await OsuUtils.convert_name(spiller)

        embed = discord.Embed(color=discord.Color.green(),
                              description=f':white_check_mark: Du har satt **{spiller}** som ditt {posisjon}. valg!')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command(aliases=['stemmer'])
    async def minestemmer(self, ctx):
        """Se hvem du har stemt på"""

        query = {'_id': ctx.author.id}
        try:
            db_user = self.db_users.find_one(query)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        if db_user is None:
            return await Defaults.error_warning_send(ctx, text='Du har ikke stemt på noen')

        votes = ''
        for key, value in db_user.items():
            if key != '_id':
                if value is None:
                    value = ''
                value = await OsuUtils.convert_name(value)
                votes += f'**{key}.** {value}\n'

        embed = discord.Embed(color=ctx.me.color, description=votes)
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command()
    async def fjernstemmer(self, ctx):
        """Fjerner alle stemmene dine"""

        query = {'_id': ctx.author.id}
        try:
            db_user = self.db_users.find_one(query)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        if db_user is None:
            return await Defaults.error_warning_send(ctx, text='Du har ikke stemt på noen')

        self.db_users.delete_one(query)

        embed = discord.Embed(color=discord.Color.green(), description='Alle stemme dine er nå fjernet!')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def kandidater(self, ctx):
        """Viser kandidatene"""

        embed = discord.Embed(color=ctx.me.color, title='Kandidater',
                              description='[Trykk her for å se lista](https://gist.github.com/' +
                                          'LBlend/6cc58ee838d928032df48740c313fec6)')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def resultat(self, ctx):
        """Viser resultatet for øyeblikket"""

        query = {'_id': ctx.author.id}
        try:
            self.db_users.find_one(query)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        players = {}
        voters = 0
        for i in self.db_users.find():
            voters += 1
            for key, value in i.items():
                if key != '_id' and value is not None:
                    try:
                        players[f'{value}']
                    except KeyError:
                        players[f'{value}'] = await OsuUtils.convert_score(key)
                        continue
                    players[f'{value}'] += await OsuUtils.convert_score(key)
                    
        players = sorted(players.items(), key=lambda x: x[1], reverse=True)

        leaderboard = ''
        for i in players:
            player = await OsuUtils.convert_name(i[0])
            score = i[1]
            leaderboard += f'**{player}**: {score}\n'

        embed = discord.Embed(color=ctx.me.color, title='Stilling', description=leaderboard)
        embed.set_footer(text=f'Antall som har stemt: {voters}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Vote(bot))
