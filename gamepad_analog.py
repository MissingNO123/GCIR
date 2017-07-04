import sys, time
from TPPFLUSH.tppflush import *

if len(sys.argv) < 2:
	server = input("3DS IP >").strip()
else:
        server = sys.argv[1]
        
server=LumaInputServer(server)
        
print("please wait...")
import pygame

done=False

buttonMappings = [
        HIDButtons.SELECT,
        HIDButtons.SELECT, # not used
        HIDButtons.SELECT, # not used
        HIDButtons.START,
        HIDButtons.DPADUP,
        HIDButtons.DPADRIGHT,
        HIDButtons.DPADDOWN,
        HIDButtons.DPADLEFT,
        HIDButtons.L, # really L2 
        HIDButtons.R, # really R2
        HIDButtons.L,
        HIDButtons.R,
        HIDButtons.X,
        HIDButtons.A,
        HIDButtons.B,
        HIDButtons.Y
]

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
                if event.type == pygame.QUIT: # If user clicked close
                    done=True

                #Touchscreen input
                if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        server.touch(pos[0], pos[1])
                        #print("THSC: ",pos[0],",",pos[1])
                        server.send()
                elif event.type == pygame.MOUSEBUTTONUP:
                        server.clear_touch()
                        server.send()

                #Special Buttons on Keyboard
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                done=True
                        if event.key == pygame.K_h:
                                server.press(Special_Buttons.HOME)
                        if event.key == pygame.K_p:
                                server.press(Special_Buttons.POWER)
                        server.send()
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_h:
                                server.unpress(Special_Buttons.HOME)
                        if event.key == pygame.K_p:
                                server.unpress(Special_Buttons.POWER)
                        server.send()

                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                        print("Joystick {} button {} pressed.".format(event.joy,event.button))
                        if 4 <= event.button <= 7:
                                axis_x = 0
                                axis_y = 0
                                if event.button == 4:
                                        axis_y = 32767
                                if event.button == 6:
                                        axis_y = -32767
                                if event.button == 5:
                                        axis_x = 32767
                                if event.button == 7:
                                        axis_x = -32767

                                server.circle_pad_coords[0] = axis_x #ls x
                                server.circle_pad_coords[1] = axis_y #ls 
                        else:
                                server.press(buttonMappings[event.button])
                        
                        server.send()
                if event.type == pygame.JOYBUTTONUP:
                        print("Joystick {} button {} released.".format(event.joy,event.button))
                        if 4 <= event.button <= 7:
                                axis_x = 0
                                axis_y = 0

                                server.circle_pad_coords[0] = axis_x #ls x
                                server.circle_pad_coords[1] = axis_y #ls 
                        else:
                                server.unpress(buttonMappings[event.button])

                        server.send()
                '''
                if event.type == pygame.JOYAXISMOTION:
                        #if event.axis in range(2,3): print("Joystick {} axis {} moved to {}.".format(event.joy,event.axis, event.value))
                        if event.axis == 0: server.circle_pad_coords[0] = int(32767*event.value) #ls x
                        if event.axis == 1: server.circle_pad_coords[1] = int(-32767*event.value) #ls y
                        if event.axis == 2: #l trig
                                if event.value >= 0: server.press(HIDButtons.L)
                                else: server.unpress(HIDButtons.L)
                        if event.axis == 3: #r trig
                                if event.value >= 0: server.press(HIDButtons.R)
                                else: server.unpress(HIDButtons.R)
                        if event.axis == 4: print("soon") #rs y
                        if event.axis == 5: print("TM")   #rs x
                        server.send()
                '''
                        
                #server.send()       #0sx 1sy 4cy 5cx 2l 3r
print("resetting everything...")
server.circle_pad_coords[0:2] = [0,0]
server.cstick_coords[0:2] = [0,0]
for button in HIDButtons: server.unpress(button)
for button in N3DS_Buttons: server.unpress(button)
for i in range(1,50):
        server.send()
pygame.quit()
        
        

