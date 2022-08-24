from pytube import YouTube #pip install pytube3
import youtube_dl
import requests

def valid_url(url):
	example_urls = ['https://www.youtube.com/','https://youtu.be','www.youtube.com/','youtu.be/']
	for i in range(4):
		if example_urls[i] in url:
			return True 
	return False

def valid_video_pytube3(url):
	try:
		checker_url = "https://www.youtube.com/oembed?format=json&url="
		video_url = checker_url + url
		request = requests.get(video_url)
		return request.status_code == 200
	except:
		return False

def valid_video_youtube_dl(url):
	try:
		with youtube_dl.YoutubeDL() as ydl:
			result = ydl.extract_info(url, False)
		return True
	except:
		return False

