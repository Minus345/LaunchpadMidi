import os
from threading import Thread
from queue import Queue
import mido
import yaml
import gui
from createConfig import createConfig

global outputLaunchaPad, inputLaunchPad, outputToSoftware, inputFromSoftware, faders, flashButton, notes, percentage, flash, switchOn, savePercentage, faderColour, queue


def checkStart():
    # create config
    path = './config.yml'
    check_file = os.path.isfile(path)
    if check_file == True:
        print("config loading")
    else:
        print("creating config file")
        createConfig()
        print("Output:")
        print(mido.get_output_names())
        print("Input:")
        print(mido.get_input_names())
        exit(101)


def updateLightingInColum(colum):
    # notes = button
    # velocity = colour
    # channel = static, flashing, pulsing
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][1], velocity=flashButton[colum][0], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][0], velocity=0, channel=0))

    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][2], velocity=faders[colum][0], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][3], velocity=faders[colum][1], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][4], velocity=faders[colum][2], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][5], velocity=faders[colum][3], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][6], velocity=faders[colum][4], channel=0))


def updateColumWithPercentage(percentage, flash, colum):
    color = faderColour[colum]
    match percentage[colum]:
        case 0:
            faders[colum][4] = 0
            faders[colum][3] = 0
            faders[colum][2] = 0
            faders[colum][1] = 0
            faders[colum][0] = color
        case 25:
            faders[colum][4] = 0
            faders[colum][3] = 0
            faders[colum][2] = 0
            faders[colum][1] = color
            faders[colum][0] = color
        case 50:
            faders[colum][4] = 0
            faders[colum][3] = 0
            faders[colum][2] = color
            faders[colum][1] = color
            faders[colum][0] = color
        case 75:
            faders[colum][4] = 0
            faders[colum][3] = color
            faders[colum][2] = color
            faders[colum][1] = color
            faders[colum][0] = color
        case 100:
            faders[colum][4] = color
            faders[colum][3] = color
            faders[colum][2] = color
            faders[colum][1] = color
            faders[colum][0] = color

    if flash[colum]:
        flashButton[colum][0] = 21
    else:
        flashButton[colum][0] = 45


def sendMidiToSoftware(percentage, colum):
    match percentage[colum]:
        case 0:
            outputToSoftware.send(mido.Message('control_change', channel=colum, control=1, value=0))
        case 25:
            outputToSoftware.send(mido.Message('control_change', channel=colum, control=1, value=16))
        case 50:
            outputToSoftware.send(mido.Message('control_change', channel=colum, control=1, value=32))
        case 75:
            outputToSoftware.send(mido.Message('control_change', channel=colum, control=1, value=48))
        case 100:
            outputToSoftware.send(mido.Message('control_change', channel=colum, control=1, value=64))


def getButtons(message, y):
    if message == mido.Message("note_on", note=notes[y][1], velocity=127, channel=0):  # flash
        savePercentage[y] = percentage[y]
        percentage[y] = 100
        flash[y] = True

    if message == mido.Message("note_on", note=notes[y][1], velocity=0, channel=0):  # flash
        if flash[y]:
            percentage[y] = savePercentage[y]
            flash[y] = False

    if message == mido.Message("note_on", note=notes[y][2], velocity=127, channel=0):
        percentage[y] = 0
    if message == mido.Message("note_on", note=notes[y][3], velocity=127, channel=0):
        percentage[y] = 25
    if message == mido.Message("note_on", note=notes[y][4], velocity=127, channel=0):
        percentage[y] = 50
    if message == mido.Message("note_on", note=notes[y][5], velocity=127, channel=0):
        percentage[y] = 75
    if message == mido.Message("note_on", note=notes[y][6], velocity=127, channel=0):
        percentage[y] = 100

    updateColumWithPercentage(percentage, flash, y)
    updateLightingInColum(y)
    sendMidiToSoftware(percentage, y)


def loop(message):
    # print(message)
    # side Buttons
    control = [19, 29, 39, 49, 59, 69, 79, 89]
    for x in range(len(control)):
        if message == mido.Message("control_change", channel=0, control=control[x], value=127):
            outputToSoftware.send(mido.Message('note_on', note=10 + x, velocity=127, channel=0))
            outputLaunchaPad.send(mido.Message('control_change', channel=0, control=control[x], value=6))
            return
        if message == mido.Message("control_change", channel=0, control=control[x], value=0):
            outputToSoftware.send(mido.Message('note_off', note=10 + x, velocity=127, channel=0))
            outputLaunchaPad.send(mido.Message('control_change', channel=0, control=control[x], value=1))
            return

    # bottom buttons
    bottomButtons = [11, 12, 13, 14, 15, 16, 17, 18]
    for x in range(len(bottomButtons)):
        if message == mido.Message("note_on", note=bottomButtons[x], velocity=127, channel=0):
            outputToSoftware.send(mido.Message('note_on', note=x + 1, velocity=127, channel=0))
            outputLaunchaPad.send(mido.Message('note_on', note=bottomButtons[x], velocity=6, channel=0))
            return
        if message == mido.Message("note_on", note=bottomButtons[x], velocity=0, channel=0):
            outputToSoftware.send(mido.Message('note_off', note=x + 1, velocity=127, channel=0))
            outputLaunchaPad.send(mido.Message('note_on', note=bottomButtons[x], velocity=1, channel=0))
            return

    # check wich channel is pressed:
    intensity = ["not used", "flash", "0", "25", "50", "75", "100"]
    for x in range(7):  # x is colum  y is row y: 0: toggle 1: flash 2: not used 3:0% 4:25% 5:50% 6:75% 7:100%
        for y in range(8):
            if message == mido.Message("note_on", note=notes[y][x], velocity=127, channel=0) or message == mido.Message(
                    "note_on", note=notes[y][x], velocity=0, channel=0):
                # print("colum: ", y, "row: ", intensity[x], message)
                getButtons(message, y)


def updateFaderColour():
    with open('config.yml', 'r') as file:
        configFile = yaml.safe_load(file)

    global faderColour
    faderColour = [1, 2, 3, 4, 5, 6, 7, 8]
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h"]

    for i in range(8):
        match configFile['fadercolour'][alpha[i]]:
            case 'white':
                faderColour[i] = 3
            case 'red':
                faderColour[i] = 5
            case 'orange':
                faderColour[i] = 10
            case 'yellow':
                faderColour[i] = 13
            case 'green':
                faderColour[i] = 22
            case 'blue':
                faderColour[i] = 45
            case 'pink':
                faderColour[i] = 53
            case _:
                faderColour[i] = 2


def startMidi(q):
    global queue
    queue = q
    print("Output:")
    print(mido.get_output_names())
    print("Input:")
    print(mido.get_input_names())

    with open('config.yml', 'r') as file:
        configFile = yaml.safe_load(file)

    print("starting Midi")
    global outputLaunchaPad, inputLaunchPad, outputToSoftware, inputFromSoftware, faders, flashButton, notes, percentage, flash, switchOn, savePercentage

    outputLaunchaPad = mido.open_output(configFile['outputLaunchaPad'])
    inputLaunchPad = mido.open_input(configFile['inputLaunchPad'])
    outputToSoftware = mido.open_output(configFile['outputToSoftware'])
    inputFromSoftware = mido.open_input(configFile['inputFromSoftware'])

    faders = [[50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50]]
    flashButton = [[45, 45], [45, 45], [45, 45], [45, 45], [45, 45], [45, 45], [45, 45], [45, 45]]
    notes = [[21, 31, 41, 51, 61, 71, 81], [22, 32, 42, 52, 62, 72, 82], [23, 33, 43, 53, 63, 73, 83],
             [24, 34, 44, 54, 64, 74, 84], [25, 35, 45, 55, 65, 75, 85], [26, 36, 46, 56, 66, 76, 86],
             [27, 37, 47, 57, 67, 77, 87], [28, 38, 48, 58, 68, 78, 88]]

    percentage = [0, 0, 0, 0, 0, 0, 0, 0]
    flash = [False, False, False, False, False, False, False, False]
    switchOn = [False, False, False, False, False, False, False, False]
    savePercentage = [0, 0, 0, 0, 0, 0, 0, 0]

    updateFaderColour()

    for x in range(8):
        updateLightingInColum(x)

    bottomButtons = [11, 12, 13, 14, 15, 16, 17, 18]
    for x in range(8):
        outputLaunchaPad.send(mido.Message('note_on', note=bottomButtons[x], velocity=1, channel=0))

    control = [19, 29, 39, 49, 59, 69, 79, 89]
    for x in range(8):
        outputLaunchaPad.send(mido.Message('control_change', channel=0, control=control[x], value=1))

    while True:
        if not queue.empty():
            data = queue.get_nowait()
            if data == "updateFader":
                updateFaderColour()

        msg = inputLaunchPad.receive()
        # print(msg)

        if msg:
            loop(msg)


if __name__ == '__main__':
    gui.start()
