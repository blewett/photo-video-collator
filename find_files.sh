#
# This is a system for collecting image filenames and video
#  filenames for further processing.  "-type f" does not follow
#  symbolic links.  grep -v removes files from "hidden" directories.
#
dir=`pwd`
cd
find -P . \
     -type f -name "*.jpg" -o \
     -type f -name "*.JPG" -o \
     -type f -name "*.jpeg" -o \
     -type f -name "*.JPEG" -o \
     -type f -name "*.png" -o \
     -type f -name "*.PNG" -o \
     -type f -name "*.mov" -o \
     -type f -name "*.MOV" -o \
     -type f -name "*.mp4" -o \
     -type f -name "*.MP4" | grep -v "/\." > /tmp/files_list.txt 2>/dev/null

#  grep remove hidden directoies - e.g. .cache

cd $dir
mv /tmp/files_list.txt .
ls -l files_list.txt
wc -l files_list.txt
