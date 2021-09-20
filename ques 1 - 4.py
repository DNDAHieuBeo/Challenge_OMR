import cv2
import pandas as pd
import numpy as np
from helper import show_images
import os


def name(s2, j):
    fn = ""
    while s2[j].islower()==True:
        fn = s2[j] + fn
        j -= 1
    fn = s2[j] + fn
    sn = ""
    for k in range(j):
        sn = sn + s2[k]

    return fn, sn


# Create columns
df = pd.DataFrame(columns=['Student_ID', 'First_Name', 'Sur_Name', 'Code'])
lst = os.listdir("D:/data/grading")

id = []
cd = []
fst = []
sur = []
for i in range(0, len(lst)):
    s = lst[i]
    j = 0
    id.append("")
    while s[j] != "_":
        id[i] = id[i] + s[j]
        j += 1
    j += 1
    s2 = ""
    for h in range(j, len(s)):
        if s[h] == "_":
            j = h + 1
            break
        s2 = s2 + s[h]
    cd.append("")
    while j < len(s):
        cd[i] = cd[i] + s[j]
        j += 1
    cd[i] = cd[i][0:3]
    j = len(s2) - 1
    fn, sn = name(s2, j)

# create students_file to data_file
    sur.append("")
    fst.append("")
    fst[i] = fst[i]+fn
    sur[i] = sur[i]+sn

    df.loc[i, 'Student_ID'] = id[i]
    df.loc[i, 'Code'] = cd[i]
    df.loc[i, 'First_Name'] = fst[i]
    df.loc[i, 'Sur_Name'] = sur[i]

height = 800
width = 600
questions = 5
answers = 5

img = cv2.imread("D:/data/grading/2000100_LeCongVinh_123.png")
rimg = cv2.resize(img, (width, height))


def split_image(image):
    # make the number of rows and columns
    # a multiple of 5 (questions = answers = 5)
    r = len(image) // questions * questions
    c = len(image[0]) // answers * answers
    image = image[:r, :c]
    # split the image horizontally (row-wise)
    rows = np.vsplit(image, questions)
    boxes = []
    for row in rows:
        # split each row vertically (column-wise)
        cols = np.hsplit(row, answers)
        for box in cols:
            boxes.append(box)
    return boxes


def Character_table(j):
    if j == 0:
        print("A")
    elif j == 1:
        print("B")
    elif j == 2:
        print("C")
    elif j == 3:
        print("D")
    elif j == 4:
        print("E")


# Ques 3
doc_img = rimg[120:215, 105:263]
gray = cv2.cvtColor(doc_img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
boxes = split_image(thresh)
print('The first 5 ans: ')
for h in range(0, questions):
    user_answer = None

    for j in range(answers):
        pixels = cv2.countNonZero(boxes[j + h * 5])
        if user_answer is None or pixels > user_answer[1]:
            user_answer = (j, pixels)
            s = j

    Character_table(s)


def ans1_30(jump):

    ans_img = rs_img[120 + (jump * 105):(220 + (jump * 110)), 100:260]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    boxes = split_image(thresh)
    # show_images(['test'],[thresh])
    for h in range(0, questions):
        user_answer = None

        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + h * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                s = j
        Character_table(s)


def ans31_60(jump):
    ans_img = rs_img[120 + (jump * 105):(220 + (jump * 110)), 375:530]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    boxes = split_image(thresh)

    for h in range(0, questions):
        user_answer = None
        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + h * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                s = j
        Character_table(s)


# Ques 2: Generating Student.csv
df.to_csv('D:/data/students.csv')
# Ques 3: Generating first 5 answers of one student and image
demo_img = rimg[120:220, 45:260]
show_images(['First 5 ans'], [demo_img])

# Ques 4: Generating all answers of one student
img = cv2.imread("D:/data/grading/2000101_DangVanLam_123.png")
rs_img = cv2.resize(img, (width, height))
print('All ans of one student: ')
for i in range(0, 6):
    ans1_30(i)
for i in range(0, 6):
    ans31_60(i)
