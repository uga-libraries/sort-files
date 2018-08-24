# Sort Files

# Purpose
Do a first pass at appraising files obtained through a web crawl by sorting into folders based on keywords in the title and based on file extensions.

# Description
Python script that sorts files into folders to keep and don't keep based on keywords in the file title and based on the file extensions. Files are sorted into folders so that the user can verify the decisions before processing or deleting content.

The script was developed to work with the results of web crawls using the software HTTrack in order to obtain publications from those sites. Therefore, the script is based on the directory structure of HTTrack output:

    Parent Folder 
        Website_Name (folder)
            Website_Name (folder)
                images (folder)
                    files (these are the files to be sorted)
            hts-cache (folder)
                files
            cookies.txt
            hts-log.txt
     
The script creates folders "Keep" and "Don't Keep" within each images folder and then sorts the files within that images folder according to the rules.

# Usage
Download the script to your computer and give it permission so it is executable.

Run the script with the command:  python sort-files.py parentfolder

    Where parentfolder is the folder which contains all the folders with files you want to sort.
  
# Dependencies

Python 3

# Initial Author

Adriane Hanson, Head of Digital Stewardship, 2018.

# Acknowledgements

This script was developed and tested with the assistance of Sarah Causey, Map and Government Information Library.
