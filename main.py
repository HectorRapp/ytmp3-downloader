import connection_test as ct
# from youtube_dl_option import youtube_dl_opt as ydl
import import_packages
import pytube3 as pyt3
import moviepy.editor as mp #pip install moviepy
import subprocess
import requests
import shutil
import os
import re


def insert_link():
	service = False
	while not service:
		url = ""
		while not ct.valid_url(url):
			url = str(input("Enter the link video: "))
		#test pytube3
		if(ct.valid_video_pytube3(url)):
			service = "pytube3"
			print("Downloading via pytube3")
		#test youtube-dl
		elif ct.valid_video_youtube_dl(url):
			service = "youtube-dl"
			print("Downloading via youtube-dl")
		else:
			print("\nThe link is invalid or the services are not available!\n")
	return url, service


def download_video(service,url):
	if service == "pytube3":
		video_data = pyt3.download_video(url)
		pyt3.download_thumbnail(video_data)
		pyt3.convert_video(video_data)
		return video_data
	elif service == "youtube-dl":
		return ydl.download_video(url)

#TODO crear funcion que se encargue de mover el archivo al directorio 

def run():
	# ----- Check Packages ----- # 
	import_packages.run_packages()
	url, service = insert_link()
	service = "youtube-dl"
	video_data = download_video(service,url)
	print(video_data['thumbnail'])
	

run()


#TODO ver si hago una función que recorte la canción