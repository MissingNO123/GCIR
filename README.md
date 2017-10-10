# GCIR - Gamecube Controller Input Redirect
Fully re-mappable GCN controller to Luma InputRedirect.
Also supports remappable keyboard inputs.

## Features
  - Supports any DInput device (anything your OS sees as a joystick)
  - Also supports Xinput (Xbox 360/One controller)
  - Supports using the keyboard
  - Supports putting a picture over the touch screen window
  - Fully re-mappable controls

## Configuration
To re-map buttons, edit the buttonMappings dict (for controllers) or KBDButtons class (for the keyboard) in gamepad.py. 

To add a button mapping to the buttonMappings dict, type the button ID followed by the 3DS button you want it to be mapped to. For example, if you wanted button `0` to be mapped to `HIDButtons.A`, add an entry to `buttonMappings` like so:

```0: HIDButtons.A``` 

Likewise, if you want button 3 to be A, put `3: HIDButtons.A` in the list instead. 

Button IDs can be found in Windows Game Controller settings (Start > Run... > joy.cpl)

To remap joystick axes (if your controller for some reason uses different ones) find `pygame.JOYAXISMOTION` with ctrl+f and change the joystick axis indices (`event.axis == 0` etc). 
~~(I will fix that later)~~

## Requirements
Requires Python 3.6 or higher, and the PyGame library.

Python can be downloaded from [its website](https://python.org)

PyGame can be installed with the following command:

```bash
pip install pygame
```

or, if you have multiple versions of Python installed:

```bash
python -m pip install pygame
```

You may have to substitute `python` for either `python3` or `python3.6` depending on how you installed it

If neither of those work you may have to type the full path to the python executable (i.e. `C:\Python36\python.exe`)

## Cloning
When cloning this repository, make sure to use `--recursive` to download the necessary submodule.
