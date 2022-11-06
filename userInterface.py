import shutil
import cv2
import os



def initUserInterface():
    print('Video_Filters_Converter_App')
    print('-' * 10)
    print('Default directories are: data and dataOut')
    print('Do you want to change them? (yes/no)')
    if input() == "yes":
        data = input('Name for non converted images')
        dataOutPath = input('Name for converted images')
    else:
        print('Skipping renaming...')
        print('Choose filter option: \n1.Edge \n2.Pencil, \n3.Invert')
        match int(input()):
            case 1:
                while True:
                    try:
                        definition = int(input('definition: '))  # odd between 3 and 7 including
                        L2Gradient = int(input('L2Gradient: '))  # Boolean L2Gradient is  abs(gradient_x) + abs(gradient_y)
                        lower = int(input('lower: '))  # Lower Threshold
                        upper = int(input('upper: '))  # Upper threshold

                    except ValueError:
                        print("Not an integer! Please enter an integer.")
                    except AssertionError:
                        print("Please enter an integer between 1 and 10")
                    else:
                        break

                print('Edge')
            case 2:
                print('Pencil')
            case 3:
                print('Invert')
            case _:
                print('Choose correct option')
