print("please wait...")
import sys, time
from TPPFLUSH.tppflush import *
import pygame
from enum import IntEnum

done=False

#edit this to True to print the bytes that are sent.
print_bytes=False

pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

print("Number of joysticks: {}".format(joystick_count) )
for i in range(joystick_count):
        print("")
        joystick = pygame.joystick.Joystick(i)
        print("initting joystick {}".format(i))
        joystick.init()
        name = joystick.get_name()
        print(" Joystick name: {}".format(name))
        axes = joystick.get_numaxes()
        print(" Number of axes: {}".format(axes))
        buttons = joystick.get_numbuttons()
        print(" Number of buttons: {}".format(buttons))
        hats = joystick.get_numhats()
        print(" Number of hats: {}".format(hats))
        

#These variables are needed for the button asignment code to work. DO NOT mess with them.
button_list = {"A" :"","B" :"","X" :"","Y" :"","L" :"","R" :"","Start" :"","Select" :"","Home" :"","ZL" :"","ZR" :"","Dpad Up" :"","Dpad Down" :"","Dpad Left" :"","Dpad Right" :""}
axis_list = {"L" :"","R" :"","Stick Up" :"","Stick Left" :"","C Stick Up" :"","C Stick Left" :""}
button_reference = {"A" :"HIDButtons.A","B" :"HIDButtons.B","X" :"HIDButtons.X","Y" :"HIDButtons.Y","L" :"HIDButtons.L","R" :"HIDButtons.R","Start" :"HIDButtons.START","Select" :"HIDButtons.SELECT","Home" :"Special_Buttons.HOME","ZL" :"N3DS_Buttons.ZL","ZR" :"N3DS_Buttons.ZR","Dpad Up" :"HIDButtons.DPADUP","Dpad Down" :"HIDButtons.DPADDOWN","Dpad Left" :"HIDButtons.DPADLEFT","Dpad Right" :"HIDButtons.DPADRIGHT","null" :"0"}
binary_list = []
button_quantity = joystick.get_numbuttons()
button_count = 0
buttonMappingsString = "["

#ensures each button is used only once
def used_button_check(x):
    if x in button_list.values():
        return True
    else:
        return False

#ensures each axis is used only once
def used_axis_check(x):
    if x in axis_list.values():        
        return True
    else:
        return False

#Checks for pressed buttons to map them
def button_check(x):
    print("\nWhat button do you wish to use for " + x + "?\nPress any key on keyboard to Skip\n")
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and used_button_check(event.button) == False:
                print("Joystick {} button {} pressed.".format(event.joy,event.button))
                return event.button
            elif event.type == pygame.KEYDOWN:
                return "null"

#Checks for pressed axes (yes, that's the plural) to map them
def axis_check(x):
    print("\nWhat axis do you wish to use for " + x + "?\nPress any key on keyboard to Skip\n")
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION and abs(event.value) > 0.7 and used_axis_check(event.axis) == False:
                temp = event.axis
                print("Joystick {} Axis {} Value {}.".format(event.joy,event.axis,event.value))
                return temp
            elif event.type == pygame.KEYDOWN:
                return "null"
    return

for n in button_list:
    button_list[n] = button_check(n)

for n in axis_list:
    axis_list[n] = axis_check(n)

button_keys = list(button_list.keys())
button_values = list(button_list.values())

while button_count < button_quantity:
    if (button_count in button_values):
        position = button_values.index(button_count)
        binary_list.append(button_keys[position])
    else:
        binary_list.append("null")
    button_count += 1

for x in binary_list:
    buttonMappingsString += button_reference.setdefault(x)
    if x == binary_list[-1]:
        buttonMappingsString += "]"
    else:
        buttonMappingsString += ","

buttonMappings = eval(buttonMappingsString)

class KBDButtons(IntEnum):
        C_UP = pygame.K_w
        C_DOWN = pygame.K_s
        C_LEFT = pygame.K_a
        C_RIGHT = pygame.K_d

        DPADUP = pygame.K_UP
        DPADDOWN = pygame.K_DOWN
        DPADLEFT = pygame.K_LEFT
        DPADRIGHT = pygame.K_RIGHT

        A = pygame.K_j
        B = pygame.K_k
        X = pygame.K_u
        Y = pygame.K_i
        L = pygame.K_h
        R = pygame.K_l
        START = pygame.K_RETURN
        SELECT = pygame.K_BACKSPACE
        ZL = pygame.K_y
        ZR = pygame.K_o

        HOME = pygame.K_HOME
        POWER = pygame.K_END

if len(sys.argv) < 2:
	server = input("3DS IP >").strip()
else:
        server = sys.argv[1]
        
server=LumaInputServer(server)

#time.sleep(3)
#server.hid_press(HIDButtons.X) #to show it works
#server.send(print_bytes)

screen = pygame.display.set_mode((320, 240))
#screen.fill((0,0,0))
TCImg="images/home.jpg"
try:
        img=pygame.image.load(TCImg)
except pygame.error:
        print("Could not find touch screen file, using default black screen")
        screen.fill((0,0,0))
else:
        screen.blit(img,(0,0))
        pygame.display.flip()
pygame.display.set_caption('touchscreen')
pygame.display.update()




print("ready!")
while done==False:
        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True

                #Touchscreen input
                if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        server.touch(pos[0], pos[1])
                        #print("THSC: ",pos[0],",",pos[1])
                        server.send(print_bytes)
                elif event.type == pygame.MOUSEBUTTONUP:
                        server.clear_touch()
                        server.send(print_bytes)

                #Keyboard Mappings
                elif event.type == pygame.KEYDOWN:
                        if event.key == KBDButtons.C_UP:
                                server.circle_pad_set(CPAD_Commands.CPADUP)
                                #print("C_UP")
                        if event.key == KBDButtons.C_LEFT:
                                server.circle_pad_set(CPAD_Commands.CPADLEFT)
                                #print("C_LEFT")
                        if event.key == KBDButtons.C_DOWN:
                                server.circle_pad_set(CPAD_Commands.CPADDOWN)
                                #print("C_DOWN")
                        if event.key == KBDButtons.C_RIGHT:
                                server.circle_pad_set(CPAD_Commands.CPADRIGHT)
                                #print("C_RIGHT")
                              
                        for button in KBDButtons:
                            if event.key == button:
                                if hasattr(HIDButtons, button.name): #KBDButtons.B -> HIDButtons.B
                                        server.press(HIDButtons[button.name])
                                        #print(button.name)

                        if event.key == KBDButtons.ZL: #ZL
                                server.n3ds_zlzr_press(N3DS_Buttons.ZL)
                                #print("ZL")
                        if event.key == KBDButtons.ZR: #ZR
                                server.n3ds_zlzr_press(N3DS_Buttons.ZR)
                                #print("ZR")
                        if event.key == KBDButtons.HOME: #Home
                                server.special_press(Special_Buttons.HOME)
                                #print("HOME")
                        if event.key == KBDButtons.POWER: #Power
                                server.special_press(Special_Buttons.POWER)
                                #print("POWER")
                                
                        if event.key == pygame.K_ESCAPE:
                                server.clear_everything()
                                done = True
                        server.send(print_bytes)
                        
                elif event.type == pygame.KEYUP:
                        if event.key == KBDButtons.C_UP:
                                server.circle_pad_coords[1] = 0
                        if event.key == KBDButtons.C_LEFT:
                                server.circle_pad_coords[0] = 0
                        if event.key == KBDButtons.C_DOWN:
                                server.circle_pad_coords[1] = 0
                        if event.key == KBDButtons.C_RIGHT:
                                server.circle_pad_coords[0] = 0
                        
                        for button in KBDButtons:
                            if event.key == button:
                                if hasattr(HIDButtons, button.name): #KBDButtons.B -> HIDButtons.B
                                        server.unpress(HIDButtons[button.name])

                        if event.key == KBDButtons.ZL: #Zl
                                server.n3ds_zlzr_unpress(N3DS_Buttons.ZL)
                        if event.key == KBDButtons.ZR: #Zr
                                server.n3ds_zlzr_unpress(N3DS_Buttons.ZR)
                        if event.key == KBDButtons.HOME: #Home
                                server.special_unpress(Special_Buttons.HOME)
                        if event.key == KBDButtons.POWER: #Power
                                server.special_unpress(Special_Buttons.POWER)

                        server.send(print_bytes)


                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                        print("Joystick {} button {} pressed.".format(event.joy,event.button))
                        server.press(buttonMappings[event.button])
                        server.send(print_bytes)
                if event.type == pygame.JOYBUTTONUP:
                        print("Joystick {} button {} released.".format(event.joy,event.button))
                        server.unpress(buttonMappings[event.button])
                        server.send(print_bytes)
                if event.type == pygame.JOYAXISMOTION:
                        #if event.axis in range(2,3): print("Joystick {} axis {} moved to {}.".format(event.joy,event.axis, event.value))
                        if event.axis == axis_list["Stick Left"]: server.circle_pad_coords[0] = int(32767*event.value) #ls x
                        if event.axis == axis_list["Stick Up"]: server.circle_pad_coords[1] = int(-32767*event.value) #ls y
                        if event.axis == axis_list["L"]: #l trig
                                if event.value >= 0: server.press(HIDButtons.L) #Zero is a half-press on GC Controller
                                else: server.unpress(HIDButtons.L)
                        if event.axis == axis_list["R"]: #r trig
                                if event.value >= 0: server.press(HIDButtons.R)
                                else: server.unpress(HIDButtons.R)
                        if event.axis == axis_list["C Stick Left"]: server.cstick_coords[0] = int(32767*event.value)  #rs y
                        if event.axis == axis_list["C Stick Up"]: server.cstick_coords[1] = int(-32767*event.value) #rs x
                        server.send(print_bytes)
                        
                #server.send(print_bytes) #GCC Axes - 0:LStickX 1:LStickY 4:CStickY 5:CStickX 2:LTrig 3:RTrig
print("clearing everything...")
server.clear_everything()
for i in range(1,50):
        server.send(print_bytes)
pygame.quit()
        
        

