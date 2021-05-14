import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


path = 'ImagesAttendance'
imagesfr = []
classNamesfr = []
myListfr = os.listdir(path)
# print(myListfr)

for cl in myListfr:
    curImgfr = cv2.imread(f'{path}/{cl}')
    imagesfr.append(curImgfr)
    classNamesfr.append(os.path.splitext(cl)[0])
print(classNamesfr)

def findEncodings(imagesfr):
    encodeList = []

    for img in imagesfr:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        print(myDataList)
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')

encodeListKnown = findEncodings(imagesfr)
print('Encoding Complete Bitch')



### Authenticate ID

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
        # print(matchList)
    except:
        pass

    if len(matchList)!=0:
        if max(matchList) > 16:
            finalvalue = matchList.index((max(matchList)))
    return finalvalue



desList = findDes(images)
# print(len(desList))
count = 0




cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrframe = face_recognition.face_locations(imgS)
    encodeCurrframe = face_recognition.face_encodings(imgS, faceCurrframe)

    for encodeFace, faceLoc in zip(encodeCurrframe, faceCurrframe):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if (faceDis.max() - faceDis.min() <= 0.2):
            print("Unrecognized")
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Unrecognized", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            ### ID Authentication
            print("SHOW ID")
            while True:
                success2, img2 = cap.read()
                id = findID(img2, desList)

                ### OCR

                himg, wing, _ = img2.shape
                boxes = pytesseract.image_to_data(img2)
                # print(boxes)
                for x, b in enumerate(boxes.splitlines()):
                    if x != 0:
                        b = b.split()
                        # print(b)
                        if len(b) == 12:
                            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                            cv2.rectangle(img2, (x, y), (w + x, y + h), (0, 0, 255), 1)
                            cv2.putText(img2, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 50, 255), 2)

                ### OCR


                if id != -1:
                    count = count + 1
                    cv2.putText(img2, classNames[id], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    print("ID Authenticated")
                    cv2.imwrite('Saved ID/ID'+str(count)+".jpg", img2)



                    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


                    cv2.imwrite('ImagesAttendance/user' + str(count) + ".jpg", imgS)
                    break

                cv2.imshow('Authentication', img2)
                cv2.waitKey(1)
        elif matches[matchIndex]:
            name = classNamesfr[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            markAttendance(name)

    cv2.imshow('Facial Recognition', img)
    cv2.waitKey(1)
