"""
proc_selected.py: Original work Copyright (C) 2026 by Blewett

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
#
# process selected files - create a single file with that performs
#  both dirs_list.sh and links_list.sh functions - creates directories
#  and copies the files into those directories.
#
# The input is a links_list.sh format file.  The input file can also be
#  the file produced by files_select.py.
#
import os
import sys
import subprocess
from datetime import datetime

if __name__ == "__main__":
    #
    # parse the command line arguments
    #
    argc = len(sys.argv)
    if argc != 3:
        print("  " + sys.argv[0] + ": the argument count should be 3.  You supplied " +
              str(argc))
        print("  " + sys.argv[0] + " arguments should be:")

        print("    " + sys.argv[0] + "  destination directory name")

        print("    " + sys.argv[0] + "  files selected sh file")

        exit(1)

    dest_dir = sys.argv[1]
    files_selected_file = sys.argv[2]

    if not os.path.isfile(files_selected_file):
        print("File not found: (" + files_selected_file + ")")

    #
    # process the selected records
    #
    cargs = [""] * 4
    selected_record_duplicates_list = []
    dir_dict = {}
    records_list = []

    with open(files_selected_file, 'r') as selected_file:

        record_count = 0

        for selected_record in selected_file:

            record_count += 1

            if selected_record[0] == '':
                print(f"BAD RECORD: record_count = {record_count}")
                exit(1)

            if selected_record[0] == '#':
                continue

            selected_record = selected_record.strip()
            selected_index = selected_record.rfind('" "')
            selected = selected_record[selected_index + 3: -1]
            selected_parts = selected.split("/")

            dir = dest_dir + "/" + selected_parts[1] + "/" + selected_parts[2]

            # enumerate and count the directory uses
            if dir in dir_dict:
                i = dir_dict[dir]
            else:
                i = 0
            dir_dict[dir] = i + 1

            record = selected_record[0:selected_index] + "\" \"" + dir + "/" + selected_parts[3] + "\""
            records_list.append(record)

    #
    # print out the directory creations and file links
    #
    for key in dir_dict:
        print(f"mkdir -p {key}")

    for record in records_list:
        print(f"{record}")
