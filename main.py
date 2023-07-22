import mido


def updateFirstColum(colum):
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][0], velocity=button[colum][0], channel=2))
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][1], velocity=button[colum][1], channel=0))

    outputLounchPad.send(mido.Message('note_on', note=notes[colum][3], velocity=faders[colum][0], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][4], velocity=faders[colum][1], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][5], velocity=faders[colum][2], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][6], velocity=faders[colum][3], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=notes[colum][7], velocity=faders[colum][4], channel=0))


def updateFirstColumWithPercentage(percentage, flash, switchOn, colum):
    channel = colum;
    if switchOn[channel]:
        button[channel][0] = 45
        color = 9
        outputToSoftware.send(mido.Message('note_on', note=colum + 1, velocity=127, channel=0))
    else:
        button[channel][0] = 0
        color = 5
        outputToSoftware.send(mido.Message('note_off', note=colum + 1, velocity=127, channel=0))

    match percentage[channel]:
        case 0:
            faders[channel][4] = 0
            faders[channel][3] = 0
            faders[channel][2] = 0
            faders[channel][1] = 0
            faders[channel][0] = color
        case 25:
            faders[channel][4] = 0
            faders[channel][3] = 0
            faders[channel][2] = 0
            faders[channel][1] = color
            faders[channel][0] = color
        case 50:
            faders[channel][4] = 0
            faders[channel][3] = 0
            faders[channel][2] = color
            faders[channel][1] = color
            faders[channel][0] = color
        case 75:
            faders[channel][4] = 0
            faders[channel][3] = color
            faders[channel][2] = color
            faders[channel][1] = color
            faders[channel][0] = color
        case 100:
            faders[channel][4] = color
            faders[channel][3] = color
            faders[channel][2] = color
            faders[channel][1] = color
            faders[channel][0] = color

    if flash[channel]:
        button[channel][1] = 21
    else:
        button[channel][1] = 45
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


if __name__ == '__main__':
    print("Starting")
    print(mido.get_output_names())  # To list the output ports
    print(mido.get_input_names())

    outputLounchPad = mido.open_output('MIDIOUT2 (LPMiniMK3 MIDI) 3')
    inportLounchPad = mido.open_input('MIDIIN2 (LPMiniMK3 MIDI) 2')
    outputToSoftware = mido.open_output('midi 1')
    inputFromSoftware = mido.open_input('midi 0')

    faders = [[50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50],
              [50, 50, 50, 50, 50], [50, 50, 50, 50, 50]]
    button = [[0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45], [0, 45]]
    notes = [[11, 21, 31, 41, 51, 61, 71, 81], [12, 22, 32, 42, 52, 62, 72, 82], [13, 23, 33, 43, 53, 63, 73, 83],
             [14, 24, 34, 44, 54, 64, 74, 84], [15, 25, 35, 45, 55, 65, 75, 85], [16, 26, 36, 46, 56, 66, 76, 86],
             [17, 27, 37, 47, 57, 67, 77, 87], [18, 28, 38, 48, 58, 68, 78, 88]]
    for x in range(8):
        updateFirstColum(x)

    percentage = [0, 0, 0, 0, 0, 0, 0, 0]
    flash = [False, False, False, False, False, False, False, False]
    switchOn = [False, False, False, False, False, False, False, False]
    savePercentage = [0, 0, 0, 0, 0, 0, 0, 0]

    while True:
        msg = inportLounchPad.receive()

        for colum in range(8):

            if msg == mido.Message("note_on", note=notes[colum][0], velocity=127, channel=0):
                if not switchOn[colum]:
                    switchOn[colum] = True
                else:
                    switchOn[colum] = False
            if msg == mido.Message("note_on", note=notes[colum][1], velocity=127, channel=0):  # flash
                savePercentage[colum] = percentage[colum]
                percentage[colum] = 100
                flash[colum] = True
            if msg == mido.Message("note_on", note=notes[colum][1], velocity=0, channel=0):
                if flash[colum]:
                    percentage[colum] = savePercentage[colum]
                    flash[colum] = False

            if msg == mido.Message("note_on", note=notes[colum][3], velocity=127, channel=0):
                percentage[colum] = 0
            if msg == mido.Message("note_on", note=notes[colum][4], velocity=127, channel=0):
                percentage[colum] = 25
            if msg == mido.Message("note_on", note=notes[colum][5], velocity=127, channel=0):
                percentage[colum] = 50
            if msg == mido.Message("note_on", note=notes[colum][6], velocity=127, channel=0):
                percentage[colum] = 75
            if msg == mido.Message("note_on", note=notes[colum][7], velocity=127, channel=0):
                percentage[colum] = 100

            updateFirstColumWithPercentage(percentage, flash, switchOn, colum)
            sendMidiFirstColum(percentage, colum)
