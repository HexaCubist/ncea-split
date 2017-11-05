# for finding files
import glob
# for running poppler
import subprocess
import os
# for getting paths
from os import path
# for regexing stuff
import re
# to do some post-processing
from PIL import Image, ImageChops, ImageDraw
# For Cleaning up the .tmp folder
import shutil
# For better memory when gathering answers
import mmap
# Logging!
import logging

logging.basicConfig(filename='mcstripper.log', filemode='w',level=logging.DEBUG, format='[%(levelname)s] %(message)s')
def reglob(path, exp, invert=False):
    """glob.glob() style searching which uses regex

    :param exp: Regex expression for filename
    :param invert: Invert match to non matching files
    """

    m = re.compile(exp)

    if invert is False:
        res = [f for f in os.listdir(path) if m.search(f)]
    else:
        res = [f for f in os.listdir(path) if not m.search(f)]

    res = map(lambda x: "%s/%s" % (path, x, ), res)
    return res

def setupcli():
    os.system("mode con cols=150 lines=30")
    print(r"________/\\\\\\\\\__/\\\\\\\\\\\__/\\\\\\\\\\\\\\\_____________________________/\\\\\\________________________        ".center(149, " "))
    print(r" _____/\\\////////__\/////\\\///__\/\\\///////////_____________________________\////\\\________________________       ".center(149, " "))
    print(r"  ___/\\\/_______________\/\\\_____\/\\\____________________________/\\\\\\\\\_____\/\\\_____/\\\_____/\\\______      ".center(149, " "))
    print(r"   __/\\\_________________\/\\\_____\/\\\\\\\\\\\______/\\\\\\\\\\__/\\\/////\\\____\/\\\____\///___/\\\\\\\\\\\_     ".center(149, " "))
    print(r"    _\/\\\_________________\/\\\_____\/\\\///////______\/\\\//////__\/\\\\\\\\\\_____\/\\\_____/\\\_\////\\\////__    ".center(149, " "))
    print(r"     _\//\\\________________\/\\\_____\/\\\_____________\/\\\\\\\\\\_\/\\\//////______\/\\\____\/\\\____\/\\\______   ".center(149, " "))
    print(r"      __\///\\\______________\/\\\_____\/\\\_____________\////////\\\_\/\\\____________\/\\\____\/\\\____\/\\\_/\\__  ".center(149, " "))
    print(r"       ____\////\\\\\\\\\__/\\\\\\\\\\\_\/\\\\\\\\\\\\\\\__/\\\\\\\\\\_\/\\\__________/\\\\\\\\\_\/\\\____\//\\\\\___ ".center(149, " "))
    print(r"        _______\/////////__\///////////__\///////////////__\//////////__\///__________\/////////__\///______\/////____".center(149, " "))
    print(r" ".center(149, " "))
    print(r"A program by Zac M-W".center(149, " "))
    print(r" ".center(149, " "))
    print(r" ".center(149, " "))

    # print(r"  ____   ___   _____     ____    ____    _       ___   _____ ".center(114, " "))
    # print(r" / ___| |_ _| | ____|   / ___|  |  _ \  | |     |_ _| |_   _|".center(114, " "))
    # print(r"| |      | |  |  _|     \___ \  | |_) | | |      | |    | |  ".center(114, " "))
    # print(r"| |___   | |  | |___     ___) | |  __/  | |___   | |    | |  ".center(114, " "))
    # print(r" \____| |___| |_____|   |____/  |_|     |_____| |___|   |_|  ".center(114, " "))
    # print(r"                                                             ".center(114, " "))
    # print(r"                    A program by Zac M-W                     ".center(114, " "))
    # print(r"                                                             ".center(114, " "))
    # print(r"                                                             ".center(114, " "))


def settings(foldertype, nonumbers, merge_questions):
    # split folders or not?
    foldertype = foldertype
    print("[INFO] Folder type set to " + str(foldertype))
    logging.info("Folder type set to " + str(foldertype))
    nonumbers = nonumbers
    print("[INFO] Question numbers set to " + str(nonumbers))
    logging.info("Question numbers set to " + str(nonumbers))
    merge_questions = merge_questions
    print("[INFO] Merging questions set to " + str(merge_questions))
    logging.info("Merging questions set to " + str(merge_questions))


def trimbot(impath, nonumbers=True):
    im = Image.open(impath)
    w, h = im.size
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    if not diff.getbbox():
        os.remove(impath)
        print("[INFO] Trimbot just removed an empty image. This can happen, do not panic.")
        logging.info("Trimbot just removed an empty image. This can happen, do not panic.")
        return
    left, upper, right, lower = diff.getbbox()
    cropdim = (0, 0, w, lower + 5)
    cropped = im.crop(cropdim)
    cropped.save(impath)
    im = Image.open(impath)
    w, h = im.size
    if nonumbers:
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (44, 100)], fill="white")
    im.save(impath)

def merge_images(file1, file2):
    """Merge two images into one, displayed one on top of the other
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = max(width1, width2)
    result_height = height1 + height2

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))
    result.save(file1)
    os.remove(file2)

def searchfiles():
    # search for files
    files = glob.glob('./.tmp/*.pdf')
    # detect if there are any files, then output list of files
    if not files == []:
        print("[INFO] Files found\n")
        logging.info("Files found\n")
        print("[INFO] Finding question papers...")
        logging.info("Finding question papers...")
        qp = glob.glob('./.tmp/*exm*.pdf')
        qp.sort()
        print("[INFO] Finding exemplars...")
        logging.info("Finding exemplars...")
        ms = glob.glob('./.tmp/*exp*.pdf')
        ms.sort()
        return [qp, ms]
    else:
        input("[SEVERE] No files found")
        return "Error code 01: Files not found"
'''
print("\n")
print("Here are the question papers:")
print("\n".join(qp))
print("\n")
print("Here are the mark schemes:")
print("\n".join(ms))
print("\n")
'''

# Delete all temp files
def remdir(loc):
    files = glob.glob(loc)
    for f in files:
        os.remove(f)


def cleanup():
    shutil.rmtree(".tmp/", ignore_errors=True)


def convhtml(qp, ms):
    # convert each question paper and mark scheme to html
    print("[INFO] Converting to html")
    logging.info("Converting to html")
    for paper in qp:
        execloc = path.relpath("libs/poppler/bin/pdftohtml.exe")
        startloc = path.relpath(paper)
        endloc = path.relpath(".tmp/html/qp/" + paper[7:])
        with open(os.devnull, "w") as f:
            subprocess.call([execloc, "-noframes", "-c", "-s", "-i",
                             startloc, endloc], stdout=f)
    for paper in ms:
        execloc = path.relpath("libs/poppler/bin/pdftohtml.exe")
        startloc = path.relpath(paper)
        endloc = path.relpath(".tmp/html/ms/" + paper[7:])
        with open(os.devnull, "w") as f:
            subprocess.call([execloc, "-noframes", "-c", "-s", "-i", startloc,
                            endloc], stdout=f)
    # Get files just generated
    qphtml = glob.glob('./.tmp/html/qp/*.html')
    mshtml = glob.glob('./.tmp/html/ms/*.html')
    logging.debug([qphtml, mshtml])
    return [qphtml, mshtml]


def getquestions(qphtml, qindent="74"):
    # make variable that will contain all locations in each document
    '''
    structure:
    [
        [ # document
            [locations], #page
            [locations] #page
        ]
    ]
    '''
    doctaglist = {
        "Classification": {"keywords": [
            "Kingdom",
            "Phylum",
            "Family",
            "year 9s",
            "Lucy",
            "12v",
            "Towey",
            "Dicot "
        ]},
        "Organisation of the organism": {"keywords": [
            "Stack",
            "Tree",
            "Membrane",
            "compartmentalisation",
            "nucleus",
            "Vacuole",
            "cell membrane",
            "Root hair cells",
            "Palisade",
            "organ system"
        ]},
        "Movement in and out of the Cell": {"keywords": [
            "Osmosis",
            "concentration gradient ",
            "Channel proteins",
            "Active Transport",
            "Osmotic Potential",
            "Diffusion",
            "magnification",
            "red blood cells"
        ]},
        "Biological Molecules ": {"keywords": [
            "proteins",
            "Enzymes",
            "Carbohydrates",
            "Glycogen",
            "Fats",
            "Lipids",
            "dick"
        ]},
        "Enzymes": {"keywords": [
            "Amylase",
            "Protease",
            "Hormones",
            "Digestive",
            "Defensive",
            "lipase"
        ]},
        "Plant nutrition": {"keywords": [
            "Starch",
            "Photosynthesis",
            "Magensium",
            "Nitrogen",
            "nitrogen Cycle",
            "Carbon Cycle",
            "Carbon Dioxide"
        ]},
        "Human Nutrition": {"keywords": [
            "Digestion",
            "Stomach",
            "Intestines",
            "Vitamin C",
            "Vitamin D",
            "Deamination",
            "Glucose"
        ]},
        "Transport in plants": {"keywords": [
            "Phloem",
            "Xylem",
            "sucrose",
            "Monocot",
            "Dicot"
        ]},
        "Transport in animals": {"keywords": [
            "Blood",
            "vespa",
            "Haemoglobin",
            "mr towey"
        ]},
        "Disease and immunity": {"keywords": [
            "ebola",
            "Immune system",
            "Antibodies",
            "sickle cell anaemia",
            "Genetic",
            "Contagious",
            "Bacterial",
            "Viral",
            "Fungal"
        ]},
        "Gas exchange in Humans": {"keywords": [
            "Lungs",
            "Alveoli",
            "Bronchi",
            "bronchus",
            "Air  sacs",
            "Oxygen"
        ]},
        "Respiration": {"keywords": [
            "Mitochondria",
            "Breathing",
            "Glucose",

        ]},
        "Excretion in humans": {"keywords": [
            "Kidneys",
            "carbon dioxide",
            "Liver",
            "Urea",
            "Loop Of Henle",
            "medulla",
            "dialysis",
            "Transplant "
        ]},
        "Coordination and response": {"keywords": [
            "Nervous system",
            "Twitchiness",
            "Falling Over",
            "relay"
        ]},
        "Drugs": {"keywords": [
            "Cocaine",
            "depression",
            "Stimulents ",
            "Depressents",
            "Alcohol",
            "methylated spirits"
        ]},
        "Reproduction": {"keywords": [
            "sperm",
            "vagina",
            "orgasm",
            "yes!!!!",
            "ZYGOTE",
            "*orgasmic scream*",
            "Placenta",
            "STOP DELETING PENIS ITS PART OF REPRODUCTION"
        ]},
        "Inheritance": {"keywords": [
            "dick",
            "Allele",
            "Gene",
            "mr towey",
            "mr towey"
        ]},
        "Variation and Selection": {"keywords": [
            "woman with beards",
            "survival of",
            "Mutation",
            "Natural selection",
            "evolution",
            "mr towey",
            "Darwin Awards",
            "<--YES"
        ]},
        "Organisms and their environments": {"keywords": [
            "mr towey",
            "mr toweys baby",
            "mr toweys wife",
            "mr toweys house"
        ]},
        "Biotechnology and Genetic engineering": {"keywords": [
        ]},
        "Human Influences on ecosystems": {"keywords": [
            "death",
            "destruction",
            "global warming",
            "Ecosystem Collapse",
            "deforestation",
            "Extinction",
            "ISIS"
        ]}
    }
    # doctaglist = {
    #     "Classification of Life": {"keywords": [
    #         "living organisms",
    #         "excretion",
    #         "respiration",
    #         "characteristic",
    #         "species",
    #         "identify the",
    #         "athropod",
    #     ]},
    #     "Cells": {"keywords": [
    #         "cell"
    #     ]},
    #     "Movement in and out of Cells": {"keywords": []},
    #     "Biological molecules": {"keywords": []},
    #     "Enzymes": {"keywords": [
    #         "enzyme"
    #     ]},
    #     "Plant nutrition": {"keywords": []},
    #     "Human nutrition": {"keywords": []},
    #     "Transport in plants": {"keywords": [
    #         "osmosis",
    #         "diffusion",
    #         "active transport",
    #         "translocation",
    #         "transpiration"
    #     ]},
    #     "Transport in animals": {"keywords": [
    #         "osmosis",
    #         "diffusion",
    #         "active transport",
    #         "translocation",
    #         "transpiration"
    #     ]},
    #     "Diseases and immunity": {"keywords": []},
    #     "Gas exchange in humans": {"keywords": []},
    #     "Respiration": {"keywords": []},
    #     "Excretion in humans": {"keywords": []},
    #     "Co-ordination and response": {"keywords": []},
    #     "Drugs": {"keywords": []},
    #     "Reproduction": {"keywords": []},
    #     "Inheritance": {"keywords": []},
    #     "Variation and selection": {"keywords": []},
    #     "Organisms and their environment": {"keywords": []},
    #     "Biotechnology and genetic engineering": {"keywords": []},
    #     "Human influences on ecosystems": {"keywords": []},
    # }
    currentdoc = 0
    pagenum = -1
    questionnum = -1
    alreadycrossed = False
    docquestions = []

    # get location of places to split pdf
    for doc in qphtml:
        docquestions.append([])
        file = path.relpath(doc)
        with open(file, encoding="utf8") as f:
            questions = f.read()
            docquestions[currentdoc] = []
            print("[INFO] Beginning to proccess " + doc)
            logging.info("Beginning to proccess " + doc)
            # Calculate the start and end locations for the questions, as we will need this when we come to generate the images.
            qlist = re.findall("page(\d+)-div|top:(\d+).+<b>QUESTION|top:(\d+).+left:64px.+\(\w\)", questions)
            logging.info(qlist)
            questionCoords = []
            pagenum = -1
            mainquestion = -1

            for item in qlist:
                logging.info(item)
                # If it's ('XXX', '', '') then we know it's a page header
                if item[0]:
                    pagenum = int(item[0])
                    if len(questionCoords) > 0:
                        questionCoords[-1]["endpage"] = pagenum
                # If it's ('', 'XXX', '') then we know it's an answer location
                if item[1]:
                    questionCoords.append({
                        "startpage": pagenum,
                        "endpage": pagenum,
                        "startcoord": int(item[1]),
                        "subcuts": []
                        })
                # If it's ('', '', 'XXX') then we know it's a subanswer location
                if item[2]:
                    # If there is a previous subcut
                    logging.info(questionCoords)
                    if len(questionCoords[-1]["subcuts"]) > 0:
                        # Update coords of last question to trim to this question
                        questionCoords[-1]["subcuts"][-1]["endpage"] = pagenum
                        questionCoords[-1]["subcuts"][-1]["endloc"] = int(item[2])

                    questionCoords[-1]["subcuts"].append({
                        "startpage": pagenum,
                        "startloc": int(item[2]),
                        "endpage": pagenum,
                        "endloc": 1130
                        })
            docquestions[currentdoc] = questionCoords
        print("[INFO]     - Found " + str(len(docquestions[currentdoc])) + " questions")
        logging.info("    - Found " + str(len(docquestions[currentdoc])) + " questions")
        currentdoc += 1
    logging.debug(docquestions)
    return docquestions


def genimg(qp, docquestions, foldertype, nonumbers, merge_questions, isms=False):
    type = ""
    if isms:
        type = "answer"
    else:
        type = "question"
    print("[INFO] Generating images for each " + type + "..")
    logging.info("Generating images for each " + type + "..")
    print("[INFO] Estimated time to complete is " + str(int(len(qp)*6)) +
          " seconds")
    logging.info("Estimated time to complete is " + str(int(len(qp)*6)) +
          " seconds")
    currentdoc = 0
    for paper in qp:
        newimgname = path.basename(paper)
        # Check to see if this is a question
        questionmatch = re.findall('(\d+)-exm-(\d+)', newimgname)
        print(questionmatch, newimgname)
        if questionmatch:
            newimgname = questionmatch[0][0] + "-" + questionmatch[0][1] + ""
        else:
            print(questionmatch)
            ansmatch = re.findall('(\d+)-exp-(\d+)-\w+', newimgname)
            print(ansmatch)
            if ansmatch:
                newimgname = ansmatch[0][0] + "-" + ansmatch[0][1] + ""
        i = 0
        mainQuestionNumber = 0
        for mainQuestion in docquestions[currentdoc]:
            mainQuestionNumber += 1
            for question in mainQuestion["subcuts"]:
                if foldertype == 1:
                    directory = path.relpath(".tmp/img/" + paper[7:-4] + "/")
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    paperfolder = paper[7:-4] + "/"
                    multiloc = False
                elif foldertype == 2:
                    paperfolder = ""
                    multiloc = False
                qpart = 1
                for qpage in range(question["startpage"], question["endpage"]+1):
                    logging.info("Generating images for paper")
                    if question["startpage"] == question["endpage"]:
                        aheight = question["endloc"] - question["startloc"]
                        astart = question["startloc"]
                    elif qpage == question["startpage"]:
                        aheight = 1130 - question["startloc"]
                        astart = question["startloc"]
                    elif qpage == question["endpage"]:
                        aheight = question["endloc"] - 60
                        astart = 60
                    else:
                        aheight = 1130 - 60
                        astart = 60
                    awidth = 850
                    execloc = path.relpath("libs/poppler/bin/pdftoppm.exe")
                    startloc = path.relpath(".tmp/" + qp[currentdoc][7:])
                    # if docanswers[currentdoc]["answers"] == []:
                    #     suffix = ""
                    # else:
                    #     suffix = docanswers[currentdoc]["answers"][i]
                    if isms:
                        suffix = "ms"
                    else:
                        suffix = ""
                    endloc = path.relpath(".tmp/img/" + paperfolder + newimgname + "q"  + str(mainQuestionNumber) + "s" + str(i + 1) + suffix + "p" + str(qpart))
                    command = (execloc + " -png -f " + str(qpage) + " -l " +
                               str(qpage) + " -singlefile -x 64 -y " +
                               str(astart*2) + " -W " + str(awidth*2) + " -H " +
                               str(aheight*2) +
                               ' -scale-to-x 1784 -scale-to-y 2526 "' + startloc +
                               '" "' + endloc + '"')
                    logging.debug(command)
                    with open(os.devnull, "w") as f:
                        subprocess.call(command, stdout=f)
                    qpart += 1
                if merge_questions:
                    filestomerge = glob.glob('./.tmp/img/' + paperfolder + newimgname + "q"  + str(mainQuestionNumber) + "s" + str(i + 1) + suffix + 'p*')
                    filestomerge.sort()
                    for image in filestomerge:
                        trimbot(image, False)
                    filestomerge = glob.glob('./.tmp/img/' + paperfolder + newimgname + "q"  + str(mainQuestionNumber) + "s" + str(i + 1) + suffix + 'p*')
                    filestomerge.sort()
                    for x in range(1, len(filestomerge)):
                        merge_images(filestomerge[0], filestomerge[x])
                    # Remove question numbers and rename
                    renamefrom = path.relpath('./.tmp/img/' + paperfolder + newimgname + "q"  + str(mainQuestionNumber) + "s" + str(i + 1) + suffix + 'p1' + '.png')
                    renameto = path.relpath('./.tmp/img/' + paperfolder + newimgname + '_q'  + str(mainQuestionNumber) + "s" + str(i + 1) + '.png')
                    os.rename(renamefrom, renameto)
                    trimbot(renameto, nonumbers)
                else:
                    filestotrim = glob.glob('./.tmp/img/' + paperfolder + newimgname + "q"  + str(mainQuestionNumber) + "s" + str(i + 1) + suffix + 'p*')
                    for image in filestotrim:
                        trimbot(image, False)
                    trimbot(image[0], nonumbers)
                print("[INFO] Generated image for question " + str(i + 1) + " in doc " + str(currentdoc + 1))
                logging.info("Generated image for question " + str(i + 1) + " in doc " + str(currentdoc + 1))
                i += 1
        currentdoc += 1
