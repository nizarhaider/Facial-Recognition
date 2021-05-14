import cv2
import numpy as np
import os
from datetime import datetime
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


path = 'query'
orb = cv2.ORB_create(nfeatures=1000)

### Importing Images
images = []
classNames = []

myList = os.listdir(path)
# print(myList)
# print('Total Classes Detected', len(myList))

for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    # print(cl)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findDes(images):
    desList = []
    for img in images:
        sp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

def findID(img,desList):
    kp2,des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList=[]
    finalvalue = -1
    try:

        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
        print(matchList)
    except:
        pass

    if len(matchList)!=0:
        if max(matchList) > 16:
            finalvalue = matchList.index((max(matchList)))
    return finalvalue



desList = findDes(images)
# print(len(desList))

cap = cv2.VideoCapture(0)
print("SHOW ID")

while True:

    success, img2 = cap.read()
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    id = findID(img2,desList)

    if id !=-1:
        cv2.putText(img2, classNames[id],(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        print("AIGHT YOU IS GOOD")

    # findID(img2, desList)
    cv2.imshow('Authentication', img2)
    cv2.waitKey(1)