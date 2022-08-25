import moviepy.editor as mp 
from pytube import YouTube
import requests
import shutil
import os

def download_video(url):
	video = YouTube(url)
	title = video.title
	author = video.author
	thumbnail = video.thumbnail_url
	downloaded_file = video.streams.get_highest_resolution().download()
	base, ext = os.path.splitext(downloaded_file)
	video_data = {'title': title,
				  'author': author,
				  'thumbnail': thumbnail,
				  'video': downloaded_file,
				  'path_base': base,
				  'path_ext': ext}
	return video_data

def download_thumbnail(video_data):
	res = requests.get(video_data['thumbnail'],stream = True)
	thumbnail_name = "cover.png"
	if res.status_code == 200:
		with open(thumbnail_name,'wb') as f:
			shutil.copyfileobj(res.raw, f)
	else:
		print('\n**Could not download thumbnail!**\n')

def convert_video(video_data):
	print("Converting to mp3")
	clip = mp.VideoFileClip(video_data['video'])
	clip.audio.write_audiofile(video_data['path_base'] + ".mp3", bitrate="320k")
	clip.close()
	os.remove(video_data['video'])
	print("Converted!\n")
