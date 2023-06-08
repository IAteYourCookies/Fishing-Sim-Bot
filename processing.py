import numpy
import cv2
import time
import keyboard
import os
import torch
from pynput.mouse import Controller
from pyautogui import *
from pyautogui import press
import pyautogui
import random
import subprocess

processing = True

caught = 0
maxfish = 190
TimesSold = 0

errors = 0

AutoSell = True
ThirdPerson = False

def process():
    click()
    global caught
    global maxfish
    start_time = time.time()
    while processing:
        current_time = time.time()
        if pyautogui.pixelMatchesColor(1059, 822, (83, 250, 83)) & pyautogui.pixelMatchesColor(809, 836, (251, 98, 76)) or current_time - start_time > 5:
            #print("Start loop!")
            while pyautogui.pixelMatchesColor(1059, 822, (83, 250, 83)) & pyautogui.pixelMatchesColor(809, 836,(251, 98, 76)) and not current_time - start_time > 10:
                if pyautogui.pixelMatchesColor(943, 810, (255, 255, 255)) & pyautogui.pixelMatchesColor(1059, 822, (83, 250, 83)) & pyautogui.pixelMatchesColor(809, 836, (251, 98, 76)) or current_time - start_time > 5:
                    #Alte detect Werte (Für Weiß): 881, 816
                    click()
            #print("End loop!", end="")
            print(" Fish Caught: ", end="")
            caught = caught + 1
            print(caught)
            time.sleep(1.5)
            #print("Recasted Fishingrod!")
            click()
            break

    if keyboard.is_pressed('q'):
        print("Stopped inside loop - processing")
        stop()

    if caught >= maxfish:
        if AutoSell == True:
            sell()
        else:
            stop()


def zoomOut():
    for i in range(0, 25):
        keyboard.press_and_release("o")
        time.sleep(0.1)

def zoomIn():
    for i in range(0, 20):
        keyboard.press_and_release("i")
        time.sleep(0.05)

def sell():
    global errors
    global AutoSell
    global TimesSold
    global ThirdPerson
    mouse = Controller()
    if AutoSell == True:
        print("Selling initiated! ", end="")
        keyboard.press_and_release("1")
        if pyautogui.pixelMatchesColor(948, 1009, (255, 255, 255)):
            print("... Stopped Sell! No Fish Caught!")
            errors = errors + 1
            click(1807, 86)
        else:
            global caught
            if ThirdPerson:
                subprocess.call(["C:/Users/username/Desktop/scripts/(Zoom out) Fishing Sim v1.1 - 12 sec.exe"])
            else:
                mouse.scroll(0, -35)
                # zoomOut()
                subprocess.call(["C:/Users/username/Desktop/scripts/Fishing Sim v1.3 - 20 sec.exe"])
            caught = 0
            TimesSold = TimesSold + 1
            clear()
            print(" Successfully sold fish! SellNr: ", end="")
            print(TimesSold)
            # refresh()
            errors = errors - 1
    else:
        print("Sell is False!")

def refresh():
    #click 1386, 409 for close backpack
    #Click 1418, 389 for close sell

    for i in range (0, 2):
        keyboard.press_and_release("3")
        time.sleep(0.25)
        keyboard.press_and_release("1")
        time.sleep(0.25)
    keyboard.press_and_release("3")
    time.sleep(1)
    keyboard.press_and_release("1")
    time.sleep(0.75)
    click()

def clear():
    print("\033[H\033[3J", end="")

def stop():
    print("Stopping")
    global processing
    processing = False
    cv2.destroyAllWindows()
    print("Times Sold: ",end="")
    print(TimesSold)
    print("Errors: ", end="")
    print(errors)
    exit()

if __name__ == "__main__":
    print("Processing Initiated!")

    #process()
    time.sleep(1)
    sell()
