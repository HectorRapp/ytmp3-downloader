from __future__ import unicode_literals
import youtube_dl

#TODO hacer la funcion de descarga de video para youtube-dl
def download_video(url):
	ydl_opts = {'format': 'bestaudio',
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320',
			}]
			}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

#TODO hacer funcion que mueva el archivo mp3 a la otra carpeta y luego manejarlo con una funcion del mismo main
#Puedo obtener los datos fácilmente desde youtube-dl con ydl.extract_info['title'] por ejemplo