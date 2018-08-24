#Purpose: Sort files in a directory into folders based on the file name or extension. 

#Expected directory structure (from web crawl using HTTrack):
	#ParentFolder
		#AgencyFolder - there are many folders with this same directory structure in Parent Folder 
			#AgencyFolder - repeats the name of its parent
				#images
					#files - these are the files we want to sort
			#hts-cache
				#files
			#cookies.txt
			#hts-log.txt

#Usage: python sort-files.py parent-folder

import os
import sys

#1. Test arguments: are there the right number and is the file path supplied a valid directory.
#If there is an error, a message displays on how to fix the error and the scrip quits.

if len(sys.argv) != 2:
	if len(sys.argv) < 2:
		print("Missing required argument. To run this script, put this into the terminal: python sort-files.py parentfolder")
	if len(sys.argv) > 2:
		print("Too many arguments. To run this script, put this into the terminal: python sort-files.py parentfolder")
	sys.exit()
	
if not os.path.isdir(sys.argv[1]):
	print(f"Folder to sort '{sys.argv[1]}' is not a directory.")
	sys.exit()

#2. Change current directory to the ParentFolder
os.chdir(sys.argv[1])

#3. List of keywords that indicate a file should be kept or not. 
#Single words will also match partial words. Example: 'brochure' matches 'brochures'.
#Phrases have to match exactly. Example: 'fact sheet' does not match fact-sheet'.
keep = ['annual', 'brochure', 'fact sheet', 'fact-sheet', 'newsletter', 'report']
dont = ['agenda', 'code', 'form', 'law', 'letter', 'memoranda', 'minutes', 'press release', 'rules and regulations']

#4. Navigate to each images folder.

for dir in os.listdir():
	#gets to the agency folders
	if os.path.isdir(dir):
		os.chdir(dir)
		
		#gets to the subfolders within the agency folders
		for subdir in os.listdir():
			if os.path.isdir(subdir):
				os.chdir(subdir)
			
				#get to the subfolders within the subfolders that are named images
				for subsubdir in os.listdir():
					if os.path.isdir(subsubdir) and subsubdir == 'images':
						os.chdir(subsubdir)
						
						#5. Make Keep and Don't Keep subfolders in the images folder
						if not os.path.exists("Keep"):
							os.mkdir("Keep")

						if not os.path.exists("Don't Keep"):
							os.mkdir("Don't Keep")
	
						#6. Get a list of file names in the images folder
						files = os.listdir()
						
						#7. Sorts those files based on the keyword lists and file extensions.
						#The rules are applied in order.
						#Files are sorted based on the first rule they match.
						#If a file does not match any rules, it will not be moved.
						for filename in files:

							if filename == 'Keep' or filename == 'Don\'t Keep':
								continue
	
							lower_filename = filename.lower()
	
							if lower_filename.endswith('.ppt') or lower_filename.endswith('.pptx'):
								os.replace(filename,f'Don\'t Keep/{filename}')

							elif any(s in lower_filename for s in keep):
								os.replace(filename,f'Keep/{filename}')
		    
							elif any(s in lower_filename for s in dont):
								os.replace(filename,f'Don\'t Keep/{filename}')
						
						os.chdir('..')
					
				os.chdir('..')
	
		os.chdir('..')
		
print("Script is complete.")