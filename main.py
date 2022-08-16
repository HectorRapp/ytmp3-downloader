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

def valid_url(url):
	key_words  = ["youtu.be","youtube"]
	for i in range(2):
		if key_words[i] in url:
			return True
	return False

#Spotify offline music directory
music_path = "YourDirectory"

# ---------- Video Download ---------- #
success = False
while not success:
	success = True
	try:
		url = str(input("Enter the link video: "))
		video = YouTube(url).streams.filter(res="720p").first()
		thumbnail = YouTube(url).thumbnail_url
		downloaded_file = video.download()
		base, ext = os.path.splitext(downloaded_file)
		print("Downloaded!\n")
	except:
		print("\n**An error occurred!**\n")
		success = False

# ---------- Thumbnail download ---------- #
res = requests.get(thumbnail,stream = True)
thumbnail_name = "cover.png"
if res.status_code == 200:
    with open(thumbnail_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
else:
    print('\n**Could not download thumbnail!**\n')

# ---------- The video is converted to mp3 - 320kbps and deleted ---------- #
print("Converting to mp3")
clip = mp.VideoFileClip(downloaded_file)
clip.audio.write_audiofile(base + ".mp3", bitrate="320k")
clip.close()
os.remove(downloaded_file)
print("Converted!\n")

# ---------- MP3 Edit ---------- #
mp3_route = os.path.basename(f"{base}.mp3")
edit = ""
while not (edit =="s" or edit =="n"):
	edit = input("Do you want to edit your mp3 file? [s/n]: ")

if(edit.lower() == "s"):
	audio = ID3(mp3_route)
	with open(thumbnail_name, 'rb') as albumart:
		audio['APIC'] = APIC(mime = thumbnail_name, type = 3, 
							desc = u"Cover", data = albumart.read())
	audio.save()
	title = input("Enter the title of song: ")
	author = input("Enter the author of song: ")
	audio = EasyID3(mp3_route)
	audio['title'] = title
	audio['artist'] = author
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








