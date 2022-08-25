import import_packages
import_packages.run_packages()

import os
import shutil
import subprocess

from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3

import connection_test as ct
import pytube3 as pyt3
import tools
import youtube_dl_opt as ydlo

# "DefaultDirectory" -> The songs will be saved in the program directory
# Or paste your directory to save them wherever you want
music_path = "DefaultDirectory"

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
		video_data = ydlo.download_video(url)
		ydlo.download_thumbnail(video_data['thumbnail'])
		return video_data
		
def edit_mp3(video_data):
	mp3_path = os.path.basename(f"{video_data['path_base']}.mp3")
	insert_cover(mp3_path)
	print("\nThe following parameters will be added to the .mp3 file")
	tools.print_metadata(video_data)
	response = ""
	options = ['y','n'] 
	title = video_data['title']
	author = video_data['author']
	while not response in options:
		response = input("\nDo you want to edit your mp3 file? [y/n]: ").lower()
	if(response == 'y'):
		title, author = tools.mp3_parameters(title, author)
		response = ""
	audio = EasyID3(mp3_path)
	audio['title'] = title
	audio['artist'] = author
	while not response in options:
		response = input("\nDo you want to add album? [y/n]: ").lower()
	if(response == 'y'):
		audio['album'] = input("Enter the album of song: ")
	audio.save()
	print("File edited successfully!")

def insert_cover(mp3_path):
	audio = ID3(mp3_path)
	with open('cover.png', 'rb') as albumart:
		audio['APIC'] = APIC(mime = 'cover.png', type = 3, desc = u"Cover", data = albumart.read())
	audio.save()
	os.remove('cover.png')

def move_file(dest_path, video_data):
	src = video_data['path_base'] + ".mp3"
	shutil.move(src, dest_path)
	explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
	subprocess.run([explorer_path, dest_path])


def find_directory():
	dest = music_path
	only_directories = [ name for name in os.listdir(dest) if os.path.isdir(os.path.join(dest, name)) ]
	input_artist = tools.input_artist_or_folder()
	directory_path = tools.find_path(input_artist, dest, only_directories)
	if directory_path == "":  directory_path = tools.create_directory(input_artist,dest)
	return directory_path

def main():
	url, service = insert_link()
	video_data = download_video(service,url)
	edit_mp3(video_data)
	if music_path != "DefaultDirectory":
		dest_path = find_directory()
		print(dest_path)
		move_file(dest_path,video_data)
	if music_path == "DefaultDirectory": print("The file was downloaded to the local directory!")
	else: print(f"The file was downloaded to the directory: {dest_path}")

music_path = tools.run(music_path)
main()
