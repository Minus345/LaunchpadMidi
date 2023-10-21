# LaunchpadMidi

Software wich translates midi notes form a novation Launchpad mini to DMX Joker Pro.
Features:
 - 8 Fader with 5 states (0%,25%,50%,75%,100%)
 - Flash button
 - 16 action buttons (just send midi note to software)
 - visual feedback
 - customisable colors (gui and launchpad)
## Get it up and running:

1. Download the zip File
2. Unpack it
3. Run the main.exe
4. The first time it will start and create a config file
5. Use loopmidi to create an virtual midi port to Dmx Joker Pro
6. Write the correct input and output midi ports in the config file
7. Set the launchpad in Programmer mode
8. Set the right midi port in the config file (a list of available ports is printed in the terminal at the start of the application)

## Launchpad in Programmer Mode:

1. Connect
2. Press Session
3. Press "Stop Solo Mute" Button

## Config file

- _button_: gui button names (don't change)
- _fader_: text for the faders
- _fadercolour_: changes the colour from the launchpad buttons   
  -> supported colours: "white" "red" "orange" "yellow" "green" "blue" "pink"

## Midi

- FADER
    - fader A -> Channel 1 Value 1
    - fader B -> Channel 2 Value 1
    - ...
- Flash Buttons
    - A (right first from the top) -> Channel 1 Value 17
    - B (under A) -> Channel 1 Value 16
    - ...