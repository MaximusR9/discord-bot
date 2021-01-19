import discord
from discord.ext import commands
import requests
import logging
import json
import random

# Init Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot Command Prefix
bot = commands.Bot(command_prefix='!')

# Gets a random inspirational quote from zenquotes.io
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@bot.event
async def on_ready():
    print('-------------------------------------')
    print('Logged in as')
    print(bot.user.name)
    print('-------------------------------------')
    # Set Bot Status
    await bot.change_presence(activity=discord.Game(name='OOF 1v1 / DM'))

# This event is executed whenever a command error occurs
@bot.event
async def on_command_error(ctx, error):
    """The event is triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """
    
    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
         return
    
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(':x:  You do not have the correct role for this command.')
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send(':x:  You do not have permission to do that!')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(':robot:  I do not have permission to do that!')
    if isinstance(error, commands.BadArgument):
        await ctx.send(f':exclamation:  Bad Argument. Type `!help {ctx.command}`')
#---------------------------------------------------------------------------------

#   Math Commands
@bot.command()
async def add(ctx, number1: int, number2: int):
    """
    Perform Addition
    """
    await ctx.send(number1 + number2)

@bot.command()
async def sub(ctx, number1: int, number2: int):
    """
    Perform Subtraction
    """
    await ctx.send(number1 - number2)

@bot.command()
async def mul(ctx, number1: int, number2: int):
    """
    Perform Multiplication
    """
    await ctx.send(number1 * number2)

@bot.command()
async def div(ctx, number1: int, number2: int):
    """
    Perform Division
    """
    await ctx.send(number1 / number2)
#---------------------------------------------------------------------------------

#   Fun / Misc Commands
@bot.command(name='dice')
async def dice(ctx):
    """
    Rolls a dice (from 1 to 6)
    """
    roll = random.randint(1, 6)
    await ctx.send(f"Dice: `{roll}`")

@bot.command(name='inspire')
async def inspire(ctx):
    """
    Shows a random inspirational quote from zenquotes.io
    """
    await ctx.send(get_quote())

@bot.command(name='joined')
async def joined(ctx, *, member: discord.Member):
    """
    Shows when a member joined.
    """
    await ctx.send(f'**{member.name}** joined in `{member.joined_at}`')

@bot.command(name='99')
async def nine_nine(ctx):
    """
    Shows a random quote from Brooklyn 99
    """
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='repeat')
async def repeat(ctx, times: int, *, message):
    """
    Repeat message n number of times
    """
    for i in range(times):
        await ctx.send(message)

@bot.command()
async def roll(ctx, dice: str):
    """
    Roll a dice
    """
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def slap(ctx, *, member: discord.Member):
    """
    Slaps member.
    """
    await ctx.send(f'**{ctx.author.mention}** slapped **{member.mention}**')

@bot.command()
async def wave(ctx, *, member: discord.Member):
    """
    Waves member.
    """
    await ctx.send(f'**{ctx.author.mention}** waves **{member.mention}**')
#---------------------------------------------------------------------------------

# OOF Commands
@bot.command(aliases=['forums'])
async def forum(ctx):
    """
    Shows OOF 1v1 DM Server's Forum
    """
    await ctx.send('Forum: **https://oofdm.cf**')

@bot.command()
async def invite(ctx):
    """
    Shows Discord Server's Invite Link
    """
    await ctx.send('Invite Link: **https://discord.com/invite/GeeTBqm**')

@bot.command()
async def ip(ctx):
    """
    Shows OOF 1v1 DM Server's IP
    """
    await ctx.send('Server IP: **play.oofdm.cf**')

@bot.command(aliases=['web'])
async def website(ctx):
    """
    Shows OOF 1v1 DM Server's Website
    """
    await ctx.send('Website: **https://oofdm.cf**')
#---------------------------------------------------------------------------------

# Admin Commands
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """
    Kicks user from server.
    This command is only for users with 'kick_members' permission
    """
    await member.kick(reason=reason)
    await ctx.send(f'**{member}** has been kicked by **{ctx.author.mention}**.')
    await ctx.send(f'Reason: **{reason}**')

@kick.error
async def kick_error(ctx, error):
    """
    Local error handler for kick command.
    """
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')

    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send('You forgot to provide member name!')

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Bot is missing kick_members permission.')

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    
#    if message.content.startswith('*hello'):
#        await message.channel.send('Hello')
#    
#    if message.content.startswith('*inspire'):
#        quote = get_quote()
#        await message.channel.send(quote)

bot.run('MzA4OTk3NzE3ODQ4NDg5OTg2.WQiujA.gISKZosef7z2xiS_2yrbLiUJg6k')