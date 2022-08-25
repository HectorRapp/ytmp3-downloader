from __future__ import unicode_literals
import youtube_dl
import requests
import shutil

def download_video(url):
	ydl_opts = {'format': 'bestaudio',
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320',
			}],
			'ffmpeg_location':'ffmpeg-avconv/' 
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
		video_info = ydl.extract_info(url, False)
	title = video_info['title']
	author = video_info['uploader']
	thumbnail = fix_thumbnail(video_info['thumbnail'])
	id = video_info['id']
	base = f"{title}-{id}"
	video_data = {'title': title,
				  'author': author,
				  'thumbnail': thumbnail,
				  'path_base': base,
				  'path_ext': 'mp3'}
	return video_data

def fix_thumbnail(thumbnail):
	fixed_thumbnail = ""
	for i in thumbnail:
		if i == '?':
			break
		fixed_thumbnail+= i
	return fixed_thumbnail

def download_thumbnail(thumbnail):
	res = requests.get(thumbnail, stream = True)
	thumbnail_name = "cover.png"
	if res.status_code == 200:
		with open(thumbnail_name,'wb') as f:
			shutil.copyfileobj(res.raw, f)
	else:
		print('\n**Could not download thumbnail!**\n')
