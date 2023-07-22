import mido


def updateFirstColum():
    outputLounchPad.send(mido.Message('note_on', note=11, velocity=button1[0], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=21, velocity=button1[1], channel=0))

    outputLounchPad.send(mido.Message('note_on', note=41, velocity=faders1[0], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=51, velocity=faders1[1], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=61, velocity=faders1[2], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=71, velocity=faders1[3], channel=0))
    outputLounchPad.send(mido.Message('note_on', note=81, velocity=faders1[4], channel=0))


def updateFirstColumWithPercentage(percentage, flash):
    match percentage:
        case 0:
            faders1[4] = 0
            faders1[3] = 0
            faders1[2] = 0
            faders1[1] = 0
            faders1[0] = 9
        case 25:
            faders1[4] = 0
            faders1[3] = 0
            faders1[2] = 0
            faders1[1] = 9
            faders1[0] = 9
        case 50:
            faders1[4] = 0
            faders1[3] = 0
            faders1[2] = 9
            faders1[1] = 9
            faders1[0] = 9
        case 75:
            faders1[4] = 0
            faders1[3] = 9
            faders1[2] = 9
            faders1[1] = 9
            faders1[0] = 9
        case 100:
            faders1[4] = 9
            faders1[3] = 9
            faders1[2] = 9
            faders1[1] = 9
            faders1[0] = 9

    if flash:
        button1[1] = 21
    else:
        button1[1] = 45
    updateFirstColum()


def sendMidiFirstColum(percentage):
    match percentage:
        case 0:
            outputToSoftware.send(mido.Message('control_change', channel=0, control=1, value=0))
        case 25:
            outputToSoftware.send(mido.Message('control_change', channel=0, control=1, value=16))
        case 50:
            outputToSoftware.send(mido.Message('control_change', channel=0, control=1, value=32))
        case 75:
            outputToSoftware.send(mido.Message('control_change', channel=0, control=1, value=48))
        case 100:
            outputToSoftware.send(mido.Message('control_change', channel=0, control=1, value=64))


if __name__ == '__main__':
    print("Starting")
    print(mido.get_output_names())  # To list the output ports
    print(mido.get_input_names())

    outputLounchPad = mido.open_output('MIDIOUT2 (LPMiniMK3 MIDI) 3')
    inportLounchPad = mido.open_input('MIDIIN2 (LPMiniMK3 MIDI) 2')
    outputToSoftware = mido.open_output('midi 1')
    inputFromSoftware = mido.open_input('midi 0')

    faders1 = [0, 0, 0, 0, 0]
    button1 = [45, 45]
    updateFirstColum()

    percentage = 0
    flash = False

    while True:
        msg = inportLounchPad.receive()
        if msg == mido.Message("note_on", note=21, velocity=127, channel=0):  # flash
            savePercentage = percentage
            percentage = 100
            flash = True
        else:
            if flash:
                percentage = savePercentage
                flash = False

        if msg == mido.Message("note_on", note=41, velocity=127, channel=0):
            percentage = 0
        if msg == mido.Message("note_on", note=51, velocity=127, channel=0):
            percentage = 25
        if msg == mido.Message("note_on", note=61, velocity=127, channel=0):
            percentage = 50
        if msg == mido.Message("note_on", note=71, velocity=127, channel=0):
            percentage = 75
        if msg == mido.Message("note_on", note=81, velocity=127, channel=0):
            percentage = 100

        updateFirstColumWithPercentage(percentage, flash)
        sendMidiFirstColum(percentage)
        print(msg)
        print(percentage)

        # print(inputFromSoftware.receive())
