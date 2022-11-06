import os
import sys

from video import vidToJpg, makeEdgeJpg, createVideo, makePencilJpg, makeInvertJpg, cleanUpDirs, createDirs

# data and dataOut contain paths of jpgs produced
data = []
dataOut = []
dataPath = "data"
dataOutPath = "dataOut"


def devMode(x): return x


####################
#       MAIN       #
####################
# sys.argv[1] gets command line parameter
# example: python main.py name_of_the_video.mp4


if devMode(0):
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
    penciloption = 2  # 1=gray 2=color

    createDirs(dataPath, dataOutPath)
    data = vidToJpg(fileName, dataPath)
    dataOut = makeEdgeJpg(data, dataOutPath, lower, upper, L2Gradient, definition)
    # dataOut = makePencilJpg(data, dataOutPath, penciloption)
    # dataOut = makeInvertJpg(data, dataOutPath)
    createVideo(dataOut)
    cleanUpDirs(dataPath, dataOutPath)
else:
    print("Input Video" + fileName + " not found")
