import cv2
import pandas as pd
import numpy as np

height = 800
width = 600
questions = 5
answers = 5


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
        return "A"
    elif j == 1:
        return "B"
    elif j == 2:
        return "C"
    elif j == 3:
        return "D"
    elif j == 4:
        return "E"

ans123 = []
rs = ""
df = pd.DataFrame(columns=['Answers'])
img = cv2.imread("D:/data/ans/123.png")
rs_img = cv2.resize(img, (width, height))

for i in range(0, 6):
    ans_img = rs_img[120+(i * 105):(220+(i*110)), 100:260]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    boxes = split_image(thresh)

    for i in range(0, questions):
        user_answer = None

        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + i * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j,pixels)
                s = j
        rs = Character_table(s)
        ans123.insert(len(ans123),rs)

for i in range(0, 6):
    ans_img = rs_img[120+(i * 105):(220+(i*110)), 375:530]
    gray = cv2.cvtColor(ans_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    boxes = split_image(thresh)

    for i in range(0, questions):
        user_answer = None
        for j in range(answers):
            pixels = cv2.countNonZero(boxes[j + i * 5])
            if user_answer is None or pixels > user_answer[1]:
                user_answer = (j, pixels)
                s = j
        rs = Character_table(s)
        ans123.insert(len(ans123),rs)

for i in range(0, len(ans123)):
    df.loc[i+1, 'Answers'] = ans123[i]
# export all answer to Answer_123.csv
df.to_csv('Answer_123.csv')
