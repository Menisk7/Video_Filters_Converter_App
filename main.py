import cv2
import os
import sys
import shutil

def vidToJpg(video):
    datalist = []
    imgarr = []
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
        if (currentFrame % 30 == 0):
            print('frame ' + str(currentFrame))
        # Adds images to imgarr
        imgarr.append([name, frame])
        # Datalist consists of images names
        datalist.append(name)
        currentFrame += 1

    # Saves images
    saveImages(imgarr)
    # When everything done, release the capture
    print('vid to jpg done...')
    cap.release()
    cv2.destroyAllWindows()
    return datalist


def saveImages(imgarr):
    print('saving images...')
    # print(imgarr[0][0])
    # print(imgarr[0][1])

    for i in range(len(imgarr)):
        # imgarr has a structure like [ [name,frame]]
        # so you do this imgarr[i][0] for name
        # and  imgarr[i][1] for frame
        if (i % 30 == 0):
            print('saved image ' + str(i))
        cv2.imwrite(imgarr[i][0], imgarr[i][1])


def makeEdgeJpg(datalist, t_lower, t_upper, L2Gradient, definition=7):
    currentFrame = 0
    print('creating edge jpgs....')
    dataEL = []

    for file in datalist:
        img = cv2.imread(file)
        edge = cv2.Canny(img, t_lower, t_upper, apertureSize=definition, L2gradient=L2Gradient)
        name = './dataEdge/frame' + str(currentFrame) + '.jpg'
        cv2.imwrite(name, edge)
        dataEL.append(name)
        if (currentFrame % 30 == 0):
            print('frame ' + str(currentFrame))
        currentFrame += 1

    return dataEL


def makeEdgeVid(dataEdge):
    size = (0, 0)
    img_array = []
    print('creating edge vid....')

    for i in range(len(dataEdge)):
        img = cv2.imread(dataEdge[i])
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        if (i % 30 == 0):
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


####################
#       MAIN       #
####################
# sys.argv[1] gets command line parameter
# example: python main.py name_of_the_video.mp4
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
    createDirs()
    datalist = vidToJpg(fileName)
    dataEdge = makeEdgeJpg(datalist, lower, upper, L2Gradient, definition)
    makeEdgeVid(dataEdge)
    cleanUp()
else:
    print("Input Video" + fileName + " not found")
