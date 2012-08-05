#!/usr/bin/python2.7

import os
import sys

NAME='set-mp3-artist'

def main():
	global ROOT
	
	if len(sys.argv) != 2:
		print 'Invalid usage'
		print NAME, '<path of the music directory>'
		sys.exit(1)
	
	ROOT=sys.argv[1]

	get_file_list()
	set_data()
	
def get_file_list():

	global file_list
	file_list=[]

	for path, dirs, files in os.walk(ROOT):
		for fi in files:
			abs_path = os.path.join(path, fi)
			if abs_path.lower().endswith('.mp3'):
				file_list.append(abs_path)

def set_data():
	pre_artist=''
	pre_album=''

	for fi in file_list:
		data = get_artist_album(fi)

		if data is not None:
			if data[0] != pre_artist:
				print data[0]
				pre_artist = data[0]
			cmd_artist = 'id3tag -a"' + data[0] + '" "' + fi + '"'
			os.system(cmd_artist)

			if data[1] is not None:
				cmd_album = 'id3tag -A"' + data[1] + '" "' + fi + '"'
				os.system(cmd_album)

def get_artist_album(fi):
	temp = (fi[len(ROOT):]).split(os.sep)

	# artist and album	
	if len(temp) > 2:
		return [temp[0], temp[1]]
	
	# artist only
	if len(temp) > 1:
		return [temp[0], None]

	# top level files
	return None

if __name__ == '__main__':
	main()
