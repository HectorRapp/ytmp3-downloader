
from unicodedata import normalize
import re
import os

def run(path):
	if path == "DefaultDirectory": 
		print("\n*The songs will be saved in the program directory*\n")
	elif valid_path(path): 
		print(f"\n*The songs will be saved in the path: {path}*\n")
	elif not valid_path(path):
		print("\nInvalid directory, the songs will be saved in the default location!")
		path = "DefaultDirectory"
	return path

def valid_path(path):
	if path != "":
		characters = ['/','\\']
		for i in path:
			if i in characters:
				return True
	return False

def print_metadata(video):
	print(f"title: {video['title']}")
	print(f"author: {video['author']}")

def mp3_parameters(title, author):
	print("\nLeave empty if you don't want to modify")
	title_ = input("Enter the title of song: ")
	author_ = input("Enter the author of song: ")
	if (title_ != ""):
		title = title_
	if(author_ != ""):
		author = author_
	return title, author

def input_artist_or_folder():
	artist_directory = ""
	while artist_directory == "":
		artist_directory = str(input("Enter the name of artist or directory: "))
	return artist_directory
	
def find_path(directory_path, dest, directories):
	artist_path = ""
	for i in directories:

		directory = clean_string(i)
		if directory_path.lower() in directory.lower():
			artist_path = (f"{dest}\{i}")
			break
	return artist_path

def create_directory(input_artist, dest):
	artist_path = (f"{dest}\{input_artist.capitalize()}")
	os.mkdir(artist_path)
	print("Created a new directory")
	return artist_path

def clean_string(directory):
	string = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", directory), 0, re.I)
	return string

