#A modified version of gamepad.py that allows you to connect any number of 3DSes to one InputRedirect session on PC

print("please wait...")
import sys, time
from TPPFLUSH.tppflush import *
import pygame

servers = []

done=False

#Change this to True to print bytes that are sent
print_bytes = False

buttonMappings = [
                HIDButtons.A,
                HIDButtons.B,
                HIDButtons.X,
                HIDButtons.Y,
                HIDButtons.SELECT, #Z
                HIDButtons.R,
                HIDButtons.L,
                HIDButtons.START,
                HIDButtons.DPADUP,
                HIDButtons.DPADDOWN,
                HIDButtons.DPADLEFT,
                HIDButtons.DPADRIGHT
        ]

class KBDButtons(int):
        C_UP = pygame.K_w
        C_DOWN = pygame.K_s
        C_LEFT = pygame.K_a
        C_RIGHT = pygame.K_d

        D_UP = pygame.K_UP
        D_DOWN = pygame.K_DOWN
        D_LEFT = pygame.K_LEFT
        D_RIGHT = pygame.K_RIGHT

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
        serverCount = int(input("How many 3DSes are you connecting? >"))
        for i in range(0,serverCount):
                tempstring = ("3DS IP #%s>" % str(i+1))
                servers.append(input(tempstring).strip())
else:
        servers.append(sys.argv[1])

for i in range(0,serverCount):       
        servers[i]=LumaInputServer(servers[i])

#time.sleep(3)
#server.hid_press(HIDButtons.X) #to show it works
#server.send()

pygame.init()
screen = pygame.display.set_mode((320, 240))
screen.fill((0,0,0))
pygame.display.set_caption('touchscreen')
pygame.display.update()

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

print("ready!")
while done==False:
        for event in pygame.event.get(): # User did something
                for i in range(0,serverCount):
                        if event.type == pygame.QUIT: # If user clicked close
                            done=True

                        #Touchscreen input
                        if pygame.mouse.get_pressed()[0]:
                                pos = pygame.mouse.get_pos()
                                servers[i].touch(pos[0], pos[1])
                                #print("THSC: ",pos[0],",",pos[1])
                                servers[i].send(print_bytes)
                        elif event.type == pygame.MOUSEBUTTONUP:
                                servers[i].clear_touch()
                                servers[i].send(print_bytes)

                        #Keyboard Mappings
                        elif event.type == pygame.KEYDOWN:
                                if event.key == KBDButtons.C_UP:
                                        servers[i].circle_pad_set(CPAD_Commands.CPADUP)
                                        #print("C_UP")
                                if event.key == KBDButtons.C_LEFT:
                                        servers[i].circle_pad_set(CPAD_Commands.CPADLEFT)
                                        #print("C_LEFT")
                                if event.key == KBDButtons.C_DOWN:
                                        servers[i].circle_pad_set(CPAD_Commands.CPADDOWN)
                                        #print("C_DOWN")
                                if event.key == KBDButtons.C_RIGHT:
                                        servers[i].circle_pad_set(CPAD_Commands.CPADRIGHT)
                                        #print("C_RIGHT")
                                        
                                if event.key == KBDButtons.D_UP:
                                        servers[i].hid_press(HIDButtons.DPADUP)
                                        #print("UP")
                                if event.key == KBDButtons.D_LEFT:
                                        servers[i].hid_press(HIDButtons.DPADLEFT)
                                        #print("LEFT")
                                if event.key == KBDButtons.D_DOWN:
                                        servers[i].hid_press(HIDButtons.DPADDOWN)
                                        #print("DOWN")
                                if event.key == KBDButtons.D_RIGHT:
                                        servers[i].hid_press(HIDButtons.DPADRIGHT)
                                        #print("RIGHT")
                                        
                                if event.key == KBDButtons.B: #b
                                        servers[i].hid_press(HIDButtons.B)
                                        #print("B")
                                if event.key == KBDButtons.A: #a
                                        servers[i].hid_press(HIDButtons.A)
                                        #print("A")
                                if event.key == KBDButtons.Y: #y
                                        servers[i].hid_press(HIDButtons.Y)
                                        #print("Y")
                                if event.key == KBDButtons.X: #x
                                        servers[i].hid_press(HIDButtons.X)
                                        #print("X")
                                if event.key == KBDButtons.L: #l
                                        servers[i].hid_press(HIDButtons.L)
                                        #print("L")
                                if event.key == KBDButtons.R: #r
                                        servers[i].hid_press(HIDButtons.R)
                                        #print("R")
                                if event.key == KBDButtons.ZL: #zl
                                        servers[i].n3ds_zlzr_press(N3DS_Buttons.ZL)
                                        #print("ZL")
                                if event.key == KBDButtons.ZR: #zr
                                        servers[i].n3ds_zlzr_press(N3DS_Buttons.ZR)
                                        #print("ZR")
                                if event.key == KBDButtons.START: #st
                                        servers[i].hid_press(HIDButtons.START)
                                        #print("START")
                                if event.key == KBDButtons.SELECT: #sl
                                        servers[i].hid_press(HIDButtons.SELECT)
                                        #print("SELECT")
                                if event.key == KBDButtons.HOME: #home
                                        servers[i].special_press(Special_Buttons.HOME)
                                        #print("HOME")
                                if event.key == KBDButtons.POWER: #power
                                        servers[i].special_press(Special_Buttons.POWER)
                                        #print("POWER")
                                        
                                if event.key == pygame.K_ESCAPE:
                                        servers[i].clear_everything()
                                        done = True
                                servers[i].send(print_bytes)
                                
                        elif event.type == pygame.KEYUP:
                                if event.key == KBDButtons.D_UP:
                                        servers[i].hid_unpress(HIDButtons.DPADUP)
                                if event.key == KBDButtons.D_LEFT:
                                        servers[i].hid_unpress(HIDButtons.DPADLEFT)
                                if event.key == KBDButtons.D_DOWN:
                                        servers[i].hid_unpress(HIDButtons.DPADDOWN)
                                if event.key == KBDButtons.D_RIGHT:
                                        servers[i].hid_unpress(HIDButtons.DPADRIGHT)

                                if event.key == KBDButtons.C_UP:
                                        servers[i].circle_pad_coords[1] = 0
                                if event.key == KBDButtons.C_LEFT:
                                        servers[i].circle_pad_coords[0] = 0
                                if event.key == KBDButtons.C_DOWN:
                                        servers[i].circle_pad_coords[1] = 0
                                if event.key == KBDButtons.C_RIGHT:
                                        servers[i].circle_pad_coords[0] = 0
                                
                                if event.key == KBDButtons.B: #b
                                        servers[i].hid_unpress(HIDButtons.B)
                                if event.key == KBDButtons.A: #a
                                        servers[i].hid_unpress(HIDButtons.A)
                                if event.key == KBDButtons.Y: #y
                                        servers[i].hid_unpress(HIDButtons.Y)
                                if event.key == KBDButtons.X: #x
                                        servers[i].hid_unpress(HIDButtons.X)
                                if event.key == KBDButtons.L: #l
                                        servers[i].hid_unpress(HIDButtons.L)
                                if event.key == KBDButtons.R: #r
                                        servers[i].hid_unpress(HIDButtons.R)
                                if event.key == KBDButtons.ZL: #zl
                                        servers[i].n3ds_zlzr_unpress(N3DS_Buttons.ZL)
                                if event.key == KBDButtons.ZR: #zr
                                        servers[i].n3ds_zlzr_unpress(N3DS_Buttons.ZR)
                                if event.key == KBDButtons.START: #st
                                        servers[i].hid_unpress(HIDButtons.START)
                                if event.key == KBDButtons.SELECT: #sl
                                        servers[i].hid_unpress(HIDButtons.SELECT)
                                if event.key == KBDButtons.HOME: #hm
                                        servers[i].special_unpress(Special_Buttons.HOME)
                                if event.key == KBDButtons.POWER: #pw
                                        servers[i].special_unpress(Special_Buttons.POWER)
                                servers[i].send(print_bytes)

                        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                        if event.type == pygame.JOYBUTTONDOWN:
                                print("Joystick {} button {} pressed.".format(event.joy,event.button))
                                servers[i].press(buttonMappings[event.button])
                                servers[i].send(print_bytes)
                        if event.type == pygame.JOYBUTTONUP:
                                print("Joystick {} button {} released.".format(event.joy,event.button))
                                servers[i].unpress(buttonMappings[event.button])
                                servers[i].send(print_bytes)
                        if event.type == pygame.JOYAXISMOTION:
                                #if event.axis in range(2,3): print("Joystick {} axis {} moved to {}.".format(event.joy,event.axis, event.value))
                                if event.axis == 0: servers[i].circle_pad_coords[0] = int(32767*event.value) #ls x
                                if event.axis == 1: servers[i].circle_pad_coords[1] = int(-32767*event.value) #ls y
                                if event.axis == 2: #l trig
                                        if event.value >= 0: servers[i].press(HIDButtons.L)
                                        else: servers[i].unpress(HIDButtons.L)
                                if event.axis == 3: #r trig
                                        if event.value >= 0: servers[i].press(HIDButtons.R)
                                        else: servers[i].unpress(HIDButtons.R)
                                if event.axis == 4: print("soon") #rs y
                                if event.axis == 5: print("TM")   #rs x
                                servers[i].send(print_bytes)
                                
                        #server.send()       #0sx 1sy 4cy 5cx 2l 3r
print("clearing everything...")
for i2 in servers:
        servers[i].clear_everything()
        servers[i].send(print_bytes)
pygame.quit()
        
        

