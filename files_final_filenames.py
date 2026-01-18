"""
files_final_filenames.py: Original work Copyright (C) 2026 by Blewett

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

def process_duplicates(record_count, duplicates_length, final_record_duplicates_list):
    global records_processed_final_groups
    global records_group

    #
    # add the collision number (N) is added to all but the first record
    #
    i = 1
    while i < duplicates_length:
        final_indexed_record = final_record_duplicates_list[i]
        final_indexed = final_indexed_record.split("|")
        final_indexed_length = len(final_indexed)

        name = final_indexed[final_indexed_length - 1]
        dot = name.rfind(".")
        name_numbered = name[0:dot] + "(" + str(i) + ")" + name[dot:]
        final_indexed[final_indexed_length - 1] = name_numbered

        composite = final_indexed[0]
        j = 1
        while j < final_indexed_length:
            composite = composite + "|" + final_indexed[j]
            j  += 1
        final_record_duplicates_list[i] = composite
        i += 1

if __name__ == "__main__":
    #
    # parse the command line arguments
    #
    argc = len(sys.argv)
    if argc != 2:
        print("  " + sys.argv[0] + ": the argument count should be 2.  You supplied " +
              str(argc))
        print("  " + sys.argv[0] + " arguments should be:")
        print("    " + sys.argv[0] + "  files_final_sorted_data_filename")
        exit(1)

    final_list_file = sys.argv[1]

    if not os.path.isfile(final_list_file):
        print("File not found: (" + final_list_file + ")")
        exit(1)

    #
    # process the final records
    #
    cargs = [""] * 4
    final_record_duplicates_list = []

    with open(final_list_file, 'r') as final_file:

        record_count = 0
        final_groups = 0
        current_final = ""
        first_pass = True

        for final_record in final_file:
            if final_record[0] == '#':
                # print(f"skipped: {final_record.strip()}")
                continue

            final_record = final_record.strip()
            final = final_record.split("|")

            if final[0] == '':
                print(f"BAD RECORD: record_count = {record_count}  final[0] = |{final[0]}| {final_record}")
                exit(1)

            record_count += 1

            if first_pass:
                first_pass = False
                current_final = final[4]
                final_record_duplicates_list = []
                final_record_duplicates_list.clear()
                final_record_duplicates_list.append(final_record)
                continue

            #
            # new group - switch current_final
            #
            if current_final != final[4]:
                current_final = final[4]
                final_groups += 1

                #
                # new group - sort the old group - print the oldest entry
                #
                duplicates_length = len(final_record_duplicates_list)
                if duplicates_length > 1:
                    process_duplicates(record_count, duplicates_length, final_record_duplicates_list)
                i = 0
                while i < duplicates_length:
                    # print(f"{i} {duplicates_length}: {final_record_duplicates_list[i]}")
                    print(f"{final_record_duplicates_list[i]}")
                    i += 1

                #
                # clear / reset the group list
                #
                final_record_duplicates_list = []
                final_record_duplicates_list.clear()
                # drop through and add to the list

            #
            #  this not a single entry add it to the last
            #   from:
            #      current_final != final[0]:
            #
            final_record_duplicates_list.append(final_record)

            #
            # continue reading
            #

    print(f"# record_count = {record_count}  final_groups = {final_groups}")
