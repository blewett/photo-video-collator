"""
files_select.py: Original work Copyright (C) 2026 by Blewett

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

This is a simple image viewing and selecting program.

The program can display jpegs, pngs and video files, mp4 and mov.

Load cv2:
 pip3 install opencv-python

Load tkinter:
 apt-get install python3-tk

Load Pillow:
 pip3 install --upgrade Pillow

and other words like that.
"""
import os
import sys
from tkinter import *
import tkinter as tk
from PIL import ImageTk
from PIL import Image
import cv2
import time
import shutil

OUTPUT_FILE = "files_selected.sh"
DISPLAY_TIME_MS = 2000  # 2.0 seconds
FRAMES_PER_SECOND = 20 # a guess on videos large and small
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 764
IMAGE_BOX_SIZE = 512

# assume strip()'ed line
def display_file(line):
    file_index = line.rfind('" "')
    file_name = line[file_index+3:-1]
    return file_name

def short_display_file(line):
    file_index = line.rfind('/')
    file_name = line[file_index+1:-1]
    return file_name

def display_file_year_month(file_name):
    file_name_parts = file_name.split("/")
    year = int(file_name_parts[1])
    month = int(file_name_parts[2])
    return year, month

class ImageViewer:
    def __init__(self, root, list_file, 
                 year_start, month_start,
                 year_end, month_end):

        year_start = int(year_start)
        month_start = int(month_start)
        year_end = int(year_end)
        month_end = int(month_end)

        self.file_year_start_int = year_start
        self.file_month_start_int = month_start
        self.file_year_end_int = year_end
        self.file_month_end_int = month_end

        self.year_start_int = year_start
        self.month_start_int = month_start
        self.year_end_int = year_end
        self.month_end_int = month_end
        self.search_string = None

        self.root = root
        self.root.title("Image Selector")

        #
        # create the tkinter interface
        #

        # Fixed window size
        #self.root.geometry(f"{60 + WINDOW_WIDTH * 2}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.grid_propagate(True)

        # top level frame
        self.top_frame = tk.Frame(
            root,
            width=40 + IMAGE_BOX_SIZE * 2 ,
            height=20 + IMAGE_BOX_SIZE
        )
        self.top_frame.grid(row=0, column=0, padx=10, pady=10)
        self.top_frame.grid_propagate(True)

        # Fixed image frame left
        self.image_frame_left = tk.Frame(
            self.top_frame,
            width=IMAGE_BOX_SIZE,
            height=IMAGE_BOX_SIZE,
            borderwidth=5, relief="ridge",
            bg="black"
        )
        self.image_frame_left.grid(row=0, column=0, padx=5, pady=10)

        # label_left for images
        self.label_left = tk.Label(self.image_frame_left, bg="black")
        self.label_left.place(relx=0.5, rely=0.5, anchor="center")

        # Fixed image frame right
        self.image_frame_right = tk.Frame(
            self.top_frame,
            width=IMAGE_BOX_SIZE,
            height=IMAGE_BOX_SIZE,
            borderwidth=5, relief="ridge",
            bg="black"
        )
        self.image_frame_right.grid(row=0, column=2, padx=5, pady=10)

        # label_right for images
        self.label_right = tk.Label(self.image_frame_right, bg="black")
        self.label_right.place(relx=0.5, rely=0.5, anchor="center")

        # controls frame left
        self.controls_left_frame = tk.Frame(self.top_frame)
        self.controls_left_frame.grid(row=1, column=0, padx=0, pady=10)

        # file_name_label_left
        self.file_name_label_left = tk.Label(self.controls_left_frame, text="[ running ]")
        self.file_name_label_left.grid(row=0, column=0, padx=0, pady=0)

        # button frame left
        self.button_frame_left = tk.Frame(self.controls_left_frame)
        self.button_frame_left.grid(row=1, column=0, padx=10, pady=10)

        # pause button
        self.pause_button = tk.Button(
            self.button_frame_left,
            text="Run",
            width=15,
            command=self.pause_filename
        )
        self.pause_button.grid(row=0, column=0, padx=10, pady=10)

        # back button
        self.back_button = tk.Button(
            self.button_frame_left,
            text="Back",
            width=15,
            command=self.back_filename
        )
        self.back_button.grid(row=0, column=1, padx=10, pady=10)

        # forward button
        self.forward_button = tk.Button(
            self.button_frame_left,
            text="Forward",
            width=15,
            command=self.forward_filename
        )
        self.forward_button.grid(row=0, column=2, padx=10, pady=10)

        # range frame
        self.range_frame = tk.Frame(self.button_frame_left)
        self.range_frame.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        tk.Label(self.button_frame_left, text="search dates: ").grid(row=2, column=0, padx=0, pady=0, sticky="e")

        index = 0
        self.year_start_var = tk.StringVar(value=year_start)
        self.year_start = tk.Entry(self.range_frame, width=4,
                                   textvariable=self.year_start_var)
        self.year_start.grid(row=2, column=index, padx=0, pady=0)

        index += 1
        tk.Label(self.range_frame, text="/").grid(row=2, column=index, padx=0, pady=0)

        index += 1
        self.month_start_var = tk.StringVar(value=month_start)
        self.month_start = tk.Entry(self.range_frame, width=2,
                                   textvariable=self.month_start_var)
        self.month_start.grid(row=2, column=index, padx=0, pady=0, sticky="e")

        index += 1
        tk.Label(self.range_frame, text=" ").grid(row=2, column=index, padx=0, pady=0)

        index += 1
        self.year_end_var = tk.StringVar(value=year_end)
        self.year_end = tk.Entry(self.range_frame, width=4,
                                 textvariable=self.year_end_var)
        self.year_end.grid(row=2, column=index, padx=0, pady=0)

        index += 1
        tk.Label(self.range_frame, text="/").grid(row=2, column=index, padx=0, pady=0)

        index += 1
        self.month_end_var = tk.StringVar(value=month_end)
        self.month_end = tk.Entry(self.range_frame, width=2,
                                  textvariable=self.month_end_var)
        self.month_end.grid(row=2, column=index, padx=0, pady=0)

        tk.Label(self.button_frame_left, text="search string: ").grid(row=3, column=0, padx=0, pady=0, sticky="e")

        self.search_string_var = tk.StringVar(value=" ")
        self.search_string = tk.Entry(self.button_frame_left,
                                      textvariable=self.search_string_var)
        self.search_string.grid(row=3, column=1, sticky="we")

        # search button
        self.search_button = tk.Button(
            self.button_frame_left,
            text="Search",
            width=15,
            command=self.search
        )
        self.search_button.grid(row=4, column=1, padx=10, pady=10)

        self.error_search_var = tk.StringVar(value="[ search status ]")
        self.error_search_field = tk.Entry(self.button_frame_left,
                                           textvariable=self.error_search_var)
        self.error_search_field.grid(row=4, column=2, padx=5, pady=0, sticky="ew")

        # controls frame right
        self.controls_right_frame = tk.Frame(self.top_frame)
        self.controls_right_frame.grid(row=1, column=2, padx=0, pady=10)

        # button frame right
        self.button_frame_right = tk.Frame(self.controls_right_frame)
        self.button_frame_right.grid(row=0, column=0, padx=10, pady=0)

        # view button
        self.view_button = tk.Button(
            self.button_frame_right,
            text="View",
            width=15,
            command=self.view_filename
        )
        self.view_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # copy file to directory
        tk.Label(self.button_frame_right, text="Directory: ").grid(row=1, column=0, padx=0, pady=0, sticky="e")
        self.dir_name_var = tk.StringVar(value="/tmp")
        self.dir_name = tk.Entry(self.button_frame_right,
                                 textvariable=self.dir_name_var)
        self.dir_name.grid(row=1, column=1, sticky="we")
        self.copy_file = tk.IntVar(value=0)
        self.checkbox_copy_file = tk.Checkbutton(self.button_frame_right,
                                                 text="Copy the file:",
                                                 width=15,
                                                 variable=self.copy_file)
        self.checkbox_copy_file.grid(row=1, column=2, padx=10, pady=10)

        # append filename to file
        tk.Label(self.button_frame_right, text="List file: ").grid(row=2, column=0, padx=0, pady=0, sticky="e")
        self.file_name_var = tk.StringVar(value="selected.sh")
        self.file_name = tk.Entry(self.button_frame_right,
                                 textvariable=self.file_name_var)
        self.file_name.grid(row=2, column=1, sticky="we")
        self.append_list_file = tk.IntVar(value=0)
        self.checkbox_append_list_file = tk.Checkbutton(self.button_frame_right,
                                                         text="Append name:",
                                                         width=15,
                                                         variable=self.append_list_file)
        self.checkbox_append_list_file.grid(row=2, column=2, padx=10, pady=10)

        # write button
        self.write_button = tk.Button(
            self.button_frame_right,
            text="Write",
            width=15,
            command=self.write_filename
        )
        self.write_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.error_write_var = tk.StringVar(value="[ write status ]")
        self.error_write_field = tk.Entry(self.button_frame_right,
                                          textvariable=self.error_write_var)
        self.error_write_field.grid(row=3, column=2, padx=5, pady=0, sticky="ew")

        #
        # Load image list
        #
        self.Load_image_list()
        self.error_search_var.set(f"{len(self.image_files)} images")
        self.record_index = 0
        self.current_image_path = None
        self.view_image_path = None
        self.photo = None
        self.photo_left = None
        self.photo_right = None
        self.pause = True
        self.cycle_images()

    #
    # function for displaying one image
    #
    def show_image(self, image_path, display_label):
        if not self.image_files:
            return

        image_filename = display_file(image_path)

        try:
            image = Image.open(image_filename)
            image.thumbnail((IMAGE_BOX_SIZE, IMAGE_BOX_SIZE))
            self.photo = ImageTk.PhotoImage(image)

            # total crap caused by garbage collecting ImageTk
            if display_label == self.label_right:
                self.photo_right = self.photo
            else:
                self.photo_left = self.photo

            display_label.config(image=self.photo)

        except Exception as e:
            root.title(f"Error loading {image_filename}: {e}")

    #
    # Load image list
    #
    def Load_image_list(self):
        search_string = self.search_string_var.get()

        files = []
        match = False
        with open(list_file, "r") as f:
            for line in f:
                line = line.strip()
                file_name = display_file(line)
                year, month = display_file_year_month(file_name)
                year = int(year)
                month = int(month)

                if search_string != None and line.find(search_string) == -1:
                    continue

                if year < int(self.year_start_int):
                    continue
                if year == int(self.year_start_int) and month < int(self.month_start_int):
                    continue

                if year > int(self.year_end_int):
                    break
                if year == int(self.year_end_int) and month > int(self.month_end_int):
                    break

                files.append(line)
                match = True

        if match == True:
            self.image_files = []
            self.image_files = files
            self.record_index = 0

        return match
    #
    # function for displaying a video stream
    #
    def show_video(self, image_path, display_label):

        video_filename = display_file(image_path)
        cap = cv2.VideoCapture(video_filename)

        if not cap.isOpened():
            root.title(f"Could not open {video_filename}")
            return DISPLAY_TIME_MS

        start_time = time.time()

        video_filename = display_file(image_path)

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                break  # End of video or read error

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            display_label.imgtk = imgtk
            display_label.configure(image=imgtk)

            self.top_frame.update_idletasks()

            #
            # frames to display
            #
            frame_count += 1
            if frame_count > (DISPLAY_TIME_MS / FRAMES_PER_SECOND):
                cap.release()
                break

            #
            # Exit after DISPLAY_TIME_MS seconds
            #
            if time.time() - start_time >= (DISPLAY_TIME_MS / 1000):
                cap.release()
                break

        rt = round((time.time() - start_time) * 1000)
        return rt

    # in cycle
    def move_to_next_image(self, delay):
        self.record_index = (self.record_index + 1) % len(self.image_files)
        self.root.after(delay, self.cycle_images)

    # in back - self.record_index has been updated prior to this call
    def move_to_previous_image(self):
        length = len(self.image_files)
        if self.record_index == 0:
            self.record_index = length - 1
        else:
            self.record_index -= 1

        self.current_image_path = self.image_files[self.record_index]
        root.title(f"{self.record_index + 1}. {short_display_file(self.current_image_path)}")
        tr = self.show_entry(self.current_image_path, self.label_left, self.file_name_label_left)


    def show_entry(self, image_path, display_label, file_name_label):
        image_filename = display_file(image_path)
        if file_name_label != None:
            file_name_label.config(text = image_filename)

        type_image = image_filename[image_filename.rfind("."):]
        time_remaining = DISPLAY_TIME_MS
        if (type_image == ".mov" or type_image == ".MOV" or
            type_image == ".mp4" or type_image == ".MP4"):

            rt = self.show_video(image_path, display_label)
            time_remaining = DISPLAY_TIME_MS -rt
            if time_remaining < 0:
                time_remaining = FRAMES_PER_SECOND
        else:
            self.show_image(image_path, display_label)

        return time_remaining

    def cycle_images(self):
        if not self.image_files:
            return

        self.current_image_path = self.image_files[self.record_index]
        root.title(f"{self.record_index + 1}. {short_display_file(self.current_image_path)}")
        time_remaining = self.show_entry(self.current_image_path, self.label_left, self.file_name_label_left)
        if self.pause == False:
            self.move_to_next_image(time_remaining)

    def view_filename(self):
        self.view_image_path = self.current_image_path
        self.show_entry(self.view_image_path, self.label_right, None)

    def write_filename(self):

        self.error_write_var.set("")

        if self.view_image_path == None:
            self.error_write_var.set("failed: no viewed image")
            return

        fail = "failed:"
        failed = False

        if self.append_list_file.get() == 1:
            file = self.file_name_var.get()
            if self.view_image_path:
                try:
                    f = open(file, "a")
                    f.write(self.view_image_path + "\n")
                    f.close()
                except IOError as e:
                    fail = fail + " append"
                    failed = True

        if self.copy_file.get() == 1:
            dir = self.dir_name_var.get()
            if os.access(dir, os.W_OK) == False:
                fail = fail + " copy"
                failed = True

            file_name = display_file(self.view_image_path)
            shutil.copy(file_name, dir, follow_symlinks=True)

        if failed:
            self.error_write_var.set(fail)
        else:
            self.error_write_var.set("done")


    def back_filename(self):
        self.move_to_previous_image()

    def forward_filename(self):
        self.move_to_next_image(int(DISPLAY_TIME_MS / 10))

    def pause_filename(self):
        if self.pause == True:
            self.pause = False
            self.pause_button.config(text="Pause")
            self.move_to_next_image(int(DISPLAY_TIME_MS / 10))
        else:
            self.pause_button.config(text="Run")
            self.pause = True

    def search(self):
        self.year_start_int = self.year_start_var.get()
        if int(self.year_start_int) < self.file_year_start_int:
            self.year_start_int = self.file_year_start_int
            self.year_start_var.set(self.year_start_int)

        self.month_start_int = self.month_start_var.get()

        self.year_end_int = self.year_end_var.get()
        if int(self.year_end_int) > self.file_year_end_int:
            self.year_end_int = self.file_year_end_int
            self.year_end_var.set(self.year_end_int)

        self.month_end_int = self.month_end_var.get()

        search_string = self.search_string_var.get().strip()
        if len(search_string) == 0:
            self.search_string = None
        else:
            self.search_string = search_string
            self.search_string_var.set(search_string)

        match = self.Load_image_list()
        if match == True:
            count = len(self.image_files)
            self.record_index = count - 1
            self.move_to_next_image(int(DISPLAY_TIME_MS / 10))
            self.error_search_var.set(f"{count} matches")
        else:
            self.error_search_var.set("no matches")

    def exit_app(self):
        self.self.top_frame.destroy()


def read_list_file(list_file):
    #
    # Load image list
    #
    #self.image_files = []
    first = True
    year_start = 0
    month_start = 0
    year_end = 0
    month_end = 0
    with open(list_file, "r") as f:
        for line in f:
            line = line.strip()
            file_name = display_file(line)
            year, month = display_file_year_month(file_name)

            if first == True:
                first = False
                year_start = year
                month_start = month
                year_end = year
                month_end = month
                continue

            if year_start > year:
                year_start = year
                month_start = month
                continue

            if year_start == year and month_start > month:
                month_start = month
                continue

            if year_end < year:
                year_end = year
                month_end = month
                continue

            if year_end == year and month_end < month:
                month_end = month
                continue

        return year_start, month_start, year_end, month_end


if __name__ == "__main__":
    #
    # parse the command line arguments
    #
    argc = len(sys.argv)
    if argc != 2:
        print(f"  {sys.argv[0]} : the argument count should be 2.  You supplied  {argc}.")
        print("  " + sys.argv[0] + " arguments should be:")

        print("    " + sys.argv[0] + "  link_list_sh_filename")

        exit(1)

    list_file = sys.argv[1]

    if not os.path.isfile(list_file):
        print("File not found: (" + list_file + ")")
        exit(0)

    year_start, month_start, year_end, month_end = read_list_file(list_file)

    root = tk.Tk()
    app = ImageViewer(root, list_file,
                      year_start, month_start,
                      year_end, month_end)
    root.mainloop()
