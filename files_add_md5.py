"""
files_add_md5.py: Original work Copyright (C) 2026 by Blewett

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
# add md5 hash and date to a list of file names
#
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

def md5sum(filename, chunk_size=8192):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()

def file_date(filename):
    timestamp = os.path.getmtime(filename)
    d = str(datetime.fromtimestamp(timestamp))
    d = d.replace(" ", "|")
    return d

if __name__ == "__main__":

    #
    # parse the command line arguments to define the file names
    #
    argc = len(sys.argv)
    if argc != 2:
        print("  " + sys.argv[0] + ": the argument count should be 2.  You supplied " +
              str(argc))
        print("  " + sys.argv[0] + " arguments should be:")
        print("    " + sys.argv[0] + " files_md5_list_filename files_list_filename")
        exit(1)

    list_file = sys.argv[1]

    if not os.path.isfile(list_file):
        print("File not found: (" + list_file + ")")
        exit(1)

    home_dir = str(Path.home())

    with open(list_file, 'r') as file:
        for fx in file:

            if fx[0] == '#':
                # print(f"skipped: {fx.strip()}")
                continue

            if fx[0] == '.' and fx[1] == '/':
                fx = fx[2:]

            filename = home_dir + "/" + fx.strip()

            if not os.path.isfile(filename):
                print("File not found: (" + filename + ")")
            else:
                date_bits = file_date(filename).split("-")
                # print(f"{date_bits[0]}/{date_bits[1]}")
                file_bits = filename.split("/")
                length = len(file_bits)
                print(f"{md5sum(filename)}|{file_date(filename)}|{filename}|{date_bits[0]}/{date_bits[1]}/{file_bits[length - 1]}")
