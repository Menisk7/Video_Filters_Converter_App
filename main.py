import cv2
import os
import sys
import shutil

frames = []
imgNames = []
dataEdge = []


def vidToJpg(video):
    global imgNames
    global frames
    # Capture frames from file:
    cap = cv2.VideoCapture(video)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print('Error: Creating directory of data')

    currentFrame = 0
    # cap.read returns tuple
    # [0]=ret [1]=frame
    # cap.read()[1]
    # gets the number of frames

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    for i in range(length):
        # Capture frame-by-frame
        ret, frame = cap.read()
        name = './data/frame' + str(currentFrame) + '.jpg'

        print('vid to jpg frame ' + str(currentFrame))
        # Adds frames to frames array
        frames.append(frame)
        # imgNames are not modified
        imgNames.append(name)
        cv2.imwrite(name, frame)
        currentFrame += 1

    # When everything done, release the capture
    print('vid to jpg done...')
    cap.release()
    cv2.destroyAllWindows()


def makeEdgeJpg(imgNames, t_lower, t_upper, L2Gradient, imgOption, definition=7):
    currentFrame = 0
    print('creating edge jpgs....')
    global dataEdge
    imgOut = ""
    for file in imgNames:
        img = cv2.imread(file)

        # sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=100, sigma_r=0.2, shade_factor=0)
        match imgOption:
            case "canny":
                imgOut = cv2.Canny(img, t_lower, t_upper, apertureSize=definition, L2gradient=L2Gradient)
            case "pencil":
                imgOut = cv2.pencilSketch(img, sigma_s=100, sigma_r=0.2, shade_factor=0)
            case _:
                imgOut = img

        name = './dataEdge/frame' + str(currentFrame) + '.jpg'
        cv2.imwrite(name, imgOut)
        dataEdge.append(name)
        if currentFrame % 30 == 0:
            print('edge frame ' + str(currentFrame))
        currentFrame += 1


def makeEdgeVid():
    global dataEdge
    size = (0, 0)
    img_array = []
    print('creating edge vid....')

    for i in range(len(dataEdge)):
        img = cv2.imread(dataEdge[i])
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        if i % 30 == 0:
            print('frame ' + str(i))

    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print('edge vid done')


def createDirs():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('dataEdge'):
            os.makedirs('dataEdge')
    except OSError:
        print("Error: Couldn't create directories!")


def cleanUp():
    try:
        shutil.rmtree("data")
        shutil.rmtree("dataEdge")
    except OSError as e:
        print("Error: Couldn't remove directories: dataEdge/data")


def devMode(x): return x


####################
#       MAIN       #
####################
# sys.argv[1] gets command line parameter
# example: python main.py name_of_the_video.mp4


if devMode(1):
    fileName = "testvid.mp4"
else:
    if len(sys.argv) == 1:
        fileName = input("Type name of the file: ")
    else:
        fileName = sys.argv[1]

if os.path.isfile(fileName):
    # Defining all the parameters
    definition = 3  # odd between 3 and 7 including
    L2Gradient = False  # Boolean L2Gradient is  abs(gradient_x) + abs(gradient_y)
    lower = 100  # Lower Threshold
    upper = 350  # Upper threshold
    vidEffect = "canny"
    createDirs()
    vidToJpg(fileName)
    makeEdgeJpg(imgNames, lower, upper, L2Gradient, vidEffect, definition)
    makeEdgeVid()
    cleanUp()
else:
    print("Input Video" + fileName + " not found")
