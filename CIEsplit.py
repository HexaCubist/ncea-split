# -*- coding: utf-8 -*-
# Primary library
import mcstripper_refactor as mcstripper
# For putting files in tmp
from shutil import copyfile, copytree
# To get the file name
from os import path, makedirs
# Searching Directories
import glob
# Pausing for files to set in
import time
# For setting the window type
import ctypes
# File chooser
from tkinter import filedialog
import tkinter
import re
import json

# Intro and setting command prompt width
mcstripper.setupcli()
# Set Window Title
ctypes.windll.kernel32.SetConsoleTitleA(b"NCEA Split")

# Settings - Split into folders?
foldertype = input("First, how do you want to arrange the output images?\n1: own folder (default)\n2: all in one place (DISABLED)\n3: Sort by tags (DISABLED)\n>> ")
# if foldertype == "1" or foldertype == "2" or foldertype == "3":
# if foldertype == "1" or foldertype == "2":
#     foldertype = int(foldertype)
# else:
foldertype = 1

# Settings - Show numbers?
nonumbers = input("Next, do you want to have numbers in the final output? (y/n) - default yes\n>> ")
if nonumbers == "y":
    nonumbers = False
elif nonumbers == "n":
    nonumbers = True
else:
    nonumbers = False

merge_questions = input("Do you want to merge the questions? This is great as it provides one single image per question, with no page borders, but can be harder to place into exams (y/n) - default yes\n>> ")
if merge_questions == "y":
    merge_questions = False
elif merge_questions == "n":
    merge_questions = True
else:
    merge_questions = True

# Settings - setup
mcstripper.settings(foldertype, nonumbers, merge_questions)

# Get list of files
input("We are now going to ask for the files you wish to convert. Press ENTER to continue")
root = tkinter.Tk()
root.withdraw()
importfiles = filedialog.askopenfilenames(filetypes=[("pdf files", "*.pdf")])

# Where do we want to store when done?
input("When completed, where do you want to store the resulting image files?. Press ENTER to continue")
saveloc = filedialog.askdirectory(mustexist=True)

# Make temp folders
def makedirif(dir):
    tmpdir = path.relpath(dir)

    if not path.exists(tmpdir):
        makedirs(tmpdir)

makedirif(".tmp/")
makedirif(".tmp/html/")
makedirif(".tmp/html/qp/")
makedirif(".tmp/html/ms/")
makedirif(".tmp/img/")
makedirif(".tmp/img-ms/")

# Move files to TMP folder
for file in importfiles:
    finallocation = path.relpath(".tmp/" + path.basename(file))
    copyfile(file, finallocation)

# Get list of files
qp, ms = mcstripper.searchfiles()

# Make sure matching number of QP and MS pdfs
if not (len(qp) == len(ms)):
    input("[FATAL] Incorrect number of Question Papers to Mark Schemes (" + str(len(qp)) + " Question Papers vs " + str(len(ms)) + " Mark Schemes)\n\n" +
          "Press Enter to exit.")
    mcstripper.cleanup()
    exit()

# Convert QP and MS to html
qphtml, mshtml = mcstripper.convhtml(qp, ms)

# Get answers from the MSHTML
# msindent = ["", ""]
# msindent[0] = input("How many pixels to the left is the First row of answers? (For Cambridge files, the answer is 356) - Default 356\n>> ")
# if msindent[0] == "":
#     msindent[0] = "356"
# msindent[1] = input("How many pixels to the left is the Second row of answers? (For Cambridge files, the answer is 446) - Default 446\n>> ")
# if msindent[1] == "":
#     msindent[1] = "446"
# docanswers = mcstripper.getans(mshtml, ms, msindent)
# docanswers = mcstripper.getans(mshtml, ms)
# We no longer need to get the answers as we can feed in the same details from the doclocations array (answers are duplicate layout to questions)

# Get the Questions from the QPHTML
# qindent = input("How many pixels to the left is the question number? (For Cambridge files, the answer is 74) - Default 74\n>> ")
# if qindent == "":
#     qindent = "74"
# doclocations = mcstripper.getquestions(qphtml, qindent)
doclocations = mcstripper.getquestions(qphtml)


# Generate images of the Questions
mcstripper.genimg(qp, doclocations, foldertype, nonumbers, merge_questions)
mcstripper.genimg(ms, doclocations, foldertype, nonumbers, merge_questions, isms=True)
print("[INFO] Generating finished, saving files")
# Wait a moment
time.sleep(1)

# File info
export_paths = {}

# fix up any whitespace on the bottom
if foldertype == 1 or foldertype == 3:
    folders = glob.glob(".tmp/img/*")
    for folder in folders:
        newfoldername = path.basename(folder)
        # Check to see if this is a question
        questionmatch = re.findall('(\d+)-exm-(\d+)', newfoldername)
        print(questionmatch, newfoldername)
        if questionmatch:
            newfoldername = questionmatch[0][0] + "-" + questionmatch[0][1] + "-q"
        else:
            print(questionmatch)
            ansmatch = re.findall('(\d+)-exp-(\d+)-\w+', newfoldername)
            print(ansmatch)
            if ansmatch:
                newfoldername = ansmatch[0][0] + "-" + ansmatch[0][1] + "-a"
                files = glob.glob(folder + "/*")
                print(files)
                print(folder)
                for file in files:
                    print(file)
                    print(path.basename)
                    filename = path.basename(file)
                    export_paths.append([ansmatch[0][0] + "-" + ansmatch[0][1] + "-q" + "/" + filename, newfoldername + "/" + filename])
        finallocation = path.relpath(saveloc + "/" + newfoldername)
        copytree(folder, finallocation)

else:
    # Save images to folder
    finalimg = glob.glob(".tmp/img/*.png")
    for image in finalimg:
        finallocation = path.relpath(saveloc + "/" + path.basename(image))
        copyfile(image, finallocation)
finalans = glob.glob(".tmp/img-ms/*.png")
for image in finalans:
    makedirif(saveloc + "/ms/")
    finallocation = path.relpath(saveloc + "/ms/" + path.basename(image))
    copyfile(image, finallocation)


print("[SUCCESS] Job finished, cleaning up")
# cleanup
mcstripper.cleanup()

print("[SUCCESS] Clean up finished. Storying js of question-answer matches")
with open(path.relpath(saveloc + "/" + 'export.js'), 'w') as outfile:
    outfile.write("var examdata = ")
    json.dump(export_paths, outfile)


input("[SUCCESS] Export finished, Press ENTER to close")
