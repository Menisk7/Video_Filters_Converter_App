import shutil
import cv2
import os


def vidToJpg(video, dataPath):
    data = []
    # Capture frames from file:
    cap = cv2.VideoCapture(video)
    try:
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)
    except OSError:
        print('Error: Creating directory of data')

    currentFrame = 0
    # cap.read returns tuple
    # [0]=ret [1]=frame
    # cap.read()[1]
    # gets the number of frames

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Getting jpgs from video')
    for i in range(length):
        # Capture frame-by-frame
        ret, frame = cap.read()
        path = './' + dataPath + '/frame' + str(currentFrame) + '.jpg'

        print('vid to jpg frame ' + str(currentFrame))
        data.append(path)
        cv2.imwrite(path, frame)
        currentFrame += 1

    # When everything done, release the capture
    print('vid to jpg done...')
    cap.release()
    cv2.destroyAllWindows()
    return data


def makePencilJpg(data, dataOutPath, option):
    dataOut = []
    currentFrame = 0
    print('creating pencil jpgs....')
    for file in data:
        img = cv2.imread(file)

        grayscale, color = cv2.pencilSketch(img, sigma_s=50, sigma_r=0.07, shade_factor=0.04)

        path = './' + dataOutPath + '/frame' + str(currentFrame) + '.jpg'
        if option == 1:
            cv2.imwrite(path, grayscale)
        elif option == 2:
            cv2.imwrite(path, color)
        dataOut.append(path)
        if currentFrame % 30 == 0:
            print('pencil frame ' + str(currentFrame))
        currentFrame += 1
    return dataOut


def makeEdgeJpg(data, dataOutPath, t_lower, t_upper, L2Gradient, definition=7):
    currentFrame = 0
    print('creating edge jpgs....')
    dataOut = []

    for file in data:
        img = cv2.imread(file)

        imgOut = cv2.Canny(img, t_lower, t_upper, apertureSize=definition, L2gradient=L2Gradient)

        path = './' + dataOutPath + '/frame' + str(currentFrame) + '.jpg'
        cv2.imwrite(path, imgOut)
        dataOut.append(path)
        if currentFrame % 30 == 0:
            print('edge frame ' + str(currentFrame))
        currentFrame += 1
    return dataOut


def makeInvertJpg(data, dataOutPath):
    currentFrame = 0
    print('creating edge jpgs....')
    dataOut = []

    for file in data:
        img = cv2.imread(file)

        inverted = cv2.bitwise_not(img)

        path = './' + dataOutPath + '/frame' + str(currentFrame) + '.jpg'
        cv2.imwrite(path, inverted)
        dataOut.append(path)
        if currentFrame % 30 == 0:
            print('edge frame ' + str(currentFrame))
        currentFrame += 1
    return dataOut


def createVideo(dataOut):
    size = (0, 0)
    img_array = []
    print('creating video....')
    i = 0
    for file in dataOut:
        img = cv2.imread(file)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        if i % 30 == 0:
            print('frame ' + str(i))
        i += 1

    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print('video created')


def createDirs(dataPath,dataOutPath):
    try:
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)
        if not os.path.exists(dataOutPath):
            os.makedirs(dataOutPath)
    except OSError:
        print("Error: Couldn't create directories!")


def cleanUpDirs(dataPath, dataOutPath):
    try:
        shutil.rmtree(dataPath)
        shutil.rmtree(dataOutPath)
    except OSError:
        print("Error: Couldn't remove directories: " + dataPath + "/" + dataOutPath)
