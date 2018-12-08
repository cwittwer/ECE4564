#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes, KeyEvent
import socket
import sys

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverIP = '172.29.27.166'
port = 55548
backlog = 5
size = 1024

s.connect((serverIP, port))
gamepad = InputDevice('/dev/input/event3')

aBtn = 'BTN_A';
bBtn = 'BTN_B';
yBtn = 'BTN_Y';
xBtn = 'BTN_X';
homeBtn = 'KEY_HOMEPAGE';
backBtn = 'KEY_BACK';
startBtn = 'BTN_START';
thumbrBtn = 'BTN_THUMBR';
thumblBtn = 'BTN_THUMBL';
triggerrBtn = 'BTN_TR';
triggerlBtn = 'BTN_TL';
thrx = 'ABS_Z' #right thumbstick x axis
thrx_print = True
thry = 'ABS_RZ' #right thumbstick y axis
thry_print = True
thly = 'ABS_Y' #left thumbstick y axis
thly_print = True
thlx = 'ABS_X' #left thumbstick x axis
thlx_print = True
dpadx = 'ABS_HAT0X' #dpad x axis
dpadx_print = True
dpady = 'ABS_HAT0Y' #dpad y axis
dpady_print = True
gas = 'ABS_GAS' #right bottom trigger
gas_print = True
brake = 'ABS_BRAKE' #left bottom trigger
brake_print = True

control = False #if false, control tracks, if true control arm
LED = False #true if led on, false if off

print('Initialized to Control Tracks')

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == aBtn:
                print('LED Toggle ON/OFF')
                s.send(('LED').encode('utf-8'))
            elif keyevent.keycode[1] == yBtn:
                print('y button')
            elif keyevent.keycode[0] == bBtn:
                print('b button')
            elif keyevent.keycode[1] == xBtn:
                print('X button')
            elif keyevent.keycode == homeBtn:
                control = ~control
                if(control):
                    print('Controlling arm')
                    s.send(('arm').encode('utf-8'))
                else:
                    print('Controlling tracks')
                    s.send(('tracks').encode('utf-8'))
            elif keyevent.keycode == backBtn:
                print('back')
            elif keyevent.keycode == startBtn:
                print('start')
            elif keyevent.keycode == thumbrBtn:
                print('right thumb')
            elif keyevent.keycode == thumblBtn:
                print('left thumb')
            elif keyevent.keycode == triggerrBtn:
                print('right trigger')
            elif keyevent.keycode == triggerlBtn:
                print('left trigger')
        elif keyevent.keystate == KeyEvent.key_up:
            print('up')
            s.send(('off').encode('utf-8'))
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if ecodes.bytype[absevent.event.type][absevent.event.code] == thrx:
            if absevent.event.value > 100:
                if(thrx_print):
                    thrx_print = False
            elif absevent.event.value < -100:
                if(thrx_print):
                    thrx_print = False
            elif absevent.event.value == 0:
                if(thrx_print == False):
                    thrx_print = True
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == thry:
            if absevent.event.value > 100:
                if(thry_print):
                    if(control):
                        print('Elbow down')
                        s.send(('Elbow down').encode('utf-8'))
                    else:
                        print(' ')
                    thry_print = False
            elif absevent.event.value < -100:
                if(thry_print):
                    if(control):
                        print('Elbow up')
                        s.send(('Elbow up').encode('utf-8'))
                    else:
                        print(' ')
                    thry_print = False
            elif absevent.event.value >= -100 or absevent.event.value <= 100:
                if(thry_print == False):
                    if(control):
                        print('Elbow stop')
                        s.send(('Elbow stop').encode('utf-8'))
                    else:
                        print(' ')
                    thry_print = True
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == thlx:
            if absevent.event.value > 100:
                if(thlx_print):
                    if(control):
                        print('Shoulder right')
                        s.send(('Shoulder right').encode('utf-8'))
                    else:
                        print('Turn Tracks Right')
                        s.send(('Turn Tracks Right').encode('utf-8'))
                    thlx_print = False
            elif absevent.event.value < -100:
                if(thlx_print):
                    if(control):
                        print('Shoulder left')
                        s.send(('Shoulder left').encode('utf-8'))
                    else:
                        print('Turn Tracks Left')
                        s.send(('Turn Tracks Left').encode('utf-8'))
                    thlx_print = False
            elif absevent.event.value >= -100 or absevent.event.value <= 100:
                if(thlx_print == False):
                    if(control):
                        print('Shoulder stop')
                        s.send(('Shoulder stop').encode('utf-8'))
                    else:
                        print('Turning Stopped')
                        s.send(('Turning Stopped').encode('utf-8'))
                    thlx_print = True
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == thly:
            if absevent.event.value > 100:
                if(thly_print):
                    if(control):
                        print('Arm down')
                        s.send(('Arm down').encode('utf-8'))
                    else:
                        print(' ')
                    thly_print = False
            elif absevent.event.value < -100:
                if(thly_print):
                    if(control):
                        print('Arm up')
                        s.send(('Arm up').encode('utf-8'))
                    else:
                        print(' ')
                    thly_print = False
            elif absevent.event.value >= -100 or absevent.event.value <= 100:
                if(thly_print == False):
                    if(control):
                        print('Arm stop')
                        s.send(('Arm stop').encode('utf-8'))
                    else:
                        print(' ')
                    thly_print = True
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == dpadx:
            if absevent.event.value == -1:
                if(control):
                    print('Fingers open')
                    s.send(('Fingers Open').encode('utf-8'))
                else:
                    print(' ')
            elif absevent.event.value == 1:
                if(control):
                    print('Fingers close')
                    s.send(('Fingers Close').encode('utf-8'))
                else:
                    print(' ')
            elif absevent.event.value == 0:
                if(control):
                    print('Fingers stop')
                    s.send(('Fingers stop').encode('utf-8'))
                else:
                    print(' ')
            else: #should never happen
                if(control):
                    print(('Fingers stop').encode('utf-8'))
                else:
                    print(' ')
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == dpady:
            if absevent.event.value == -1:
                if(control):
                    print('Wrist up')
                    s.send(('Wrist up').encode('utf-8'))
                else:
                    print(' ')
            elif absevent.event.value == 1:
                if(control):
                    print('Wrist down')
                    s.send(('Wrist down').encode('utf-8'))
                else:
                    print(' ')
            elif absevent.event.value == 0:
                if(control):
                    print('Wrist stop')
                    s.send(('Wrist stop').encode('utf-8'))
                else:
                    print(' ')
            else: #should never happen
                print('dpad release maybe')
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == gas:
            val = absevent.event.value
            if val <= 50:
                if gas_print == False:
                    if(control):
                        print("")
                    else:
                        print('gas trigger released')
                        s.send(('gas trigger released').encode('utf-8'))
                    gas_print = True
            if val > 50:
                if gas_print:
                    if(control):
                        print("")
                    else:
                        print('forward')
                        s.send(('forward').encode('utf-8'))
                    gas_print = False
            '''
            elif val <= 410:
                print('less than 10% gas trigger')
            elif val >= 410 and val <= 820: 
                print('10-20% gas trigger')
            elif val >= 820 and val <= 1230:
                print('20-30% gas trigger')
            elif val >= 1230 and val <= 1640:
                print('30-40% gas trigger')
            elif val >= 1640 and val <= 2050:
                print('40-50% gas trigger')
            elif val >= 2050 and val <= 2460:
                print('50-60% gas trigger')
            elif val >= 2460 and val <= 2870:
                print('60-70% gas trigger')
            elif val >= 2870 and val <= 3280:
                print('70-80% gas trigger')
            elif val >= 3280 and val <= 3690:
                print('80-90% gas trigger')
            elif val >= 3690:
                print('90-100% gas trigger')
            '''
        elif ecodes.bytype[absevent.event.type][absevent.event.code] == brake:
            val = absevent.event.value
            if val <= 500:
                if(brake_print == False):
                    if(control):
                        print("")
                    else:
                        print('reverse released')
                        s.send(('reverse release').encode('utf-8'))
                    brake_print = True
            if val > 500:
                if brake_print:
                    if(control):
                        print("")
                    else:
                        print('reverse')
                        s.send(('reverse').encode('utf-8'))
                    brake_print = False
            '''
            if val == 0:
                print('brake trigger released')
            elif val <= 410:
                print('less than 10% brake trigger')
            elif val >= 410 and val <= 820: 
                print('10-20% brake trigger')
            elif val >= 820 and val <= 1230:
                print('20-30% brake trigger')
            elif val >= 1230 and val <= 1640:
                print('30-40% brake trigger')
            elif val >= 1640 and val <= 2050:
                print('40-50% brake trigger')
            elif val >= 2050 and val <= 2460:
                print('50-60% brake trigger')
            elif val >= 2460 and val <= 2870:
                print('60-70% brake trigger')
            elif val >= 2870 and val <= 3280:
                print('70-80% brake trigger')
            elif val >= 3280 and val <= 3690:
                print('80-90% brake trigger')
            elif val >= 3690:
                print('90-100% brake trigger')
            '''
