import mss
import numpy
import cv2
import time
import torch
import keyboard
from pyautogui import *
import pyautogui
import random
import processing

def outputImg():
    filename = "screen.png"
    filepath = os.path.join("Variables", filename)
    sct.shot(output=filepath)

captureInProgress = False
bubbleOnScreen = False

global screenHeight
global screenWidth
screenHeight = 1080
screenWidth = 1920

#Versions:
#best-pre v.1.pt
#best.pt

model = torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/username/Desktop/FishingSim/weights/best-pre v.1.pt')
with mss.mss() as sct:
    # monitor = {'top':0, 'left': 0, 'width': screenWidth, 'height': screenHeight} # Full Screen
    # monitor = {'top': int(screenHeight*0.15), 'left': int(screenWidth*0.15), 'width': int(screenWidth*0.7), 'height': int(screenHeight*0.7)} # Medium Cutout
    monitor = {'top': int(screenHeight*0.075), 'left': int(screenWidth*0.15), 'width': int(screenWidth*0.7), 'height': int(screenHeight*0.9)} # Medium Cutout - High
    # monitor = {'top': int(screenHeight*0.25), 'left': int(screenWidth*0.3), 'width': int(screenWidth*0.4), 'height': int(screenHeight*0.45} # Smaller Cutout
    # monitor = {'top': int(screenHeight*0.075), 'left': int(screenWidth*0.3), 'width': int(screenWidth*0.4), 'height': int(screenHeight*0.9)} # Smaller Cutout - High

captureInProgress = True
start_time = time.time()

while captureInProgress:
    t = time.time()
    img = numpy.array(sct.grab(monitor))
    results = model(img)
    rl = results.xyxy[0].tolist()

    confidence_threshold = 0.50
    rl = [obj for obj in rl if obj[4] > confidence_threshold]
    # print(rl)
    # print('fps: {}'.format(1 / (time.time() - t)))

    processed_img = numpy.squeeze(results.render())
    cv2.putText(processed_img, "Fish Caught: " + str(processing.caught) + "/" + str(processing.maxfish), (10, 30), cv2.FONT_ITALIC, 1, (0,0,0), 3, cv2.LINE_AA)
    cv2.putText(processed_img, "Times Sold: " + str(processing.TimesSold), (10, 70), cv2.FONT_ITALIC, 1, (0, 0, 0), 3,cv2.LINE_AA)
    cv2.putText(processed_img, "Errors: " + str(processing.errors), (10, 110), cv2.FONT_ITALIC, 1, (0, 0, 0), 3,cv2.LINE_AA)

    cv2.imshow('capture', processed_img)

    if len(rl) > 0 or (time.time() - start_time) > 25:
        start_time = time.time()
        if len(rl) > 0 :
            bubbleOnScreen = True
            #print(bubbleOnScreen)
            processing.process()
        else:
            processing.errors = processing.errors + 1
            print("Time rerun!")
            bubbleOnScreen = True
            # print(bubbleOnScreen)
            processing.refresh()
    if not len(rl) > 0:
        bubbleOnScreen = False

    cv2.waitKey(1)

    if keyboard.is_pressed('q'):
        print("Stopped inside loop - capture")
        break

print("Stopped outside loop - capture")
processing.stop()
