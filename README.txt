#
# This is a system for collecting image files and videos and
#  displaying and managing them for use with Linux, Apple, and Microsoft.
#
# Use the following steps to implement the system.
#

#
# find all of the image files in the home directory
#
find_files.sh

#
# add the md5 hash for each file and link date names (2013/07/1277.png)
#  grep remove hidden directoies - e.g. .cache
#
python3 files_add_md5.py files_list.txt > files_tmp.txt
grep -v "/\." files_tmp.txt > files_md5_list.txt
rm files_tmp.txt

#
# sort the filename entries by the associated md5
#  hash for each
#
sort -t'|' -k1 files_md5_list.txt > s.txt
mv s.txt files_md5_list.txt

#
# check that all md5 coded files are equal (cmp) - and filter duplicates
#
python3 files_final_md5.py files_md5_list.txt > files_filtered_md5_list.txt

#
# sort by date filenames - oldest files first
#
sort -t'|' -k5 files_filtered_md5_list.txt > files_filenames_list.txt

#
# final pass on the filenames
#  add the repeat count: file(2).jpg
#
python3 files_final_filenames.py files_filenames_list.txt > files_final_list.txt

#
# list all of the date strings for directory names
#  assume the target new directory is "images"
#  create the directories under "images"
#
rm -rf images
python3 dirs_list.py images files_final_list.txt | sort | uniq > dirs_list.sh
sh dirs_list.sh

#
# list all of the file links (ln -s)
#  run the link script to add symbolic links to all files
#
python3 links_list.py images files_final_list.txt > links_list.sh
sh links_list.sh

#
# At this point one can use a file/directory browser on most any system
#  (linux, apple, windows) to step through and view the images and
#  videos.  Use "cp -L" copy the files, rather than links to the files.
#

#
# select files to be further processed
#  This creates the file "files_selected.sh"
#  files_selected.sh may be used again or verified with:
#
#    python3 files_select.py files_selected.sh
#
python3 files_select.py links_list.sh

#
# create mkdir lists and link lists for the selected files
#  the first argument is the new toplevel directory
#
#  edit "ln -s" to "cp -L" to copy the file rather than
#   creating a link
#
python3 proc_selected.py Ximages files_selected.sh > proc_selected.sh
