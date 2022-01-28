'''Ethan Timothy - Personal Music Bot
	This file instantiates the bot and adds all
	cogs to the bot'''

import discord
from discord.ext import commands
from music_cog import music_cog
from Playlist import Playlist

#Instantiates Bot / Assigns the % as the command ID for Discord chat
Bot = commands.Bot(command_prefix='%')

#Adds cogs from other files to the Bot
Bot.add_cog(music_cog(Bot))
Bot.add_cog(Playlist(Bot))

'''Public Commands'''
#Repeats the string typed
@Bot.command()
async def repeat(ctx, *args):
	str_args = " ".join(args)
	await ctx.send(str_args)

#Force shut down through chat
@Bot.command()
async def kill(ctx):
	exit()

#Grabs token and starts the bot
token = str
with open("token.txt") as file:
	token = file.read()
print("----------Rythmn is Starting Up----------")	
Bot.run(token)