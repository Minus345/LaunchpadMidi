import os
from threading import Thread

import mido
import yaml
import gui
from createConfig import createConfig

global outputLaunchaPad, inputLaunchPad, outputToSoftware, inputFromSoftware, faders, button, notes, percentage, flash, switchOn, savePercentage, faderColour


def updateFirstColum(colum):
    # notes = button
    # velocity = colour
    # channel = static, flashing, pulsing

    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][0], velocity=button[colum][0], channel=2))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][1], velocity=button[colum][1], channel=0))

    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][3], velocity=faders[colum][0], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][4], velocity=faders[colum][1], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][5], velocity=faders[colum][2], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][6], velocity=faders[colum][3], channel=0))
    outputLaunchaPad.send(mido.Message('note_on', note=notes[colum][7], velocity=faders[colum][4], channel=0))


def updateFirstColumWithPercentage(percentage, flash, switchOn, colum):
    if switchOn[colum]:
        button[colum][0] = 45
        color = 9
        outputToSoftware.send(mido.Message('note_on', note=colum + 1, velocity=127, channel=0))
    else:
        button[colum][0] = 0
        color = faderColour[colum]
        outputToSoftware.send(mido.Message('note_off', note=colum + 1, velocity=127, channel=0))

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
        button[colum][1] = 21
    else:
        button[colum][1] = 45
    updateFirstColum(colum)


def sendMidiFirstColum(percentage, colum):
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


def loop(message):
    # side Buttons
    control = [19, 29, 39, 49, 59, 69, 79, 89]
    for x in range(len(control)):
        if message == mido.Message("control_change", channel=0, control=control[x], value=127):
            outputToSoftware.send(mido.Message('note_on', note=10 + x, velocity=127, channel=0))
            return
        if message == mido.Message("control_change", channel=0, control=control[x], value=0):
            outputToSoftware.send(mido.Message('note_off', note=10 + x, velocity=127, channel=0))
            return
    # faders
    for colum in range(8):
        if message == mido.Message("note_on", note=notes[colum][0], velocity=127, channel=0):
            if not switchOn[colum]:
                switchOn[colum] = True
            else:
                switchOn[colum] = False
        if message == mido.Message("note_on", note=notes[colum][1], velocity=127, channel=0):  # flash
            savePercentage[colum] = percentage[colum]
            percentage[colum] = 100
            flash[colum] = True
        if message == mido.Message("note_on", note=notes[colum][1], velocity=0, channel=0):
            if flash[colum]:
                percentage[colum] = savePercentage[colum]
                flash[colum] = False

        if message == mido.Message("note_on", note=notes[colum][3], velocity=127, channel=0):
            percentage[colum] = 0
        if message == mido.Message("note_on", note=notes[colum][4], velocity=127, channel=0):
            percentage[colum] = 25
        if message == mido.Message("note_on", note=notes[colum][5], velocity=127, channel=0):
            percentage[colum] = 50
        if message == mido.Message("note_on", note=notes[colum][6], velocity=127, channel=0):
            percentage[colum] = 75
        if message == mido.Message("note_on", note=notes[colum][7], velocity=127, channel=0):
            percentage[colum] = 100

        updateFirstColumWithPercentage(percentage, flash, switchOn, colum)
        sendMidiFirstColum(percentage, colum)


def startMidi():
    print("Output:")
    print(mido.get_output_names())
    print("Input:")
    print(mido.get_input_names())

    with open('config.yml', 'r') as file:
        configFile = yaml.safe_load(file)

    print("starting Midi")
    global outputLaunchaPad, inputLaunchPad, outputToSoftware, inputFromSoftware, faders, button, notes, percentage, flash, switchOn, savePercentage

    outputLaunchaPad = mido.open_output(configFile['outputLaunchaPad'])
    inputLaunchPad = mido.open_input(configFile['inputLaunchPad'])
    outputToSoftware = mido.open_output(configFile['outputToSoftware'])
    inputFromSoftware = mido.open_input(configFile['inputFromSoftware'])

    faders = [[50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50]]
    button = [[0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45]]
    notes = [[11, 21, 31, 41, 51, 61, 71, 81], [12, 22, 32, 42, 52, 62, 72, 82], [13, 23, 33, 43, 53, 63, 73, 83],
             [14, 24, 34, 44, 54, 64, 74, 84], [15, 25, 35, 45, 55, 65, 75, 85], [16, 26, 36, 46, 56, 66, 76, 86],
             [17, 27, 37, 47, 57, 67, 77, 87], [18, 28, 38, 48, 58, 68, 78, 88]]

    percentage = [0, 0, 0, 0, 0, 0, 0, 0]
    flash = [False, False, False, False, False, False, False, False]
    switchOn = [False, False, False, False, False, False, False, False]
    savePercentage = [0, 0, 0, 0, 0, 0, 0, 0]

    global faderColour
    faderColour = [1, 2, 3, 4, 5, 6, 7, 8]
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h"]

    for i in range(8):
        match configFile['fadercolour1'][alpha[i]]:
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

    print(faderColour)

    for x in range(8):
        updateFirstColum(x)

    while True:
        msg = inputLaunchPad.receive()
        # print(msg)

        if msg:
            loop(msg)


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


if __name__ == '__main__':
    gui.start()
