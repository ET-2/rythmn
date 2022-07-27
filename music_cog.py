'''A class for playing music in Discord. Utilizes discord library with YoutubeDL 
	to pull songs from youtube and stream to discord.
	Written by: 
	Ethan Timothy
	Source of tutorial and base code: https://www.youtube.com/watch?v=i0nNPidYQ2w&t=57s'''

import asyncio, datetime, discord, json, os, threading, time, random
from discord.ext import commands 
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.is_playing = False
		self.music_queue = []
		self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
		self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		self.vc = ""
		self.duration = int 

	#YoutubeDL searches query and extracts song info
	def search_yt(self, item):
		with YoutubeDL(self.YDL_OPTIONS) as ydl:
			try:
				info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
				self.duration = int(info['duration'])

			except Exception:
				return False

		return {'source': info['formats'][0]['url'], 'title': info['title'], 'webpage_url': info['webpage_url'], 'duration': info['duration']}
	
	#Handles playing the next song and managing the queue	
	async def play_next(self):
		if len(self.music_queue) > 0:
			print("----Playing Next Song----")
			self.is_playing = True

			m_url = self.music_queue[0][0]['source']
			if self.vc == "" or not self.vc.is_connected():
				self.vc = await self.music_queue[0][1].connect()
			elif self.vc.is_connected():
				pass
			else:
				self.vc = await self.bot.move_to(self.music_queue[0][1])

			current_play_time = self.music_queue[0][0]['duration']
			self.music_queue.pop(0)
			self.vc.stop()
			time.sleep(2)
			try:
				self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
				await asyncio.sleep(current_play_time)
				await self.play_next()
			except:
				print("Something didnt work...might want to restart")
			#play_time = threading.Timer(current_play_time, await self.play_next())
			#play_time.start()
			#time.sleep(self.duration)
			
			''', after=lambda e: self.play_next()'''

		else:
			self.is_playing = False
			

	#Public Commands

	'''Play a single song'''
	@commands.command()
	async def play(self, ctx, *args):
		query = " ".join(args)
		print(query)
		voice_channel = ctx.author.voice.channel
		if voice_channel is None:
			await ctx.send("You are not in a voice channel")
		else:
			song = self.search_yt(query)
			if type(song) == type(True):
				await ctx.send("Failed to download song, try again...")
			else:
				await ctx.send("Queued: " + song['title'] + '\nDuration: ' + str(datetime.timedelta(seconds = (song['duration']))) + '\n' + song['webpage_url'])

				self.music_queue.append([song, voice_channel])

				if self.is_playing == False:
					await self.play_next()

	'''Play a saved playlist'''
	@commands.command()
	async def playlist(self, ctx, args):
		voice_channel = ctx.author.voice.channel
		if voice_channel is None:
			await ctx.send("You are not in a voice channel")
		else:

			#Shuffle Descision
			await ctx.send('Set to shuffle?\n y/n:')
			continue_choice = await self.bot.wait_for('message')
			continue_choice = continue_choice.content

			#Shuffle = True
			if continue_choice == 'y':
				os.chdir(str(os.getcwd()))
				for file in os.listdir():
					if file.endswith(".json"):
						#check if file is empty
						if os.stat(file).st_size == 0:
							print("File is empty")
							break
						#if file is not empty, load in data
						f = open(file, "r")
						data = json.load(f)
						f.close()

						if args in data:
							song_list = []
							song_list = data[args]
							random.shuffle(song_list)
							for i in song_list:
								song = self.search_yt(i)
								if type(song) == type(True):
									await ctx.send("Failed to download song, try again...")
								else:
									await ctx.send("Queued: " + song['title'] + '\n' + song['webpage_url'])

									self.music_queue.append([song, voice_channel])
									
								if self.is_playing == False:
									await self.play_next()
						else:
							await ctx.send("Playlist Does Not Exist")
			
			#Shuffle = False				
			elif continue_choice != 'y':
				
				os.chdir(str(os.getcwd()))
				for file in os.listdir():
					if file.endswith(".json"):
						#check if file is empty
						if os.stat(file).st_size == 0:
							print("File is empty")
							break
						#if file is not empty, load in data
						f = open(file, "r")
						data = json.load(f)
						f.close()
						
						if args in data:
							for i in data[args]:
								song = self.search_yt(i)
								if type(song) == type(True):
									await ctx.send("Failed to download song, try again...")
								else:
									await ctx.send("Queued: " + song['title'] + '\n' + song['webpage_url'])

									self.music_queue.append([song, voice_channel])
									
								if self.is_playing == False:
									await self.play_next()
						else:
							await ctx.send("Playlist Does Not Exist")

	'''Show all songs in the queue'''
	@commands.command()
	async def queue(self, ctx):
		retval = ""
		for i in range(0, len(self.music_queue)):
			retval += '[' + str(i+1) + ']' + self.music_queue[i][0]['title'] + "\n"

		print(retval)
		if retval != "":
			await ctx.send(retval)
		else:
			await ctx.send("No music in queue")

	'''Skips the current playing song'''
	@commands.command()
	async def skip(self, ctx):
		if self.vc != "" and len(self.music_queue) != 0:
			await self.play_next()
			print("Music Queue Length: " + str(len(self.music_queue)))
		else:
			print("There is no more music in que. Stopping Bot...")
			self.vc.stop()
			self.is_playing = False
			
	'''Bot timeout listener'''
	'''@commands.Cog.listener()
	async def timeout(self):
		if self.is_playing == False:
			self.bot.disconnect()'''