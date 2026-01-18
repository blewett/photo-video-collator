# photo-video-collator using python and tkinter
This is a system for collecting image and video files on Linux and displaying and managing them for use with Linux, Apple, and Microsoft.  It is common for people to have a large number of photos and videos that have accumulated on our computing systems over the years.

This system allows one to create USB flash drives of the collated photos and videos that may be shared, for example among family members.  The photos and  videos are arranged in directories by year and month.  As the USB drives may be formatted as NTFS these USB drives may be used on Linux, Apple, and Microsoft windows machines.  Each of those systems have native file browsers that can be used to browse through the collated images.

<img width="1151" height="861" alt="directory-browsing" src="https://github.com/user-attachments/assets/079540c9-0ca7-43da-b26b-a55bc60becf7" />

Files as are assigned to directories that match the year and month dates from the source image or video files.  Files are checked for duplication.  Duplicate files are eliminated with the oldest date being used for storing the file.

Files are placed in directories as symbolic links.  This results in small increments in disk space requirements.  Copies can be made of the directories and files by using copying applications such as "cp -L" on Linux machines.  These applications follow symbolic links to the source file.

This system is built in the software tools style of using small tools that do a specific task.  Other than Linux standard such as sort, the tools here are written in python.  There are three program files that are of general use for end users:

collate_photos.sh is a shell program that runs all of the smaller tasks which build and create the directories of photos and videos.  This program creates the directory of images that can be loaded on to flash drives and shared.  This may be the only program of interest for many users.  One step and done.

    collate_photos.sh

files_select.py is a python based browser that allows one to automatically scan, search, and select photos and videos for viewing.  This program is usually run with the links file as the only argument.

    python3 files_select.py links_list.sh

<img width="1106" height="853" alt="sample-files_select py" src="https://github.com/user-attachments/assets/801da5c4-c98c-4f11-bafe-f62c4f902fec" />

proc_selected.py is a python program that can be used to process the files selected by files_select.py.  This produces a shell script that can be used to create new directories of images and videos.

    python3 proc_selected.py files_selected.sh

I hope this helps.  You are on your own – but you already knew that.

Doug Blewett
doug.blewett@gmail.com
