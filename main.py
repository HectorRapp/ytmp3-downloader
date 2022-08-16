from pytube import YouTube #pip install pytube3
import moviepy.editor as mp #pip install moviepy
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

# ---------- The video is converted to mp3 - 320kbps and deleted ---------- #
print("Converting to mp3")
clip = mp.VideoFileClip(downloaded_file)
clip.audio.write_audiofile(base + ".mp3", bitrate="320k")
clip.close()
os.remove(downloaded_file)
print("Converted!\n")


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

# ---------- Thumbnail download ---------- #
res = requests.get(thumbnail,stream = True)
thumbnail_name = "cover.png"
if res.status_code == 200:
    with open(thumbnail_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
else:
    print('\n**Could not download thumbnail!**\n')

#We move the thumbnail
shutil.move("cover.png", dest)

# ---------- Move the mp3 and open the new directory ---------- #
shutil.move(src, dest)
explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
subprocess.run([explorer_path, dest])
#Optional (TagScanner is used to modify the data of an mp3 )
# subprocess.Popen("C:\Program Files\TagScanner\Tagscan.exe")








