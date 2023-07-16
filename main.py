
import mido

if __name__ == '__main__':
    print("Starting")
    print(mido.get_output_names())  # To list the output ports
    print(mido.get_input_names())

    output = mido.open_output('MIDIOUT2 (LPMiniMK3 MIDI) 2')
    inport = mido.open_input('MIDIIN2 (LPMiniMK3 MIDI) 1')

    output.send(mido.Message('note_on', note=11, velocity=45, channel=0))
    output.send(mido.Message('note_on', note=12, velocity=45, channel=1))
    output.send(mido.Message('note_on', note=13, velocity=45, channel=2))

    while True:
        msg = inport.receive()
        print(msg)
