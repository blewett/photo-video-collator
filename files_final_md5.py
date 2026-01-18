"""
files_final_md5.py: Original work Copyright (C) 2026 by Blewett

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
# run through the identified, md5 tagged, and sorted files.  Check
#  that duplicates are in fact duplicates using the linux cmp command.
#  Print out the working list of files.
#
import os
import sys
import subprocess
from datetime import datetime

global records_processed_md5_groups
records_processed_md5_groups = 0
global records_group
records_group = 0

def process_duplicates(record_count, duplicates_length, md5_record_duplicates_list):
    global records_processed_md5_groups
    global records_group

    i = 0
    while i < duplicates_length:
        md5i_record = md5_record_duplicates_list[i]
        md5i = md5i_record.split("|")

        i += 1
        j = i
        while j < duplicates_length:
            # print(f"compare {i - 1} {j}")
            md5j_record = md5_record_duplicates_list[j]
            md5j = md5j_record.split("|")
            j += 1

            cargs[0] = "cmp"
            cargs[1] = "-s"
            cargs[2] = md5i[3]
            cargs[3] = md5j[3]

            result = subprocess.run(cargs, capture_output=False, text=True)
            if result.returncode != 0:
                print(cargs)
                print(f"failed comparison: Return code: {result.returncode}")
                # print("Output:", result.stdout)
                print(f"record_count = {record_count}")
                print(cargs)
                exit(1)

if __name__ == "__main__":
    #
    # parse the command line arguments
    #
    argc = len(sys.argv)
    if argc != 2:
        print("  " + sys.argv[0] + ": the argument count should be 2.  You supplied " +
              str(argc))
        print("  " + sys.argv[0] + " arguments should be:")
        print("    " + sys.argv[0] + "  files_md5_sorted_data_filename")
        exit(1)

    md5_list_file = sys.argv[1]

    if not os.path.isfile(md5_list_file):
        print("File not found: (" + md5_list_file + ")")
        exit(1)

    #
    # process the md5 records
    #
    cargs = [""] * 4
    md5_record_duplicates_list = []

    with open(md5_list_file, 'r') as md5_file:

        record_count = 0
        md5_groups = 0
        current_md5 = ""
        first_pass = True

        for md5_record in md5_file:
            if md5_record[0] == '#':
                # print(f"skipped: {md5_record.strip()}")
                continue

            md5_record = md5_record.strip()
            md5 = md5_record.split("|")

            if md5[0] == '':
                print(f"BAD RECORD: record_count = {record_count}  md5[0] = |{md5[0]}| {md5_record}")
                exit(1)

            record_count += 1

            if first_pass:
                first_pass = False
                current_md5 = md5[0]
                md5_record_duplicates_list = []
                md5_record_duplicates_list.clear()
                md5_record_duplicates_list.append(md5_record)
                continue

            #
            # new group - switch current_md5
            #
            if current_md5 != md5[0]:
                current_md5 = md5[0]
                md5_groups += 1

                #
                # new group - sort the old group - print the oldest entry
                #
                duplicates_length = len(md5_record_duplicates_list)
                if duplicates_length > 1:
                    #
                    # sort the list in time order
                    #
                    md5_record_duplicates_list.sort(key=lambda s: datetime.strptime(s[33:43], '%Y-%m-%d'))
                    process_duplicates(record_count, duplicates_length, md5_record_duplicates_list)
                print(f"{md5_record_duplicates_list[0]}")

                #
                # clear / reset the group list
                #
                md5_record_duplicates_list = []
                md5_record_duplicates_list.clear()
                # drop through and add to the list

            #
            #  this not a single entry add it to the last
            #   from:
            #      current_md5 != md5[0]:
            #
            md5_record_duplicates_list.append(md5_record)

            #
            # continue reading
            #

    print(f"# record_count = {record_count}  md5_groups = {md5_groups}")
