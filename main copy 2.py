from pytube import YouTube #pip install pytube3
import moviepy.editor as mp #pip install moviepy
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from unicodedata import normalize
import subprocess
import requests
import shutil
import os
import re

def clean_string(directory):
	string = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", directory), 0, re.I)
	return string

#Spotify offline music directory
music_path = "YourDirectory"



# ---------- MP3 Edit ---------- #
mp3_route = os.path.basename(f"{base}.mp3")
response = ['y','n']
edit = ""
edit2 = ""
while not edit in response:
	edit = input("Do you want to edit your mp3 file? [y/n]: ")

if(edit.lower() == 'y'):
	print("\nThe data obtained from the video are: ")
	print(f"Title: {yt_title}")
	print(f"Author: {yt_author}")
	while not edit2 in response:
		edit2 = input("Do you want to change any? [y/n]: ")
	if(edit2 == 'y'):
		print("\nLeave empty if you don't want to modify")
		title = input("Enter the title of song: ")
		author = input("Enter the author of song: ")
		if (title != ""):
			yt_title = title
		if(author != ""):
			yt_author = author
	audio = ID3(mp3_route)
	with open(thumbnail_name, 'rb') as albumart:
		audio['APIC'] = APIC(mime = thumbnail_name, type = 3, 
							desc = u"Cover", data = albumart.read())
	audio.save()
	audio = EasyID3(mp3_route)
	audio['title'] = yt_title
	audio['artist'] = yt_author
	audio.save()

# ---------- We look for the directory ---------- #
src = base + ".mp3"
dest = music_path
ls = os.listdir(dest)
only_directories = [ name for name in os.listdir(dest) if os.path.isdir(os.path.join(dest, name)) ]
artist = ""
while artist == "":
	artist = str(input("Enter the name of artist or directory: "))
artist_path = ""
for i in only_directories:
	directory = clean_string(i)
	if artist.lower() in directory.lower():
		artist_path = (f"{dest}\{i}")
		break
#if it does not exist, it is created
if artist_path == "":
	artist_path = (f"{dest}\{artist.capitalize()}")
	os.mkdir(artist_path)
	print("Created a new directory")
dest = artist_path



# ---------- Move files and open the new directory ---------- #
if edit.lower() == "n":
	#We move the thumbnail
	shutil.move("cover.png", dest)
else:
	os.remove(thumbnail_name)

shutil.move(src, dest)
explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
subprocess.run([explorer_path, dest])








