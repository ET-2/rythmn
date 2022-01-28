"""
Playlist.py - Support list of methods within a class that will create and delete playlists
	for a locally host Rythm Bot. Within these playlists it will also be able to delete and 
	add songs to each created playlist.

Written by:
Andrew Edwards
"""
"""
Converted into a Discord Cog and made compatible with music_cog.py and bot.py by:
Ethan Timothy
"""

import os
import json
import discord
from discord.ext import commands

class Playlist(commands.Cog):

	#Loads Playlists from json upon instatiation
	def __init__(self, bot):
		self.bot = bot
		self.playlistdict = {}
		self.jsonfile = "playlists.json"
		self.__LoadPlaylists()
		
	#Private

	#loads in playlists from json file and creates dictionary
	def __LoadPlaylists(self):
		temp_array = []
		if 'playlists.json' in os.listdir():
			print('Loading Saved Playlist file...')

			f = open('playlists.json', "r")
			data = json.load(f)
			f.close()
			for dict_name in data:
				temp_array = []
				for song_name in data[dict_name]:
					temp_array.append(song_name)
				self.playlistdict[dict_name] = temp_array

	#Shows all the current playlists in memory
	async def __ListPlaylists(self, ctx):
		count = 0
		for key, value in self.playlistdict.items():
			await ctx.send('[' + str(count) + ']' + ' ' + str(key) + ' : ' + str('  |  '.join([str(elem) for elem in value])))
			count += 1

	#creates a new playlist, does not populate it
	async def __CreatePlaylist(self, ctx):
		await ctx.send("Enter a playlist name no longer than 32 characters: \n" + "Name must not contain spaces (use _'s instead):")
		playlist_name = await self.bot.wait_for('message')
		playlist_name = playlist_name.content

		if not str(playlist_name) or len(str(playlist_name)) > 32 or ' ' in str(playlist_name):
			await ctx.send("Playlist name is too long (32 chars), has spaces, or you did not enter one.")
			return
		else:
			self.playlistdict[playlist_name] = []
			await ctx.send("Playlist " + "*" + playlist_name + "*" + " has been created")
			with open(self.jsonfile, 'w') as outfile:
				json.dump(self.playlistdict, outfile)
				outfile.close()
			
	#Adds a song to a current playlist
	async def __AddSong(self, ctx):
		await self.__ListPlaylists(ctx)
		await ctx.send("\nEnter the playlist number: ")
		playlist = await self.bot.wait_for('message')
		playlist = playlist.content

		if int(playlist) <= len(self.playlistdict.keys()):
			while True:
				await ctx.send("Now the song you want to add: ")
				song_name = await self.bot.wait_for('message')
				song_name = song_name.content
				keys_list = list(self.playlistdict)
				key = keys_list[int(playlist)]
				temp_array = self.playlistdict[key]
				temp_array.append(song_name)
				self.playlistdict[key] = temp_array
				await ctx.send('*' + song_name + '*' + '  has been added to Playlist: ' + key)

				#Add another song
				await ctx.send('Add another song to the playlist?\n y/n:')
				continue_choice = await self.bot.wait_for('message')
				continue_choice = continue_choice.content
				if continue_choice == 'y':
					continue
				elif continue_choice != 'y':
					break

			with open(self.jsonfile, 'w') as outfile:
				json.dump(self.playlistdict, outfile)
				outfile.close()
			await ctx.send("Song(s) saved to playlist: " + str(key))
		else:
			await ctx.send("The playlist number you entered does not exist")
			return

	#Deletes a song from a current playlist
	async def __DeleteSong(self, ctx):
		await self.__ListPlaylists(ctx)
		playlist_todelfrom = ""
		song_todelfrom = ""

		await ctx.send("\nEnter the playlist number: ")
		playlist = await self.bot.wait_for('message')
		playlist = playlist.content

		if int(playlist) <= len(self.playlistdict.keys()):
			keys_list = list(self.playlistdict)
			key = keys_list[int(playlist)]
			await ctx.send("Now the song you want to delete: ")
			song_name = await self.bot.wait_for('message')
			song_name = song_name.content

			if song_name in self.playlistdict[key]:
				self.playlistdict[key].remove(song_name)
				await ctx.send('*' + song_name + '*' + ' has been removed from Playlist: ' + key)

				with open(self.jsonfile, 'w') as outfile:
					json.dump(self.playlistdict, outfile)
					outfile.close()
				return
			else:
				await ctx.send("The song you wanted to delete was not found.")
				return
		else:
			await ctx.send("The playlist number you entered does not exist")
			return

	#Deletes a current playlist
	async def __DeletePlaylist(self, ctx):
		await self.__ListPlaylists(ctx)
		await ctx.send("Enter the number of the playlist you want to delete: ")
		playlist = await self.bot.wait_for('message')
		playlist = playlist.content
		
		if int(playlist) <= len(self.playlistdict.keys()):
			keys_list = list(self.playlistdict)
			key = keys_list[int(playlist)]
			self.playlistdict.pop(key)
			await ctx.send("The playlist " + "*" + key + "*" + " has been deleted")

			with open(self.jsonfile, 'w') as outfile:
				json.dump(self.playlistdict, outfile)
				outfile.close()
		else:
			await ctx.send("The playlist number you entered does not exist")
			return

	# Public Commands

	@commands.command()
	async def menu(self, ctx):
		await ctx.send("\n%l -> Lists all playlists\n%a -> Creates a new playlist\n%d -> Delete a playlist\n%ads -> Add a song to a playlist\n%ds -> Delete a song from a playlist\n")

	@commands.command()
	async def l(self, ctx):
		await self.__ListPlaylists(ctx)

	@commands.command()
	async def a(self, ctx):
		await self.__CreatePlaylist(ctx)

	@commands.command()
	async def d(self, ctx):
		await self.__DeletePlaylist(ctx)

	@commands.command()
	async def ads(self, ctx):
		await self.__AddSong(ctx)

	@commands.command()
	async def ds(self, ctx):
		await self.__DeleteSong(ctx)






	
	
