from __future__ import unicode_literals
import youtube_dl
import ffmpeg

#TODO hacer la funcion de descarga de video para youtube-dl
def download_video(url):
	ydl_opts = {'format': 'bestaudio',
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320',
			}],
	        # 'outtmpl': 'youtube_dl_option/%(title)s.%(ext)s'

	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		video = ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])
		# video_info = ydl.extract_info('https://www.youtube.com/watch?v=BaW_jenozKc')
	video_data = {'video_file': video,
				  'video_info': 'video_info'}
	return video_data

#FIXME el video se va a la carpeta principal, cuando debería irse a la carpeta donde está el .py
video_data = download_video('https://www.youtube.com/watch?v=4ZEpw6nmNvs')

#TODO hacer funcion que mueva el archivo mp3 a la otra carpeta y luego manejarlo con una funcion del mismo main
#Puedo obtener los datos fácilmente desde youtube-dl con ydl.extract_info['title'] por ejemplo