import importlib.util 
import subprocess
import sys

def check_packages():
	print("Checking for missing packages...")
	package_to_install = []
	package_list = ['pytube',
					'youtube_dl',
					'moviepy',
					'mutagen',
					'unicodedata',
					'subprocess',
					'requests',
					'shutil',
					'os',
					're']
	for i in package_list:
		is_present = importlib.util.find_spec(i) #find_spec will look for the package
		if is_present is None:
			package_to_install.append(i)
	return package_to_install

def install_packages(packages):
	print("Installing...")
	for i in packages:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])

def run_packages():
	left_packages = check_packages() 
	if len(left_packages) != 0:
		install_packages(left_packages)
	print("All packages are installed!\n")

