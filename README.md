# Facial-Recognition
A Facial Recognition Registration system that allows for new users to register on the spot using authentic ID

HOW IT WORKS:

UNREGISTERED USER

1) The system detects the face and runs the encodings collected from his face against trained encodings in the database and measuring the FaceDis value (this value can be altered if needed) of each trained face to the new user. If (FaceDis(max) - FaceDis(min) < threshhold), then user is unrecognised.
2) Now the algorithm prompts the user to show an ID and only authenticates the one it's been trained to authenticate. As soon as its authenticated it saves a snapshot on the image    in that frame and saves the ID and his face in the database.
3) A parallel OCR algorithm runs where it extracts the information(Name, ID Number, DOB, etc...) on the saved image of the ID and registers it into the database.

REGISTERED USER

1) As soon as a face is detected, encodings are ran aginst the trained faces and a match is found if (FaceDis(max) - FaceDis(min) > 0.2) by using the FaceDis(min) value.
2) The user is almost instantly allowed to pass



HOW TO USE:

1) Create folder of known faces in a directory and another for templates of ID's that can be used to register new user.
2) Link the folders to the pathways in the main.py code
3) Link output to a folder as well






Required Libraries:

1) OpenCV
2) Pytesseract
3) Face-Recognition
4) Cmake
5) dlib
6) numpy
