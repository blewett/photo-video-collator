"""
dirs_list.py: Original work Copyright (C) 2026 by Blewett

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
# create year and month named directories list
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

        print("    " + sys.argv[0] + "  final_list_filename")

        exit(1)

    dest_dir = sys.argv[1]
    final_list_file = sys.argv[2]

    if not os.path.isfile(final_list_file):
        print("File not found: (" + final_list_file + ")")

    #
    # process the list records
    #
    list_record_duplicates_list = []

    with open(final_list_file, 'r') as list_file:

        record_count = 0

        for list_record in list_file:

            record_count += 1

            if list_record[0] == '#':
                # print(f"skipped: {list_record.strip()}")
                continue

            list_record = list_record.strip()
            list = list_record.split("|")

            if list[0] == '':
                print(f"BAD RECORD: record_count = {record_count}  list[0] = |{list[0]}| {list_record}")
                exit(1)

            date = list[1].split("-")
            print(f"mkdir -p {dest_dir}/{date[0]}/{date[1]}")
