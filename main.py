import connection_test as ct
from youtube_dl_option import youtube_dl as ydl
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
			print(f"holaaaaaaaaaa {ct.valid_video_pytube3(url)}")
		#test youtube-dl
		elif ct.valid_video_youtube_dl(url):
			service = "youtube-dl"
		else:
			print("\nThe link is invalid or the services are not available!\n")
	return url, service


def download_video(service,url):
	if service == "pytube3":
		pyt3.download_video(url)
	elif service == "youtube-dl":
		ydl.download_video(url)

#TODO crear funcion que se encargue de mover el archivo al directorio 

def __main__():
	# ----- Check Packages ----- # 
	import_packages.run_packages()
	url, service = insert_link()
	print(url)
	print(service)

	

if __main__:
	__main__()

