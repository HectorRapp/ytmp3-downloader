from __future__ import unicode_literals
import youtube_dl
import sys

sys.path.insert(0, 'dll_files')

ydl_opts = {'format': 'bestaudio',
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320',
			}]
			}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])