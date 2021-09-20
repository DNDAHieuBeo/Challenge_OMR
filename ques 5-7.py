import os
import cv2
import csv
import numpy as np
import pandas as pd

height = 800
width = 600
questions = 5
answers = 5


def Character_table(j):
    if j == 0:
        return "A"
    elif j == 1:
        return "B"
    elif j == 2:
        return "C"
    elif j == 3:
        return "D"
    elif j == 4:
        return "E"


def ans1_30(jump):
    list_ans = []
    ans_img = img[120 + (jump * 105):(220 + (jump * 110)), 100:260]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    boxes = split_image(thresh)

    for i in range(0, questions):
        user_answer = None

        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + i * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                f_ans = j
        list_ans.append(Character_table(f_ans))
    return list_ans


def ans31_60(jump):
    list_ans = []
    ans_img = img[120 + (jump * 105):(220 + (jump * 110)), 375:530]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

    boxes = split_image(thresh)

    for i in range(0, questions):
        user_answer = None

        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + i * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                f_ans = j
        list_ans.append(Character_table(f_ans))
    return list_ans


def split_image(image):
    r = len(image) // questions * questions
    c = len(image[0]) // answers * answers
    image = image[:r, :c]
    rows = np.vsplit(image, questions)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, answers)
        for box in cols:
            boxes.append(box)

    return boxes


# ques 5:
ques = []
for i in range(0, 60):
    ques.append(0)
ans = []
file_ans = pd.read_csv("D:/data/ans/Answer_123.csv")
# get Answers from file into an array
for i in range(0, 60):
    ans.append("")
    ans[i] = ans[i] + file_ans.loc[i, 'Answers']

# generating grading.csv
grd = pd.read_csv("D:/data/students.csv")
df = pd.DataFrame(columns=['Student_ID', 'Grading'])
for i in range(0, len(grd)):
    df.loc[i, 'Student_ID'] = grd.loc[i, 'Student_ID']

# path to student work
path = "D:/data/grading"
dirs = os.listdir(path)

spt = ""
r_ans = 0
for file in dirs:
    spt = path + "/" + file

    img = cv2.imread(spt)
    img = cv2.resize(img, (width, height))

    lst_ans = []
    for i in range(0, 6):
        lst_ans.append(ans1_30(i))
    for i in range(0, 6):
        lst_ans.append(ans31_60(i))

    # grading:
    score = 0
    for i in range(0, 12):
        for j in range(0, 5):
            if lst_ans[i][j] == ans[i * 5 + j]:
                score += 1
            else:
                ques[i * 5 + j] += 1
    df.loc[r_ans, 'Grading'] = score
    r_ans += 1
df.to_csv('grading.csv')

# ques 6: Summary which 3 questions are the most difficult
dif_ans = []
for i in range(len(ques)):
    dif_ans.append(ques[i])
ques.sort(reverse=True)
print("The three question are the most difficult: ")
diff = 0

for i in range(0, 3):
    while j < len(dif_ans):
        if ques[i] == dif_ans[diff]:
            print('Question: ', diff)
            diff += 1
            break
        else:
            diff += 1

# ques 7:
df = pd.read_csv("D:/data/students.csv")
df['Pass/Fail'] = None
df2 = pd.read_csv("D:/data/grading.csv")

for i in range(0, len(df)):
    chs = df2.loc[i, 'Grading']
    if chs >= 30:
        df.loc[i, 'Pass/Fail'] = 'Pass'
    else:
        df.loc[i, 'Pass/Fail'] = 'Fail'
df.to_csv('students.csv')
