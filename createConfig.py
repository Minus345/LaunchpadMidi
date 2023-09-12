import yaml


def createConfig():
    data = dict(
        outputLaunchaPad="MIDIOUT2 (LPMiniMK3 MIDI) 2",
        inputLaunchPad="MIDIIN2 (LPMiniMK3 MIDI) 1",
        outputToSoftware="midi 3",
        inputFromSoftware="midi 2",
        fader=dict(
            a="A",
            b="B",
            c="C",
            d="D",
            e="E",
            f="F",
            g="G",
            h="H"
        ),
        button=dict(
            a="Update GUI",
            b="B",
            c="C",
            d="D",
            e="E",
            f="F",
            g="G",
            h="H"
        ),
        rightbuttons=dict(
            a="Tab",
            b="B",
            c="C",
            d="D",
            e="E",
            f="Black",
            g="White",
            h="Strobe"
        )
    )
    with open('config.yml', 'w') as file:
        yaml.dump(data, file)
