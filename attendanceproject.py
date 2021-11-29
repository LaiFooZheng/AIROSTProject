import cv2.cv2 as cv2
import numpy as np
import face_recognition
import os
import db

# os.chdir('pythonProject')  # need ot ammend path

path = 'image'  # print the list of images in directory, need to ammend path
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)
'''for cl in myList:  # print files without extension name, cl=class
    curImg = cv2.imread(f'{path}/{cl}')  # curImg = current image
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])'''

# print(classNames)


def saveEncodings(ie, image_name):  # perform encoding function and calculate number of encoded images
    img = cv2.imread(f'{path}/{image_name}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("Image Processed!")
    encode = face_recognition.face_encodings(img)[0]
    print(encode)
    for e in range(len(encode)):
        print(encode[e])
        db.face[e][ie].value = encode[e]
    db.save_2()
    print("Saved!")


def findEncodings(images):  # perform encoding function and calculate number of encoded images
    encodeList = []
    for ie in range(len(images)):
        img = images[ie]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def loadEncodings():  # load encoded info from excel file (row 4 to 131)
    encodeList = []
    for ie in range(len(db.face[0])):
        encode = []
        for e in range(len(db.face)):
            encode.append(db.face[e][ie].value)
        encodeList.append(encode)
    return encodeList


# encodeListKnown = findEncodings(images)  # print num of encoded images
encodeListKnown = loadEncodings()
print('Encoding complete')


cap = cv2.VideoCapture(0)


'''def recogn():  # face recognition
    while True:
        ret, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize pict
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)  # encode current face
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):  # calculate the percentage of match
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)  #will give small decimal values
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:  # if match image, name will be printed out
                name = db.nam[matchIndex].value
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)  # open webcam, press q to exit
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break'''


def verifi(ed):  # face verification
    persis = 0
    timer = 0
    while True:
        ret, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize pict
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)  # encode current face
        encodesCurFrame = np.array(face_recognition.face_encodings(imgS, facesCurFrame))

        if encodesCurFrame != []:
            matches = face_recognition.compare_faces(encodeListKnown[ed], encodesCurFrame)
            # matchIndex = face_recognition.face_distance(encodeListKnown[ed], encodesCurFrame)

            if matches == [True]:  # if match image, name will be printed out
                persis = persis + 1

            if persis >= 5:
                cv2.destroyAllWindows()
                return True

        cv2.imshow('Webcam', img)  # open webcam, press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def registerEncodings():  # face verification
    while True:
        ret, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resize pict
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)  # encode current face
        encodesCurFrame = np.array(face_recognition.face_encodings(imgS, facesCurFrame))

        if encodesCurFrame != []:
            y1, x2, y2, x1 = facesCurFrame[0]
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow('Webcam', img)  # open webcam, press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print("Face id captured!")
            return encodesCurFrame[0]


# recogn()
# verifi(2)
