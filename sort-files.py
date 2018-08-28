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

errors = []                     # create list to hold error messages we encounter

if len(sys.argv) != 2:          # check for correct number of arguments
	if len(sys.argv) < 2:         # if none passed
		errors.append("Missing required argument of parent-folder.") # add to errors
	if len(sys.argv) > 2:         # if too many passed
		errors.append("Too many arguments.") # add to errors
else:                            # were passed one argument
  if not os.path.isdir(sys.argv[1]):   # ensure argument is directory
    errors.append(f"Folder to sort '{sys.argv[1]}' is not a directory.")

if len(errors) > 0:             # if we encountered errors
  for error in errors:          # print them
    print(error)
  print("""Usage: python3 sort-files.py parent_directory_to_process
       Ex: python3 sort-files.py my_directory
       Tells script to work on files in my_directory.""")
  exit()                        # exit

# List of keywords that indicate a file should be kept or not.
# Single words will also match partial words. Example: 'brochure' matches 'brochures'.
# Phrases have to match exactly. Example: 'fact sheet' does not match fact-sheet'.
keep = ['annual', 'brochure', 'fact sheet', 'fact-sheet', 'newsletter', 'report']
dont = ['agenda', 'code', 'form', 'law', 'letter', 'memoranda', 'minutes', 'press release', 'rules and regulations']

# Iterate over files
# os.walk will recurively giving you all the files and directories that are in the
# specified directory.
# it returns a tuple that has the root, which is the path to the file or directory,
# a list that holds the directories in that root,
# and a list of files in that root.
#
# for example, we'll take this structure
#
#  parent_dir
#   |--child_dir
#        |--childs_child_dir
#             |--file1
#        |--file2
#        |--file3
#   |--child_dir2
#        |--file4
#   |--file5
#
# for root, dirs, files in os.walk(parent_dir) will give us results like this (not complete):
#   root => parent_dir
#   dirs => [child_dir,child_dir2]
#   files => [file5]
#
#   root => parent_dir/child_dir
#   dirs => [childs_child_dir]
#   files => [file2,file3]
#
#   root => parent_dir/child_dir/childs_child_dir
#   dirs => []
#   files => [file1]

for root, dirs, files in os.walk(sys.argv[1]):
  for name in dirs:
    if name == 'images':              # if we've reached an images folder
      paths = [os.path.join(root,name,'Keep'), os.path.join(root,name,"Don't Keep")] # create paths for new directories
      for path in paths:              # for the two directories
        if not os.path.exists(path):  # if they don't exist
          os.makedirs(path)           # create them

  # only looking for files in the images folder, so we check to see if our root ends in images
  if root.endswith('images'):
    for name in files:
      filename = os.path.join(root,name)        # build full filename
      dont_path = os.path.join(root,"Don't Keep")    # build path to dont keep folder
      keep_path = os.path.join(root, "Keep")         # build path to keep folder
      lower_filename = name.lower()        # use lower case to ensure we match

      # if powerpoint
      if lower_filename.endswith('.ppt') or lower_filename.endswith('.pptx'):
        os.replace(filename,os.path.join(dont_path,name)) # move to dont keep

      # if name contains substring in keep list
      elif any(s in lower_filename for s in keep):
        os.replace(filename,os.path.join(keep_path,name))

      # if name contains substring in dont keep list
      elif any(s in lower_filename for s in dont):
        os.replace(filename,os.path.join(dont_path,name))

print("Script completed successfully.")
