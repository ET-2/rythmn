This is a personal rythmn bot for Discord.
It uses the YoutubeDL library as well as the Discord library for Python.
Ever since rythmn bot was shut down I had no way of listening to music in Discord with my friends so I made a bot for us to play music.

Currently the bot can:
  - play single songs
  - play songs from a playlist
  - create new playlists
  - add or remove songs from playlists

*In order to use a command the '%' is typed at the beginning of the command
Commands:
  - '%play song_name' - plays song entered or if the bot is already playing music it will add the song to the end of the queue
  - '%playlist playlist_name' - adds songs in chosen playlist to the queue. You will be prompted y/n to shuffle playlist after entering the %playlist command
  - '%queue' - prints all songs in the queue
  - '%skip' - skips current song
  - '%repeat example_string' - repeats the string in Discord chat
  - '%kill' - ends the application requiring the bot to be restarted
  - '%menu' - displays all playlist commands
  - '%l' - lists the playlists
  - '%a' - creates new playlist
  - '%d' - deletes a playlist
  - '%ads' - adds a song to a playlist
  - '%ds' - deletes a song from a playlist
