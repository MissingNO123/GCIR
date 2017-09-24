# GCIR - Gamecube Controller Input Redirect
Fully re-mappable GCN controller to Luma InputRedirect.
Also supports remappable keyboard inputs.

Technically supports any DInput device (i.e. Windows joystick), or any device that PyGame supports (i.e. XBox 360 Controller), but is currently mapped for a Gamecube Controller via a USB adapter.

To remap controls, just edit the buttonMappings array or KBDButtons class in gamepad.py (or two.py if using multiple systems). 

The buttonMappings array is a list of every button on your controller in order from 0 mapped to a 3DS button, so if you want button 0 on your controller to be button A on the 3DS, put `HIDButtons.A` first in the list. 
Likewise, if you want button 3 to be A, put `HIDButtons.A` as the 4th item in the list. 
If you want a high-numbered button (like the XBox 360 Guide button, 15 on some OSes) to be bound to a 3DS button, just add empty list entries (zero) in between the last button map and the one you want. 

To remap joystick axes (if your controller for some reason uses different ones) find `pygame.JOYAXISMOTION` with ctrl+f and change the joystick axis indices (`event.axis == 0` etc). 
~~(I will fix that later)~~
